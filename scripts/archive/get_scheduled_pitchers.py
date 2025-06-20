#!/usr/bin/env python3
"""
Script para obtener los lanzadores programados de los juegos de la temporada.
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient
from src.data.data_manager import load_season_data, save_season_data, SEASON_DATA_FILE

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

def main():
    """Función principal."""
    print("=== ACTUALIZANDO DATOS DE LANZADORES DE LA TEMPORADA ===\n")
    
    # 1. Cargar datos existentes de la temporada
    print("Cargando datos de la temporada...")
    season_data = load_season_data()
    
    if not season_data or 'games' not in season_data or not season_data['games']:
        print("[ERROR] No se pudieron cargar los juegos de la temporada.")
        return
    
    print(f"Se encontraron {len(season_data['games'])} juegos en la temporada.")
    
    # 2. Obtener rango de fechas de los juegos
    game_dates = [game['date'] for game in season_data['games'] if 'date' in game]
    if not game_dates:
        print("[ERROR] No se encontraron fechas de juegos.")
        return
    
    start_date = min(game_dates)
    end_date = max(game_dates)
    
    print(f"Obteniendo lanzadores programados del {start_date} al {end_date}...")
    
    # 3. Obtener juegos con lanzadores programados
    scheduled_games = get_scheduled_games_with_pitchers(start_date, end_date)
    
    if not scheduled_games:
        print("[ERROR] No se encontraron juegos con lanzadores programados.")
        return
    
    print(f"Se encontraron {len(scheduled_games)} juegos con lanzadores programados.")
    
    # 4. Actualizar datos de la temporada con información de lanzadores
    print("Actualizando datos de la temporada...")
    updated_season_data = update_season_data_with_pitchers(season_data, scheduled_games)
    
    # 5. Guardar los datos actualizados
    save_season_data(updated_season_data)
    print(f"\nDatos de la temporada actualizados exitosamente.")
    
    # Mostrar estadísticas
    games_with_pitchers = sum(1 for game in updated_season_data.get('games', []) 
                            if 'pitchers' in game and (game['pitchers']['home'] or game['pitchers']['away']))
    
    print(f"\nResumen:")
    print(f"- Total de juegos: {len(updated_season_data.get('games', []))}")
    print(f"- Juegos con al menos un lanzador: {games_with_pitchers}")
    print(f"- Última actualización: {updated_season_data.get('last_updated')}")

if __name__ == "__main__":
    main()
