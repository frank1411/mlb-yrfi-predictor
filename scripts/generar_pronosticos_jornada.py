#!/usr/bin/env python3
"""
Script para generar pronósticos YRFI para todos los partidos de la próxima jornada de MLB.
"""
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient

# Importar funciones de generar_pronostico
from scripts.generar_pronostico import (
    load_season_data, get_pitcher_stats, calculate_game_probability,
    format_prediction, save_prediction
)

# Mapeo de IDs de equipos a nombres (para referencia)
TEAM_IDS_TO_NAMES = {
    '108': 'Los Angeles Angels',
    '109': 'Arizona Diamondbacks',
    '110': 'Baltimore Orioles',
    '111': 'Boston Red Sox',
    '112': 'Chicago Cubs',
    '113': 'Cincinnati Reds',
    '114': 'Cleveland Guardians',
    '115': 'Colorado Rockies',
    '116': 'Detroit Tigers',
    '117': 'Houston Astros',
    '118': 'Kansas City Royals',
    '119': 'Los Angeles Dodgers',
    '120': 'Washington Nationals',
    '121': 'New York Mets',
    '133': 'Oakland Athletics',
    '134': 'Pittsburgh Pirates',
    '135': 'San Diego Padres',
    '136': 'Seattle Mariners',
    '137': 'San Francisco Giants',
    '138': 'St. Louis Cardinals',
    '139': 'Tampa Bay Rays',
    '140': 'Texas Rangers',
    '141': 'Toronto Blue Jays',
    '142': 'Minnesota Twins',
    '143': 'Philadelphia Phillies',
    '144': 'Atlanta Braves',
    '145': 'Chicago White Sox',
    '146': 'Miami Marlins',
    '147': 'New York Yankees',
    '158': 'Milwaukee Brewers'
}

def get_next_day_games() -> List[Dict[str, Any]]:
    """
    Obtiene los partidos programados para el día siguiente con sus lanzadores probables.
    
    Returns:
        Lista de diccionarios con información de los partidos y lanzadores.
    """
    client = MLBClient()
    
    # Obtener la fecha de hoy
    today = datetime.now().strftime('%m/%d/%Y')
    
    try:
        # Obtener el calendario para hoy con hidratación extendida
        schedule = client._make_request("schedule", {
            'sportId': 1,  # MLB
            'date': today,
            'hydrate': 'probablePitcher,team,linescore,flags,game(content(editorial(recap))),decisions'
        })
        
        # Extraer partidos
        games = []
        for date_data in schedule.get('dates', []):
            for game_data in date_data.get('games', []):
                game_info = {
                    'game_pk': game_data['gamePk'],
                    'game_date': game_data['gameDate'],
                    'status': game_data['status']['detailedState'],
                    'home_team': {
                        'id': str(game_data['teams']['home']['team']['id']),
                        'name': game_data['teams']['home']['team']['name']
                    },
                    'away_team': {
                        'id': str(game_data['teams']['away']['team']['id']),
                        'name': game_data['teams']['away']['team']['name']
                    },
                    'pitchers': {}
                }
                
                # Función auxiliar para obtener información del lanzador
                def get_pitcher_info(team_side):
                    pitcher_data = {}
                    # Intentar obtener del probablePitcher
                    if 'probablePitcher' in game_data['teams'][team_side]:
                        pitcher = game_data['teams'][team_side]['probablePitcher']
                        if pitcher and 'id' in pitcher:
                            return {
                                'id': str(pitcher['id']),
                                'name': pitcher.get('fullName', 'Por anunciar')
                            }
                    
                    # Si no se encuentra, buscar en el boxscore
                    linescore = game_data.get('linescore', {})
                    if team_side in linescore.get('teams', {}):
                        pitcher = linescore['teams'][team_side].get('probablePitcher', {})
                        if pitcher and 'id' in pitcher:
                            return {
                                'id': str(pitcher['id']),
                                'name': pitcher.get('fullName', 'Por anunciar')
                            }
                    
                    # Si aún no se encuentra, buscar en las decisiones del juego
                    decisions = game_data.get('decisions', {})
                    decision_key = 'winner' if team_side == 'home' else 'loser'
                    if decision_key in decisions:
                        pitcher = decisions[decision_key]
                        return {
                            'id': str(pitcher['id']),
                            'name': pitcher.get('fullName', 'Por anunciar')
                        }
                    
                    # Si no se encuentra, devolver valores por defecto
                    return {'id': None, 'name': 'Por anunciar'}
                
                # Obtener lanzadores para ambos equipos
                game_info['pitchers']['home'] = get_pitcher_info('home')
                game_info['pitchers']['away'] = get_pitcher_info('away')
                
                games.append(game_info)
        
        return games
    except Exception as e:
        print(f"Error al obtener partidos: {e}")
        return []

def generate_predictions_for_games(games: List[Dict[str, Any]], season_data: Dict) -> List[Dict[str, Any]]:
    """
    Genera predicciones para una lista de partidos.
    
    Args:
        games: Lista de diccionarios con información de los partidos
        season_data: Diccionario con los datos de la temporada
        
    Returns:
        Lista de predicciones generadas
    """
    # Mensaje de depuración para ver qué partidos se están recibiendo
    print("\n🔍 DEPURACIÓN: generate_predictions_for_games - Partidos recibidos")
    print("-" * 80)
    for i, game in enumerate(games, 1):
        home_team = game.get('home_team', {}).get('name', 'Desconocido')
        away_team = game.get('away_team', {}).get('name', 'Desconocido')
        game_pk = game.get('game_pk', 'N/A')
        game_date = game.get('game_date', 'N/A')
        
        # Obtener información de lanzadores
        home_pitcher = game.get('pitchers', {}).get('home', {})
        away_pitcher = game.get('pitchers', {}).get('away', {})
        
        print(f"{i}. {away_team} @ {home_team} (ID: {game_pk}, Fecha: {game_date})")
        print(f"   Lanzador Local: {home_pitcher.get('name', 'No definido')} (ID: {home_pitcher.get('id', 'N/A')})")
        print(f"   Lanzador Visitante: {away_pitcher.get('name', 'No definido')} (ID: {away_pitcher.get('id', 'N/A')})")
        print("   " + "-" * 60)
    
    # Mensaje de depuración
    print("\n🔍 DEPURACIÓN: Partidos obtenidos listos para procesar")
    
    predictions = []
    print("\n🔄 Iniciando procesamiento de partidos...")
    print("-" * 60)
    
    for i, game in enumerate(games, 1):
        # Mensaje al inicio de procesamiento de cada partido
        home_team_name = game.get('home_team', {}).get('name', 'Desconocido')
        away_team_name = game.get('away_team', {}).get('name', 'Desconocido')
        game_pk = game.get('game_pk', 'N/A')
        print(f"\n🔍 Procesando partido {i}/{len(games)}: {away_team_name} @ {home_team_name} (ID: {game_pk})")

        try:
            # Obtener información del partido
            home_team_id = game['home_team']['id']
            away_team_id = game['away_team']['id']
            game_date = datetime.fromisoformat(game['game_date'].replace('Z', '+00:00'))
            game_date_str = game_date.strftime('%Y-%m-%d')
            
            # Obtener lanzadores
            home_pitcher = game['pitchers'].get('home', {})
            away_pitcher = game['pitchers'].get('away', {})
            
            # Mostrar información de lanzadores
            print(f"   Lanzadores: {away_pitcher.get('name', 'No definido')} (ID: {away_pitcher.get('id', 'N/A')}) vs {home_pitcher.get('name', 'No definido')} (ID: {home_pitcher.get('id', 'N/A')})")
            
            # Mensaje de depuración detallado
            print("\n" + "="*80)
            print(f"🔍 DEPURACIÓN: Iniciando procesamiento para partido ID: {game_pk}")
            print(f"   Equipos: {away_team_name} @ {home_team_name}")
            print(f"   Estado: {game.get('status', 'No especificado')}")
            print(f"   Lanzador Local: {home_pitcher.get('name', 'No definido')} (ID: {home_pitcher.get('id', 'N/A')})")
            print(f"   Lanzador Visitante: {away_pitcher.get('name', 'No definido')} (ID: {away_pitcher.get('id', 'N/A')})")
            print("="*80 + "\n")
            
            # Si no hay lanzadores, saltar este partido
            if not home_pitcher or not away_pitcher:
                print(f"⚠️  No se encontraron lanzadores para {away_team_name} @ {home_team_name}")
                continue
                
            print(f"✅ Ambos lanzadores están presentes. Continuando con el procesamiento...")
            
            # Obtener estadísticas de los lanzadores
            print(f"\n📊 Obteniendo estadísticas para los lanzadores...")
            
            home_pitcher_id = home_pitcher.get('id')
            home_pitcher_name = home_pitcher.get('name')
            print(f"   Lanzador Local: {home_pitcher_name} (ID: {home_pitcher_id})")
            home_pitcher_stats = get_pitcher_stats(season_data, 
                                                 pitcher_id=home_pitcher_id,
                                                 pitcher_name=home_pitcher_name)
            print(f"   Estadísticas del lanzador local obtenidas: {bool(home_pitcher_stats)}")
            
            away_pitcher_id = away_pitcher.get('id')
            away_pitcher_name = away_pitcher.get('name')
            print(f"   Lanzador Visitante: {away_pitcher_name} (ID: {away_pitcher_id})")
            away_pitcher_stats = get_pitcher_stats(season_data,
                                                 pitcher_id=away_pitcher_id,
                                                 pitcher_name=away_pitcher_name)
            print(f"   Estadísticas del lanzador visitante obtenidas: {bool(away_pitcher_stats)}")
            
            # Generar predicción
            print(f"\n🎯 Generando predicción para {away_team_name} @ {home_team_name}...")
            try:
                game_data = calculate_game_probability(
                    home_team_id=home_team_id,
                    away_team_id=away_team_id,
                    home_pitcher=home_pitcher_stats,
                    away_pitcher=away_pitcher_stats,
                    season_data=season_data
                )
                print(f"✅ Predicción generada exitosamente para el partido {game_pk}")
            except Exception as e:
                print(f"❌ Error al generar predicción para el partido {game_pk}: {str(e)}")
                print(f"Tipo de error: {type(e).__name__}")
                import traceback
                traceback.print_exc()
                continue
            
            # Formatear predicción
            print(f"📝 Formateando predicción para {away_team_name} @ {home_team_name}...")
            try:
                prediction_text = format_prediction(
                    game_data, 
                    home_team_name, 
                    away_team_name, 
                    game_date_str
                )
                print(f"✅ Predicción formateada exitosamente")
            except Exception as e:
                print(f"❌ Error al formatear la predicción: {str(e)}")
                continue
            
            # Mensaje de depuración después de generar la predicción
            print(f"\n✅ Procesamiento completado para partido {i}/{len(games)}: {away_team_name} @ {home_team_name}")
            print(f"   - ID del partido: {game.get('game_pk', 'N/A')}")
            print(f"   - Lanzadores: {away_pitcher.get('name', 'N/A')} vs {home_pitcher.get('name', 'N/A')}")
            print(f"   - Predicción generada: {'Sí' if game_data else 'No'}")
            
            # Mensaje de depuración
            print("✅ Procesamiento completado para el partido")
            
            # Crear resultado con la nueva estructura
            prediction = {
                'game_pk': game.get('game_pk'),  # Asegurar que el game_pk esté incluido
                'game_date': game_date_str,
                'home_team': {
                    'id': home_team_id,
                    'name': home_team_name,
                    'pitcher': {
                        'name': home_pitcher.get('name', 'Por definir'),
                        'yrfi_allowed': home_pitcher_stats.get('home_yrfi_pct', home_pitcher_stats.get('yrfi_pct', 0)) if home_pitcher_stats else 0,
                        'yrfi_ratio': f"{home_pitcher_stats.get('home_yrfi', 0)}/{home_pitcher_stats.get('home_games', 1)}" if home_pitcher_stats and home_pitcher_stats.get('home_games', 0) > 0 else f"{home_pitcher_stats.get('yrfi_games', 0)}/{home_pitcher_stats.get('total_games', 1)}" if home_pitcher_stats else '0/1'
                    },
                    'stats': {
                        'base': {
                            'value': game_data['home_team']['yrfi_pct'],
                            'ratio': f"{game_data['home_team'].get('yrfi', 0)}/{game_data['home_team'].get('games', 1)}"
                        },
                        'tendency': {
                            'value': (game_data['home_team'].get('last_15_yrfi', 0) / game_data['home_team'].get('last_15_games', 1)) * 100 
                                    if game_data['home_team'].get('last_15_games', 0) > 0 else 0,
                            'ratio': f"{game_data['home_team'].get('last_15_yrfi', 0)}/{game_data['home_team'].get('last_15_games', 1)}"
                        }
                    }
                },
                'away_team': {
                    'id': away_team_id,
                    'name': away_team_name,
                    # Mostrar el valor de adjusted_yrfi_pct para depuración
                    'combined_yrfi_pct': round((game_data['away_team']['yrfi_pct'] * 0.45) + 
                        (((game_data['away_team'].get('last_15_yrfi', 0) / game_data['away_team'].get('last_15_games', 1)) * 100 
                        if game_data['away_team'].get('last_15_games', 0) > 0 
                        else game_data['away_team']['yrfi_pct']) * 0.55), 2),
                    'pitcher': {
                        'name': away_pitcher.get('name', 'Por definir'),
                        'yrfi_allowed': away_pitcher_stats.get('away_yrfi_pct', away_pitcher_stats.get('yrfi_pct', 0)) if away_pitcher_stats else 0,
                        'yrfi_ratio': f"{away_pitcher_stats.get('away_yrfi', 0)}/{away_pitcher_stats.get('away_games', 1)}" if away_pitcher_stats and away_pitcher_stats.get('away_games', 0) > 0 else f"{away_pitcher_stats.get('yrfi_games', 0)}/{away_pitcher_stats.get('total_games', 1)}" if away_pitcher_stats else '0/1'
                    },
                    'stats': {
                        'base': {
                            'value': game_data['away_team']['yrfi_pct'],
                            'ratio': f"{game_data['away_team'].get('yrfi', 0)}/{game_data['away_team'].get('games', 1)}"
                        },
                        'tendency': {
                            'value': (game_data['away_team'].get('last_15_yrfi', 0) / game_data['away_team'].get('last_15_games', 1)) * 100 
                                    if game_data['away_team'].get('last_15_games', 0) > 0 else 0,
                            'ratio': f"{game_data['away_team'].get('last_15_yrfi', 0)}/{game_data['away_team'].get('last_15_games', 1)}"
                        }
                    }
                },
                'prediction': {
                    'calculation': {
                        'home_team': {
                            'base': game_data['home_team']['yrfi_pct'],
                            'tendency': (game_data['home_team'].get('last_15_yrfi', 0) / game_data['home_team'].get('last_15_games', 1)) * 100 if game_data['home_team'].get('last_15_games', 0) > 0 else 0,
                            'combined': (game_data['home_team']['yrfi_pct'] * 0.45) + (((game_data['home_team'].get('last_15_yrfi', 0) / game_data['home_team'].get('last_15_games', 1)) * 100 if game_data['home_team'].get('last_15_games', 0) > 0 else game_data['home_team']['yrfi_pct']) * 0.55),
                            'pitcher_impact': away_pitcher_stats.get('away_yrfi_pct', away_pitcher_stats.get('yrfi_pct', 0)) if away_pitcher_stats else 0,
                            'combined': round((game_data['home_team']['yrfi_pct'] * 0.45) + 
                                (((game_data['home_team'].get('last_15_yrfi', 0) / game_data['home_team'].get('last_15_games', 1)) * 100 
                                if game_data['home_team'].get('last_15_games', 0) > 0 
                                else game_data['home_team']['yrfi_pct']) * 0.55), 2),
                            'adjusted': round((((game_data['home_team']['yrfi_pct'] * 0.45) + 
                                (((game_data['home_team'].get('last_15_yrfi', 0) / game_data['home_team'].get('last_15_games', 1)) * 100 
                                if game_data['home_team'].get('last_15_games', 0) > 0 
                                else game_data['home_team']['yrfi_pct']) * 0.55)) * 0.65) + 
                                (away_pitcher_stats.get('away_yrfi_pct', away_pitcher_stats.get('yrfi_pct', 0)) * 0.35) 
                                if away_pitcher_stats else 0, 2)
                        },
                        'away_team': {
                            'base': game_data['away_team']['yrfi_pct'],
                            'tendency': (game_data['away_team'].get('last_15_yrfi', 0) / game_data['away_team'].get('last_15_games', 1)) * 100 if game_data['away_team'].get('last_15_games', 0) > 0 else 0,
                            'combined': (game_data['away_team']['yrfi_pct'] * 0.45) + (((game_data['away_team'].get('last_15_yrfi', 0) / game_data['away_team'].get('last_15_games', 1)) * 100 if game_data['away_team'].get('last_15_games', 0) > 0 else game_data['away_team']['yrfi_pct']) * 0.55),
                            'pitcher_impact': home_pitcher_stats.get('home_yrfi_pct', home_pitcher_stats.get('yrfi_pct', 0)) if home_pitcher_stats else 0,
                            'combined': round((game_data['away_team']['yrfi_pct'] * 0.45) + 
                                (((game_data['away_team'].get('last_15_yrfi', 0) / game_data['away_team'].get('last_15_games', 1)) * 100 
                                if game_data['away_team'].get('last_15_games', 0) > 0 
                                else game_data['away_team']['yrfi_pct']) * 0.55), 2),
                            'adjusted': round((((game_data['away_team']['yrfi_pct'] * 0.45) + 
                                (((game_data['away_team'].get('last_15_yrfi', 0) / game_data['away_team'].get('last_15_games', 1)) * 100 
                                if game_data['away_team'].get('last_15_games', 0) > 0 
                                else game_data['away_team']['yrfi_pct']) * 0.55)) * 0.65) + 
                                (home_pitcher_stats.get('home_yrfi_pct', home_pitcher_stats.get('yrfi_pct', 0)) * 0.35) 
                                if home_pitcher_stats else 0, 2)
                        },
                        'game_yrfi_probability': None  # Se calculará después
                    },
                    'yrfi_probability': None
                },
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'data_source': 'season_data.json'
                }
            }
            
            # Calcular la probabilidad YRFI del partido
            home_adjusted = prediction['prediction']['calculation']['home_team']['adjusted']
            away_adjusted = prediction['prediction']['calculation']['away_team']['adjusted']
            yrfi_prob = round((1 - ((1 - home_adjusted / 100) * (1 - away_adjusted / 100))) * 100, 2)
            
            # Actualizar los campos de probabilidad
            prediction['prediction']['calculation']['game_yrfi_probability'] = yrfi_prob
            prediction['prediction']['yrfi_probability'] = yrfi_prob
            
            predictions.append(prediction)
            
            # Guardar predicción
            save_prediction(prediction)
            
            print(f"✅ Generado pronóstico para {away_team_name} @ {home_team_name} - Probabilidad YRFI: {yrfi_prob}%")
            
        except Exception as e:
            print(f"❌ Error al generar predicción para {game.get('away_team', {}).get('name', 'Desconocido')} @ {game.get('home_team', {}).get('name', 'Desconocido')}: {str(e)}")
    
    return predictions

def load_predictions_from_files(date_str: str = None) -> List[Dict]:
    """
    Carga las predicciones desde los archivos JSON generados.
    Busca archivos para la fecha especificada y el día siguiente para manejar partidos nocturnos.
    
    Args:
        date_str: Fecha en formato YYYY-MM-DD (opcional, usa la fecha actual si no se especifica)
        
    Returns:
        Lista de predicciones cargadas desde los archivos
    """
    from datetime import datetime, timedelta
    
    if date_str is None:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Obtener la fecha del día siguiente
    next_date_obj = date_obj + timedelta(days=1)
    
    predictions_dir = Path(__file__).parent.parent / 'predictions'
    predictions = []
    
    # Buscar archivos de predicción para ambas fechas
    date_str = date_obj.strftime("%Y-%m-%d")
    next_date_str = next_date_obj.strftime("%Y-%m-%d")
    
    # Patrones para buscar archivos de ambas fechas
    patterns = [
        f"yrfi_{date_str}_*_at_*.json",
        f"yrfi_{next_date_str}_*_at_*.json"
    ]
    
    # Encontrar archivos que coincidan con cualquiera de los patrones
    prediction_files = []
    for pattern in patterns:
        prediction_files.extend(list(predictions_dir.glob(pattern)))
    
    # Eliminar duplicados (por si acaso)
    prediction_files = list(set(prediction_files))
    
    if not prediction_files:
        print(f"No se encontraron archivos de predicción para las fechas {date_str} o {next_date_str}")
        return []
    
    print(f"\n📂 Archivos encontrados para procesar (fechas {date_str} y {next_date_str}):")
    for i, file_path in enumerate(sorted(prediction_files), 1):
        print(f"  {i}. {file_path.name}")
    
    # Cargar cada archivo de predicción
    for file_path in prediction_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                prediction = json.load(f)
                # Incluir partidos de la fecha objetivo y del día siguiente
                game_date = prediction.get('game_date', '')
                if game_date.startswith(date_str) or game_date.startswith(next_date_str):
                    predictions.append(prediction)
                    print(f"✅ Cargado: {file_path.name} (fecha partido: {game_date})")
                else:
                    print(f"⏩ Omitido (fecha {game_date}): {file_path.name}")
        except Exception as e:
            print(f"❌ Error al cargar el archivo {file_path}: {str(e)}")
    
    print(f"\n📊 Total de predicciones cargadas: {len(predictions)}")
    return predictions

def extract_team_info(prediction: dict, team_type: str) -> dict:
    """
    Extrae la información relevante de un equipo desde la predicción.
    
    Args:
        prediction: Diccionario con los datos de la predicción
        team_type: 'home_team' o 'away_team'
        
    Returns:
        Diccionario con la información del equipo
    """
    team = prediction[team_type]
    rival_type = 'away_team' if team_type == 'home_team' else 'home_team'
    rival = prediction[rival_type]
    
    return {
        'name': team['name'],
        'type': 'Local' if team_type == 'home_team' else 'Visitante',
        'yrfi_pct': team['yrfi_pct'],
        'pitcher': team['pitcher'],
        'rival_pitcher': rival['pitcher'],
        'rival_yrfi_pct': rival.get('yrfi_pct_against', 0)  # Porcentaje de YRFI permitido por el lanzador
    }

def extract_team_details(prediction: dict, team_type: str) -> dict:
    """
    Extrae los detalles completos de un equipo desde la predicción.
    """
    team = prediction[team_type]
    rival_type = 'away_team' if team_type == 'home_team' else 'home_team'
    rival = prediction[rival_type]
    
    # Obtener los valores directamente de los campos estructurados
    base_pct = team.get('yrfi_pct', 0)
    base_ratio = f"{team.get('yrfi_count', 0)}/{team.get('games_played', 1)}"
    
    # Calcular tendencia (últimos 15 partidos)
    tendencia_yrfi = team.get('last_15_yrfi', 0)
    tendencia_total = min(15, team.get('games_played', 0))  # No más que el total de partidos
    tendencia_pct = (tendencia_yrfi / tendencia_total * 100) if tendencia_total > 0 else 0
    tendencia_ratio = f"{tendencia_yrfi}/{tendencia_total}"
    
    # Obtener estadísticas del lanzador rival
    lanzador_rival = rival.get('pitcher', {})
    lanzador_pct = lanzador_rival.get('yrfi_pct', 0)
    lanzador_ratio = f"{lanzador_rival.get('yrfi_count', 0)}/{lanzador_rival.get('games_started', 1)}"
    
    # Calcular valores combinados
    combinado_calc = (base_pct * 0.45) + (tendencia_pct * 0.55)
    ajuste_calc = (combinado_calc * 0.65) + (lanzador_pct * 0.35)
    
    # Obtener el porcentaje ajustado final
    adjusted_pct = team.get('adjusted_yrfi_pct', 0)
    final_pct = adjusted_pct if adjusted_pct > 0 else ajuste_calc
    
    # Determinar si es local o visitante
    es_local = team_type == 'home_team'
    equipo_tipo = 'Local' if es_local else 'Visitante'
    
    # Obtener rendimiento del lanzador rival directamente del JSON
    lanzador_key = 'away_pitcher' if es_local else 'home_pitcher'
    lanzador_pct = prediction.get(lanzador_key, {}).get('yrfi_allowed', 0)
    lanzador_ratio = prediction.get(lanzador_key, {}).get('yrfi_ratio', '0/0')
    
    # Extraer el valor 'adjusted' del JSON
    adjusted_pct = 0.0
    if 'prediction' in prediction and 'calculation' in prediction['prediction']:
        team_key = 'home_team' if team_type == 'home_team' else 'away_team'
        if team_key in prediction['prediction']['calculation'] and 'adjusted' in prediction['prediction']['calculation'][team_key]:
            adjusted_pct = prediction['prediction']['calculation'][team_key]['adjusted']
    
    # Obtener los ratios de base y tendencia directamente del JSON
    base_ratio = team.get('stats', {}).get('base', {}).get('ratio', '0/0')
    tendencia_ratio = team.get('stats', {}).get('tendency', {}).get('ratio', '0/15')
    
    return {
        'name': team['name'],
        'type': equipo_tipo,
        'base_pct': base_pct,
        'base_ratio': base_ratio,  # Agregar ratio base
        'tendencia_pct': tendencia_pct,
        'tendencia_ratio': tendencia_ratio,  # Agregar ratio de tendencia
        'lanzador_rival': rival['pitcher'],
        'lanzador_rival_pct': lanzador_pct,
        'combinado_calc': combinado_calc,
        'ajuste_calc': ajuste_calc,
        'adjusted_pct': adjusted_pct,
        'final_pct': final_pct or base_pct  # Usar base_pct si final_pct es 0
    }

def main():
    """Función principal."""
    print("⚾ Obteniendo partidos de hoy...")
    games = get_next_day_games()
    
    # Mostrar información de depuración
    print("\n🔍 DEPURACIÓN: Partidos obtenidos de la API")
    print(f"Total de partidos: {len(games)}")
    print("-" * 80)
    
    for i, game in enumerate(games, 1):
        home_team = game['home_team']['name']
        away_team = game['away_team']['name']
        home_pitcher = game['pitchers'].get('home', {}).get('name', 'No definido')
        away_pitcher = game['pitchers'].get('away', {}).get('name', 'No definido')
        home_pitcher_id = game['pitchers'].get('home', {}).get('id', 'N/A')
        away_pitcher_id = game['pitchers'].get('away', {}).get('id', 'N/A')
        
        print(f"{i}. {away_team} @ {home_team}")
        print(f"   Lanzadores: {away_pitcher} (ID: {away_pitcher_id}) vs {home_pitcher} (ID: {home_pitcher_id})")
    
    print("\n" + "="*80)
    print("🔍 DEPURACIÓN: Datos obtenidos, continuando con el procesamiento...")
    print("="*80 + "\n")
    
    if not games:
        print("No se encontraron partidos para hoy.")
        return
    
    print(f"\n📅 Partidos encontrados: {len(games)}")
    for i, game in enumerate(games, 1):
        home = game['home_team']['name']
        away = game['away_team']['name']
        home_pitcher = game['pitchers'].get('home', {}).get('name', 'Por definir')
        away_pitcher = game['pitchers'].get('away', {}).get('name', 'Por definir')
        
        print(f"{i}. {away} @ {home}")
        print(f"   Lanzadores: {away_pitcher} vs {home_pitcher}\n")
    
    print("\n🔍 Generando pronósticos YRFI...\n")
    predictions = generate_predictions_for_games(games)
    
    if predictions:
        # Guardar las predicciones (esto generará los archivos individuales)
        for pred in predictions:
            save_prediction(pred)
        
        print("\n✨ ¡Proceso completado! Se han generado los archivos JSON individuales.")
    else:
        print("No se generaron predicciones.")

def generate_summary_markdown(prediction: Dict, output_dir: Path = None) -> str:
    """
    Genera un archivo de resumen en formato Markdown con la explicación de los cálculos.
    
    Args:
        prediction: Diccionario con los datos de la predicción
        output_dir: Directorio donde se guardará el archivo (opcional)
        
    Returns:
        Ruta al archivo generado
    """
    # Obtener información básica del partido
    game_date = prediction.get('game_date', '')
    home_team = prediction.get('home_team', {})
    away_team = prediction.get('away_team', {})
    prediction_data = prediction.get('prediction', {})
    calculation = prediction_data.get('calculation', {})
    
    # Obtener nombres de equipos y lanzadores
    home_team_name = home_team.get('name', 'Equipo Local')
    away_team_name = away_team.get('name', 'Equipo Visitante')
    home_pitcher = home_team.get('pitcher', {}).get('name', 'Por definir')
    away_pitcher = away_team.get('pitcher', {}).get('name', 'Por definir')
    
    # Obtener estadísticas de cálculo
    home_calc = calculation.get('home_team', {})
    away_calc = calculation.get('away_team', {})
    
    # Formatear la fecha para el nombre del archivo
    if game_date:
        game_date_obj = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
        date_str = game_date_obj.strftime('%Y-%m-%d')
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Crear el contenido del archivo Markdown
    markdown_content = f"# Análisis YRFI: {away_team_name} @ {home_team_name}\n\n"
    markdown_content += f"**Fecha:** {date_str}  \n"
    markdown_content += f"**Lanzadores:** {away_pitcher} (V) vs {home_pitcher} (L)\n\n"
    
    # Sección de probabilidad general
    markdown_content += "## 📊 Probabilidad YRFI del Partido\n\n"
    markdown_content += f"**Probabilidad de que anoten en la primera entrada:** {prediction_data.get('yrfi_probability', 0):.1f}%\n\n"
    
    # Explicación del cálculo
    markdown_content += "## 🔍 Explicación de los Cálculos\n\n"
    
    # Explicación para el equipo local
    markdown_content += f"### {home_team_name} (Local)\n"
    markdown_content += f"- **Estadística base YRFI:** {home_team.get('stats', {}).get('base', {}).get('value', 0):.1f}% ({home_team.get('stats', {}).get('base', {}).get('ratio', '0/0')} partidos)\n"
    markdown_content += f"- **Tendencia reciente (últimos 15 partidos):** {home_team.get('stats', {}).get('tendency', {}).get('value', 0):.1f}% ({home_team.get('stats', {}).get('tendency', {}).get('ratio', '0/0')} partidos)\n"
    markdown_content += f"- **Impacto del lanzador visitante ({away_team_name} - {away_pitcher}):** {home_calc.get('pitcher_impact', 0):.1f}% ({away_team.get('pitcher', {}).get('yrfi_ratio', '0/0')} partidos)\n"
    markdown_content += f"- **Puntuación ajustada:** {home_calc.get('adjusted', 0):.1f}%\n\n"
    
    # Explicación para el equipo visitante
    markdown_content += f"### {away_team_name} (Visitante)\n"
    markdown_content += f"- **Estadística base YRFI:** {away_team.get('stats', {}).get('base', {}).get('value', 0):.1f}% ({away_team.get('stats', {}).get('base', {}).get('ratio', '0/0')} partidos)\n"
    markdown_content += f"- **Tendencia reciente (últimos 15 partidos):** {away_team.get('stats', {}).get('tendency', {}).get('value', 0):.1f}% ({away_team.get('stats', {}).get('tendency', {}).get('ratio', '0/0')} partidos)\n"
    markdown_content += f"- **Impacto del lanzador local ({home_team_name} - {home_pitcher}):** {away_calc.get('pitcher_impact', 0):.1f}% ({home_team.get('pitcher', {}).get('yrfi_ratio', '0/0')} partidos)\n"
    markdown_content += f"- **Puntuación ajustada:** {away_calc.get('adjusted', 0):.1f}%\n\n"
    
    # Fórmula de cálculo
    markdown_content += "### 📝 Fórmula de Cálculo\n\n"
    markdown_content += "La probabilidad final de que anoten en la primera entrada se calcula en tres pasos:\n\n"
    markdown_content += "1. **Puntuación combinada** para cada equipo (45% estadística base + 55% tendencia reciente):\n"
    markdown_content += "   - `Puntuación = (0.45 × Estadística Base) + (0.55 × Tendencia Reciente)`\n\n"
    markdown_content += "2. **Ajuste por lanzador** (65% puntuación combinada + 35% impacto del lanzador contrario):\n"
    markdown_content += "   - `Puntuación Ajustada = (0.65 × Puntuación) + (0.35 × Rendimiento Lanzador Rival)`\n\n"
    markdown_content += "3. **Probabilidad final** considerando ambos equipos como eventos independientes:\n"
    markdown_content += "   - `Probabilidad Final = 1 - ((1 - P_local) × (1 - P_visitante))`\n"
    markdown_content += "   - Donde P_local y P_visitante son las probabilidades ajustadas convertidas a decimal (0-1)\n\n"
    
    # Detalles adicionales
    markdown_content += "### 📌 Notas Adicionales\n\n"
    markdown_content += f"- **Generado el:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    markdown_content += f"- **Fuente de datos:** {prediction.get('metadata', {}).get('data_source', '')}\n"
    
    # Determinar el directorio de salida
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'predictions'
    
    # Crear el directorio si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre del archivo con el mismo formato que los JSON pero con extensión .md
    home_team = prediction.get('home_team', {}).get('name', 'Home')
    away_team = prediction.get('away_team', {}).get('name', 'Away')
    game_date = prediction.get('game_date', datetime.now().strftime('%Y-%m-%d'))
    game_pk = prediction.get('game_pk', '')
    
    safe_home = "".join([c if c.isalnum() else "_" for c in home_team])
    safe_away = "".join([c if c.isalnum() else "_" for c in away_team])
    
    filename = f"yrfi_{game_date}_{safe_away}_at_{safe_home}_{game_pk}.md"
    filepath = output_dir / filename
    
    # Guardar el archivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return str(filepath)

def save_prediction(prediction: Dict, output_dir: Path = None) -> str:
    """
    Guarda la predicción en un archivo JSON y genera un resumen en Markdown.
    
    Args:
        prediction: Diccionario con los datos de la predicción
        output_dir: Directorio de salida (opcional)
        
    Returns:
        Ruta al archivo guardado
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'predictions'
    
    # Crear el directorio si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre del archivo
    home_team = prediction.get('home_team', {}).get('name', 'Home')
    away_team = prediction.get('away_team', {}).get('name', 'Away')
    game_date = prediction.get('game_date', datetime.now().strftime('%Y-%m-%d'))
    game_pk = prediction.get('game_pk', '')
    
    safe_home = "".join([c if c.isalnum() else "_" for c in home_team])
    safe_away = "".join([c if c.isalnum() else "_" for c in away_team])
    
    filename = f"yrfi_{game_date}_{safe_away}_at_{safe_home}_{game_pk}.json"
    filepath = output_dir / filename
    
    # Guardar el archivo JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(prediction, f, indent=2, ensure_ascii=False)
    
    # Generar el resumen en Markdown
    try:
        generate_summary_markdown(prediction, output_dir)
    except Exception as e:
        print(f"⚠️  No se pudo generar el resumen Markdown: {str(e)}")
    
    return str(filepath)

def generate_global_summary(predictions: List[Dict], output_dir: Path = None) -> str:
    """
    Genera un resumen global en formato Markdown con estadísticas YRFI de todos los partidos.
    
    Args:
        predictions: Lista de predicciones de partidos
        output_dir: Directorio donde se guardará el archivo (opcional)
        
    Returns:
        Ruta al archivo generado
    """
    if not predictions:
        return ""
    
    # Obtener la fecha del primer partido como fecha de referencia
    game_date = predictions[0].get('game_date', datetime.now().strftime('%Y-%m-%d'))
    
    # Preparar listas para las estadísticas
    teams_stats = []
    games_stats = []
    
    # Procesar cada predicción
    for pred in predictions:
        home_team = pred.get('home_team', {})
        away_team = pred.get('away_team', {})
        pred_data = pred.get('prediction', {})
        calc = pred_data.get('calculation', {})
        
        # Estadísticas del equipo local
        home_stats = {
            'name': home_team.get('name', 'Equipo Local'),
            'is_home': True,
            'opponent': away_team.get('name', 'Equipo Visitante'),
            'opponent_pitcher': away_team.get('pitcher', {}).get('name', 'Por definir'),
            'base_yrfi': home_team.get('stats', {}).get('base', {}).get('value', 0),
            'tendency': home_team.get('stats', {}).get('tendency', {}).get('value', 0),
            'pitcher_impact': calc.get('home_team', {}).get('pitcher_impact', 0),
            'adjusted': calc.get('home_team', {}).get('adjusted', 0),
            'game_yrfi': pred_data.get('yrfi_probability', 0)
        }
        
        # Estadísticas del equipo visitante
        away_stats = {
            'name': away_team.get('name', 'Equipo Visitante'),
            'is_home': False,
            'opponent': home_team.get('name', 'Equipo Local'),
            'opponent_pitcher': home_team.get('pitcher', {}).get('name', 'Por definir'),
            'base_yrfi': away_team.get('stats', {}).get('base', {}).get('value', 0),
            'tendency': away_team.get('stats', {}).get('tendency', {}).get('value', 0),
            'pitcher_impact': calc.get('away_team', {}).get('pitcher_impact', 0),
            'adjusted': calc.get('away_team', {}).get('adjusted', 0),
            'game_yrfi': pred_data.get('yrfi_probability', 0)
        }
        
        # Estadísticas del partido
        game_stats = {
            'home_team': home_team.get('name', 'Equipo Local'),
            'away_team': away_team.get('name', 'Equipo Visitante'),
            'home_pitcher': home_team.get('pitcher', {}).get('name', 'Por definir'),
            'away_pitcher': away_team.get('pitcher', {}).get('name', 'Por definir'),
            'yrfi_probability': pred_data.get('yrfi_probability', 0),
            'home_adjusted': calc.get('home_team', {}).get('adjusted', 0),
            'away_adjusted': calc.get('away_team', {}).get('adjusted', 0)
        }
        
        teams_stats.extend([home_stats, away_stats])
        games_stats.append(game_stats)
    
    # Ordenar equipos por YRFI ajustado (de mayor a menor)
    teams_sorted = sorted(teams_stats, key=lambda x: x['adjusted'], reverse=True)
    
    # Ordenar partidos por probabilidad YRFI (de mayor a menor)
    games_sorted = sorted(games_stats, key=lambda x: x['yrfi_probability'], reverse=True)
    
    # Determinar el directorio de salida
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'predictions'
    
    # Crear el directorio si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre del archivo
    filename = f"yrfi_global_summary_{game_date}.md"
    filepath = output_dir / filename
    
    # Crear el contenido del archivo Markdown
    content = f"# 📊 Resumen Global YRFI - {game_date}\n\n"
    
    # Sección de equipos con mayor YRFI
    content += "## 🏆 Top 3 Equipos con Mayor Probabilidad YRFI\n\n"
    
    for i, team in enumerate(teams_sorted[:3], 1):
        local_visitante = "(Local 🏠)" if team['is_home'] else "(Visitante ✈️)"
        content += f"{i}. **{team['name']}** {local_visitante}\n"
        content += f"   - **Oponente:** {team['opponent']}\n"
        content += f"   - **Lanzador Rival:** {team['opponent_pitcher']}\n"
        content += f"   - **YRFI Ajustado:** {team['adjusted']:.1f}%\n\n"
    
    # Sección de partidos con mayor YRFI
    content += "## 🎯 Top 2 Partidos con Mayor Probabilidad YRFI\n\n"
    
    for i, game in enumerate(games_sorted[:2], 1):
        content += f"{i}. **{game['away_team']} @ {game['home_team']}**\n"
        content += f"   - **Lanzadores:** {game['away_pitcher']} vs {game['home_pitcher']}\n"
        content += f"   - **Probabilidad YRFI:** {game['yrfi_probability']:.1f}%\n"
        content += f"   - **Prob. Equipos:** {game['away_adjusted']:.1f}% vs {game['home_adjusted']:.1f}%\n\n"
    
    # Sección de equipos con menor YRFI
    content += "## 📉 Top 3 Equipos con Menor Probabilidad YRFI\n\n"
    
    for i, team in enumerate(teams_sorted[-3:][::-1], 1):
        local_visitante = "(Local 🏠)" if team['is_home'] else "(Visitante ✈️)"
        content += f"{i}. **{team['name']}** {local_visitante}\n"
        content += f"   - **Oponente:** {team['opponent']}\n"
        content += f"   - **Lanzador Rival:** {team['opponent_pitcher']}\n"
        content += f"   - **YRFI Ajustado:** {team['adjusted']:.1f}%\n\n"
    
    # Sección de partidos con menor YRFI
    content += "## 🛑 Top 2 Partidos con Menor Probabilidad YRFI\n\n"
    
    for i, game in enumerate(games_sorted[-2:][::-1], 1):
        content += f"{i}. **{game['away_team']} @ {game['home_team']}**\n"
        content += f"   - **Lanzadores:** {game['away_pitcher']} vs {game['home_pitcher']}\n"
        content += f"   - **Probabilidad YRFI:** {game['yrfi_probability']:.1f}%\n"
        content += f"   - **Prob. Equipos:** {game['away_adjusted']:.1f}% vs {game['home_adjusted']:.1f}%\n\n"
    
    # Estadísticas adicionales
    content += "## 📈 Estadísticas Adicionales\n\n"
    content += f"- **Total de partidos analizados:** {len(predictions)}\n"
    content += f"- **Promedio de probabilidad YRFI:** {sum(g['yrfi_probability'] for g in games_stats) / len(games_stats):.1f}%\n"
    content += f"- **Partido con mayor probabilidad YRFI:** {games_sorted[0]['away_team']} @ {games_sorted[0]['home_team']} ({games_sorted[0]['yrfi_probability']:.1f}%)\n"
    content += f"- **Partido con menor probabilidad YRFI:** {games_sorted[-1]['away_team']} @ {games_sorted[-1]['home_team']} ({games_sorted[-1]['yrfi_probability']:.1f}%)\n"
    
    # Notas finales
    content += "\n## 📝 Notas\n\n"
    content += "- 🏠 Indica que el equipo juega de local\n"
    content += "- ✈️ Indica que el equipo juega de visitante\n"
    # Agregar información sobre los cálculos
    content += "\n### ℹ️ Sobre los Cálculos\n"
    content += "- Las probabilidades YRFI se calculan considerando el rendimiento reciente de los equipos y los lanzadores.\n"
    content += "- El YRFI Ajustado incluye el impacto del lanzador contrario y el rendimiento reciente del equipo.\n"
    content += "- La probabilidad del partido combina las estadísticas de ambos equipos.\n"
    
    content += f"\n*Resumen generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    # Guardar el archivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(filepath)

def main():
    """Función principal."""
    print("⚾ Obteniendo partidos de hoy...")
    
    # Obtener partidos programados para hoy
    games = get_next_day_games()
    
    if not games:
        print("No hay partidos programados para hoy.")
        return
    
    print(f"\n📅 Se encontraron {len(games)} partidos programados para hoy:")
    for i, game in enumerate(games, 1):
        print(f"   {i}. {game['away_team']['name']} @ {game['home_team']['name']}")
    
    # Cargar datos de la temporada
    print("\n📊 Cargando datos de la temporada...")
    season_data_file = Path(__file__).parent.parent / 'data' / 'season_data.json'
    season_data = load_season_data(season_data_file)
    
    if not season_data:
        print("No se pudieron cargar los datos de la temporada.")
        return
    
    # Generar predicciones
    print("\n🎯 Generando predicciones YRFI...")
    predictions = generate_predictions_for_games(games, season_data)
    
    if predictions:
        print(f"\n✨ ¡Proceso completado! Se han generado {len(predictions)} predicciones.")
        
        # Generar resumen global
        try:
            summary_path = generate_global_summary(predictions)
            print(f"📊 Se ha generado el resumen global: {summary_path}")
        except Exception as e:
            print(f"⚠️  No se pudo generar el resumen global: {str(e)}")
    else:
        print("No se generaron predicciones.")

if __name__ == "__main__":
    main()
