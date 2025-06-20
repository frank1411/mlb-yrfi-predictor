#!/usr/bin/env python3
"""
Script para cargar los datos de la temporada actual de MLB.
Este script debe ejecutarse periódicamente para mantener los datos actualizados.
"""
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Union
from collections import defaultdict

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient
from src.data.data_manager import (
    save_season_data, get_first_inning_yrfi, get_game_id,
    update_team_stats, load_season_data, SEASON_DATA_FILE
)

def get_season_games() -> dict:
    """Obtiene todos los juegos de la temporada actual, incluyendo la Serie de Tokio."""
    client = MLBClient()
    all_games = []
    today = datetime.now()
    
    # Definir los rangos de fechas importantes
    date_ranges = [
        # Serie de Tokio (18-19 de marzo)
        (datetime(2025, 3, 18), datetime(2025, 3, 19)),
        # Resto de la temporada regular (27 de marzo hasta hoy)
        (datetime(2025, 3, 27), today)
    ]
    
    # Procesar cada rango de fechas
    for start_date, end_date in date_ranges:
        current_date = start_date
        print(f"\nObteniendo juegos desde {start_date.strftime('%Y-%m-%d')} hasta {end_date.strftime('%Y-%m-%d')}...")
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            print(f"Procesando fecha: {date_str}")
            
            try:
                # Obtener juegos de la fecha
                schedule = client.get_schedule(date=date_str)
                games = []
                
                if 'dates' in schedule and schedule['dates']:
                    games = schedule['dates'][0].get('games', [])
                    # Filtrar solo los juegos de MLB (excluir juegos de ligas menores, etc.)
                    games = [g for g in games if g.get('gameType') == 'R']
                    
                    # Si es el rango problemático (1-7 de mayo), forzar la obtención de partidos de Houston
                    if datetime(2025, 5, 1) <= current_date <= datetime(2025, 5, 7):
                        print(f"Obteniendo partidos específicos de Houston Astros para {date_str}...")
                        houston_games = client.get_games_for_team_and_date(117, current_date)
                        if houston_games:
                            # Combinar los juegos, evitando duplicados
                            game_ids = {game['gamePk'] for game in games} if games else set()
                            for game in houston_games:
                                if game['gamePk'] not in game_ids and game.get('gameType') == 'R':
                                    print(f"  Añadiendo partido forzado de Houston: {game['teams']['away']['team']['name']} @ {game['teams']['home']['team']['name']} - {game['status']['statusCode']}")
                                    games.append(game)
                                    game_ids.add(game['gamePk'])
                
                # Forzar la inclusión del partido del 4 de mayo si es necesario
                if date_str == "2025-05-04":
                    print(f"\n[DEBUG] Procesando fecha especial: {date_str}")
                    print(f"[DEBUG] Juegos antes de forzar: {len(games)}")
                    
                    if not any(g.get('gamePk') == 778055 for g in games):
                        print("[DEBUG] No se encontró el partido 778055 en los juegos obtenidos")
                        print("[DEBUG] Intentando obtener el partido específico...")
                        
                        try:
                            forced_game = client._make_request("schedule", params={"gamePk": 778055})
                            print(f"[DEBUG] Respuesta de la API: {bool(forced_game)}")
                            
                            if 'dates' in forced_game and forced_game['dates']:
                                forced_games = forced_game['dates'][0].get('games', [])
                                print(f"[DEBUG] Juegos forzados encontrados: {len(forced_games)}")
                                
                                for game in forced_games:
                                    if game.get('gamePk') == 778055 and game.get('gameType') == 'R':
                                        print(f"[DEBUG] Añadiendo partido forzado: {game['teams']['away']['team']['name']} @ {game['teams']['home']['team']['name']} - {game['status']['statusCode']}")
                                        games.append(game)
                                        print(f"[DEBUG] Juego añadido. Total de juegos ahora: {len(games)}")
                                    else:
                                        print(f"[DEBUG] Juego no cumple condiciones: {game.get('gamePk')} - {game.get('gameType')}")
                            else:
                                print("[DEBUG] No se encontraron fechas en la respuesta forzada")
                        except Exception as e:
                            print(f"[DEBUG] Error al obtener el partido forzado: {e}")
                    else:
                        print("[DEBUG] El partido 778055 ya está en la lista de juegos")
                
                if games:
                    all_games.extend(games)
                print(f"  Encontrados {len(games)} juegos de MLB para {date_str}")
            except Exception as e:
                print(f"  Error al obtener juegos para {date_str}: {e}")
            
            # Pasar al siguiente día
            current_date += timedelta(days=1)
    
    print(f"\nTotal de juegos de MLB obtenidos: {len(all_games)}")
    return all_games

def get_scheduled_games_with_pitchers(start_date: str, end_date: str) -> List[Dict]:
    """
    Obtiene los juegos programados con sus lanzadores para un rango de fechas.
    
    Args:
        start_date: Fecha de inicio en formato 'YYYY-MM-DD'
        end_date: Fecha de fin en formato 'YYYY-MM-DD'
        
    Returns:
        Lista de diccionarios con información de los juegos y sus lanzadores.
    """
    client = MLBClient()
    
    # Parámetros para la consulta
    params = {
        'sportId': 1,  # MLB
        'startDate': start_date,
        'endDate': end_date,
        'hydrate': 'probablePitcher',  # Incluir lanzadores probables
        'fields': 'dates,date,games,gamePk,gameDate,teams,home,away,team,id,name,probablePitcher,fullName,id,gameType'
    }
    
    try:
        response = client._make_request('schedule', params=params)
        games_with_pitchers = []
        
        # Procesar la respuesta
        for date_data in response.get('dates', []):
            for game in date_data.get('games', []):
                # Solo incluir juegos de temporada regular
                if game.get('gameType') != 'R':
                    continue
                    
                game_data = {
                    'gamePk': game.get('gamePk'),
                    'gameDate': game.get('gameDate'),
                    'teams': {}
                }
                
                # Obtener lanzadores probables
                for team_type in ['home', 'away']:
                    team_data = game.get('teams', {}).get(team_type, {})
                    team_info = {
                        'team': {
                            'id': team_data.get('team', {}).get('id'),
                            'name': team_data.get('team', {}).get('name')
                        }
                    }
                    
                    # Obtener información del lanzador probable
                    pitcher = team_data.get('probablePitcher')
                    if pitcher:
                        team_info['probablePitcher'] = {
                            'id': pitcher.get('id'),
                            'name': pitcher.get('fullName')
                        }
                    
                    game_data['teams'][team_type] = team_info
                
                games_with_pitchers.append(game_data)
        
        return games_with_pitchers
        
    except Exception as e:
        print(f"Error al obtener juegos programados: {str(e)}")
        return []

def update_season_data_with_pitchers(season_data: Dict, scheduled_games: List[Dict]) -> Dict:
    """
    Actualiza los datos de la temporada con la información de los lanzadores.
    
    Args:
        season_data: Datos de la temporada actual.
        scheduled_games: Lista de juegos con lanzadores programados.
        
    Returns:
        Datos de la temporada actualizados con la información de lanzadores.
    """
    # Crear un diccionario de juegos por gamePk para búsqueda rápida
    scheduled_games_dict = {str(game['gamePk']): game for game in scheduled_games}
    
    # Actualizar cada juego en season_data con la información de lanzadores
    updated_games = []
    
    for game in season_data.get('games', []):
        game_pk = str(game.get('gamePk'))
        scheduled_game = scheduled_games_dict.get(game_pk)
        
        if scheduled_game:
            # Agregar información de lanzadores al juego
            game['pitchers'] = {
                'home': scheduled_game['teams']['home'].get('probablePitcher'),
                'away': scheduled_game['teams']['away'].get('probablePitcher')
            }
        
        updated_games.append(game)
    
    # Actualizar los juegos en los datos de la temporada
    season_data['games'] = updated_games
    season_data['last_updated'] = datetime.now().isoformat()
    
    return season_data

def process_game(game: dict) -> Optional[dict]:
    """
    Procesa un juego individual y extrae la información relevante.
    """
    game_status = game.get('status', {})
    status_code = str(game_status.get('statusCode', ''))
    abstract_code = str(game_status.get('abstractGameCode', ''))
    detailed_state = str(game_status.get('detailedState', '')).lower()
    game_type = str(game.get('gameType', ''))
    
    # Debug: Mostrar información del juego antes de decidir si incluirlo
    game_date = game.get('officialDate', game.get('gameDate', 'N/A').split('T')[0] if game.get('gameDate') else 'N/A')
    away_team = game.get('teams', {}).get('away', {}).get('team', {}).get('name', 'N/A')
    home_team = game.get('teams', {}).get('home', {}).get('team', {}).get('name', 'N/A')
    
    # Incluir juegos que estén marcados como finalizados o completados temprano
    is_valid_game = (
        abstract_code == 'F' and  # Juego finalizado
        (detailed_state in ['final', 'game over'] or 'completed early' in detailed_state) and
        status_code in ['F', 'O', 'D', 'C', 'CE', 'FR'] and  # Final, Final en extras, Final definitivo, Completed, Completed Early, Final Rain
        game_type == 'R'  # Solo juegos de temporada regular
    )
    
    # Debug: Mostrar información detallada para partidos de Houston Astros
    if 'Houston Astros' in f"{home_team} {away_team}" and '2025-05-04' in game_date:
        print("\n[DEBUG] Partido de Houston Astros el 4 de mayo encontrado:")
        print(f"  Equipos: {away_team} @ {home_team}")
        print(f"  Estado: {abstract_code}, Código: {status_code}, Detalles: {detailed_state}, Tipo: {game_type}")
        print(f"  is_valid_game: {is_valid_game}")
        print(f"  Juego completo: {json.dumps(game, indent=2, default=str)}")
        print("-" * 80)
    
    if not is_valid_game:
        print(f"[DEBUG] Descartando juego - {game_date} - {away_team} @ {home_team} - Estado: {abstract_code}, Código: {status_code}, Detalles: {detailed_state}, Tipo: {game_type}")
        return None
        
    print(f"[DEBUG] Incluyendo juego - {game_date} - {away_team} @ {home_team} - Estado: {abstract_code}, Código: {status_code}, Detalles: {detailed_state}, Tipo: {game_type}")
        
    # Obtener YRFI para el juego
    yrfi_data = get_first_inning_yrfi(game)
    
    # Extraer solo la parte de la fecha (YYYY-MM-DD) si hay una 'T' en la cadena
    game_date = game.get('gameDate', '')
    if 'T' in game_date:
        game_date = game_date.split('T')[0]
        
    # Inicializar el juego procesado con valores por defecto
    processed_game = {
        'game_id': get_game_id(game),
        'date': game_date,
        'home_yrfi': yrfi_data['home_yrfi'],
        'away_yrfi': yrfi_data['away_yrfi'],
        'game_yrfi': yrfi_data['game_yrfi'],
        'status': {
            'abstractGameCode': abstract_code,
            'statusCode': status_code,
            'detailedState': detailed_state
        }
    }
    
    # Manejar diferentes formatos de juegos
    if 'teams' in game and 'home' in game['teams'] and 'away' in game['teams']:
        # Formato completo con equipos anidados
        processed_game['home_team'] = str(game['teams']['home']['team']['id'])
        processed_game['home_team_name'] = game['teams']['home']['team'].get('name', 'Desconocido')
        processed_game['away_team'] = str(game['teams']['away']['team']['id'])
        processed_game['away_team_name'] = game['teams']['away']['team'].get('name', 'Desconocido')
    elif 'home_team' in game and 'away_team' in game:
        # Formato ya procesado
        processed_game['home_team'] = str(game['home_team'])
        processed_game['home_team_name'] = game.get('home_team_name', 'Desconocido')
        processed_game['away_team'] = str(game['away_team'])
        processed_game['away_team_name'] = game.get('away_team_name', 'Desconocido')
    else:
        # No se pudo determinar los equipos
        print(f"Advertencia: No se pudo determinar los equipos para el juego {game.get('game_id', 'desconocido')}")
        return None
    
    # Guardar el ID del juego para referencia futura
    if 'gamePk' in game:
        processed_game['gamePk'] = game['gamePk']
    
    return processed_game

def main():
    print("=== Inicialización de datos de la temporada 2025 ===")
    print(f"Incluyendo la Serie de Tokio (18-19 mar) y temporada regular hasta {datetime.now().strftime('%d %b')}\n")
    
    # Inicializar diccionario para juegos finalizados
    final_games = {}
    
    # Obtener todos los juegos de la temporada
    print("\nObteniendo juegos de la temporada...")
    all_games = get_season_games()
    print(f"Total de juegos obtenidos: {len(all_games)}")
    
    # Procesar los juegos
    print("\nProcesando juegos...")
    for i, game in enumerate(all_games, 1):
        if i % 10 == 0 or i == 1 or i == len(all_games):
            print(f"Procesando juego {i}/{len(all_games)}...")
        
        try:
            # Procesar el juego
            processed_game = process_game(game)
            
            if processed_game:  # Solo agregar si se pudo procesar correctamente
                game_id = processed_game.get('game_id')
                if game_id:
                    final_games[game_id] = processed_game
            else:
                print(f"Advertencia: No se pudo procesar el juego: {game.get('gamePk', 'desconocido')}")
        except Exception as e:
            print(f"Error al procesar juego {game.get('gamePk', 'desconocido')}: {str(e)}")
    
    # Convertir a lista para procesar
    final_games_list = list(final_games.values())
    
    print(f"\nTotal de juegos finalizados: {len(final_games_list)}")
    
    if not final_games_list:
        print("No se encontraron juegos finalizados para procesar.")
        return
        
    # Actualizar solo estadísticas de equipos (sin lanzadores por ahora)
    teams = update_team_stats({}, final_games_list)
    
    # Preparar datos para guardar
    season_data = {
        'last_updated': datetime.now().isoformat(),
        'games': final_games_list,
        'teams': teams,
        'pitchers': {}  # Inicializar diccionario vacío para lanzadores
    }

    # Guardar los datos iniciales
    print("\nGuardando datos iniciales...")
    save_season_data(season_data)

    print("\n=== Actualizando información de lanzadores ===")

    # Obtener rango de fechas de los juegos
    game_dates = [game['date'] for game in season_data['games'] if 'date' in game]
    if not game_dates:
        print("[ERROR] No se encontraron fechas de juegos.")
        return

    start_date = min(game_dates)
    end_date = max(game_dates)

    print(f"Obteniendo lanzadores programados del {start_date} al {end_date}...")

    # Obtener juegos con lanzadores programados
    scheduled_games = get_scheduled_games_with_pitchers(start_date, end_date)

    if not scheduled_games:
        print("[ERROR] No se encontraron juegos con lanzadores programados.")
        return

    print(f"Se encontraron {len(scheduled_games)} juegos con lanzadores programados.")

    # Actualizar datos con información de lanzadores
    print("Actualizando datos con información de lanzadores...")
    updated_season_data = update_season_data_with_pitchers(season_data, scheduled_games)

    # Calcular estadísticas de lanzadores
    games_with_pitchers = sum(1 for game in updated_season_data.get('games', []) 
                            if 'pitchers' in game and (game['pitchers']['home'] or game['pitchers']['away']))

    # Guardar los datos actualizados
    print("\nGuardando datos actualizados...")
    save_season_data(updated_season_data)

    print("\n¡Datos de la temporada actualizados exitosamente!")
    print(f"Total de juegos procesados: {len(updated_season_data['games'])}")
    print(f"Total de equipos: {len(updated_season_data['teams'])}")
    print(f"Juegos con información de lanzadores: {games_with_pitchers}/{len(updated_season_data['games'])}")

    # Mostrar resumen de YRFI
    total_yrfi = sum(1 for game in updated_season_data['games'] if game.get('game_yrfi', False))
    yrfi_pct = (total_yrfi / len(updated_season_data['games'])) * 100 if updated_season_data['games'] else 0
    print(f"\nEstadísticas YRFI:")
    print(f"- Total de juegos con YRFI: {total_yrfi}/{len(updated_season_data['games'])} ({yrfi_pct:.1f}%)")

    # Mostrar los equipos con más YRFI
    print("\nTop 5 equipos con más YRFI:")
    teams_yrfi = []
    for team_id, team_data in updated_season_data['teams'].items():
        if 'name' in team_data:
            teams_yrfi.append((team_data['name'], team_data['total_yrfi'], team_data['total_games']))

    for team, yrfi, total in sorted(teams_yrfi, key=lambda x: x[1], reverse=True)[:5]:
        print(f"- {team}: {yrfi}/{total} ({(yrfi/total)*100:.1f}%)")

    # Mostrar los equipos con menos YRFI
    print("\nTop 5 equipos con menos YRFI:")
    for team, yrfi, total in sorted(teams_yrfi, key=lambda x: x[1])[:5]:
        print(f"- {team}: {yrfi}/{total} ({(yrfi/total)*100:.1f}%)")

    # Mostrar algunos ejemplos de juegos con lanzadores
    print("\nEjemplos de juegos con lanzadores:")
    games_with_pitchers = [g for g in updated_season_data['games'] 
                          if 'pitchers' in g and (g['pitchers']['home'] or g['pitchers']['away'])]

    for game in games_with_pitchers[:3]:
        home_team = updated_season_data['teams'][game['home_team']]['name']
        away_team = updated_season_data['teams'][game['away_team']]['name']
        home_pitcher = game['pitchers']['home'].get('name', 'No disponible') if game['pitchers']['home'] else 'No disponible'
        away_pitcher = game['pitchers']['away'].get('name', 'No disponible') if game['pitchers']['away'] else 'No disponible'

        print(f"\n{game['date']} - {away_team} @ {home_team}")
        print(f"Lanzadores: {away_pitcher} @ {home_pitcher}")
        print(f"YRFI: {'Sí' if game.get('game_yrfi') else 'No'}")

if __name__ == "__main__":
    main()
