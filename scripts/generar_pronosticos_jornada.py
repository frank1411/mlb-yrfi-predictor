#!/usr/bin/env python3
"""
Script para generar pronósticos YRFI para todos los partidos de la próxima jornada de MLB.
"""
import sys
import json
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

def generate_predictions_for_games(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Genera predicciones para una lista de partidos.
    
    Args:
        games: Lista de diccionarios con información de los partidos.
        
    Returns:
        Lista de predicciones generadas.
    """
    # Cargar datos de la temporada
    data_dir = Path(__file__).parent.parent / 'data'
    data_file = data_dir / 'season_data.json'
    season_data = load_season_data(data_file)
    
    predictions = []
    
    for game in games:
        try:
            # Obtener información del partido
            home_team_id = game['home_team']['id']
            away_team_id = game['away_team']['id']
            home_team_name = game['home_team']['name']
            away_team_name = game['away_team']['name']
            game_date = datetime.fromisoformat(game['game_date'].replace('Z', '+00:00'))
            game_date_str = game_date.strftime('%Y-%m-%d')
            
            # Obtener lanzadores
            home_pitcher = game['pitchers'].get('home', {})
            away_pitcher = game['pitchers'].get('away', {})
            
            # Si no hay lanzadores, saltar este partido
            if not home_pitcher or not away_pitcher:
                print(f"⚠️  No se encontraron lanzadores para {away_team_name} @ {home_team_name}")
                continue
            
            # Obtener estadísticas de los lanzadores
            home_pitcher_stats = get_pitcher_stats(season_data, 
                                                 pitcher_id=home_pitcher.get('id'),
                                                 pitcher_name=home_pitcher.get('name'))
            
            away_pitcher_stats = get_pitcher_stats(season_data,
                                                 pitcher_id=away_pitcher.get('id'),
                                                 pitcher_name=away_pitcher.get('name'))
            
            # Calcular probabilidades
            game_data = calculate_game_probability(
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                home_pitcher=home_pitcher_stats,
                away_pitcher=away_pitcher_stats,
                season_data=season_data
            )
            
            # Formatear predicción
            prediction_text = format_prediction(
                game_data, 
                home_team_name, 
                away_team_name, 
                game_date_str
            )
            
            # Crear resultado con la nueva estructura
            prediction = {
                'game_date': game_date_str,
                'home_team': {
                    'id': home_team_id,
                    'name': home_team_name,
                    'pitcher': {
                        'name': home_pitcher.get('name', 'Por definir'),
                        'yrfi_allowed': home_pitcher_stats.get('home_yrfi_pct', 0) if home_pitcher_stats else 0,
                        'yrfi_ratio': f"{home_pitcher_stats.get('home_yrfi', 0)}/{home_pitcher_stats.get('home_games', 1)}" if home_pitcher_stats else '0/1'
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
                        },
                        'adjusted_yrfi_pct': game_data['home_team'].get('adjusted_yrfi_pct', 0)
                    }
                },
                'away_team': {
                    'id': away_team_id,
                    'name': away_team_name,
                    'pitcher': {
                        'name': away_pitcher.get('name', 'Por definir'),
                        'yrfi_allowed': away_pitcher_stats.get('away_yrfi_pct', 0) if away_pitcher_stats else 0,
                        'yrfi_ratio': f"{away_pitcher_stats.get('away_yrfi', 0)}/{away_pitcher_stats.get('away_games', 1)}" if away_pitcher_stats else '0/1'
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
                        },
                        'adjusted_yrfi_pct': game_data['away_team'].get('adjusted_yrfi_pct', 0)
                    }
                },
                'prediction': {
                    'base_prob': game_data['base_prob'] * 100,  # Convertir a porcentaje
                    'final_prob': game_data['final_prob'] * 100,  # Convertir a porcentaje
                    'calculation': {
                        'formula': '((base × 0.6) + (tendency × 0.4)) × 0.7 + (opponent_pitcher_yrfi × 0.3)',
                        'home_team': {
                            'base': f"{game_data['home_team']['yrfi_pct']:.1f}% ({game_data['home_team'].get('yrfi', 0)}/{game_data['home_team'].get('games', 1)})",
                            'tendency': f"{(game_data['home_team'].get('last_15_yrfi', 0) / game_data['home_team'].get('last_15_games', 1)) * 100 if game_data['home_team'].get('last_15_games', 0) > 0 else 0:.1f}% ({game_data['home_team'].get('last_15_yrfi', 0)}/{game_data['home_team'].get('last_15_games', 1)})",
                            'pitcher': f"{away_pitcher.get('name', 'Por definir')} ({away_pitcher.get('away_yrfi_pct', 0):.1f}% YRFI permitido - {away_pitcher.get('away_yrfi', 0)}/{away_pitcher.get('away_games', 1)})"
                        },
                        'away_team': {
                            'base': f"{game_data['away_team']['yrfi_pct']:.1f}% ({game_data['away_team'].get('yrfi', 0)}/{game_data['away_team'].get('games', 1)})",
                            'tendency': f"{(game_data['away_team'].get('last_15_yrfi', 0) / game_data['away_team'].get('last_15_games', 1)) * 100 if game_data['away_team'].get('last_15_games', 0) > 0 else 0:.1f}% ({game_data['away_team'].get('last_15_yrfi', 0)}/{game_data['away_team'].get('last_15_games', 1)})",
                            'pitcher': f"{home_pitcher.get('name', 'Por definir')} ({home_pitcher.get('home_yrfi_pct', 0):.1f}% YRFI permitido - {home_pitcher.get('home_yrfi', 0)}/{home_pitcher.get('home_games', 1)})"
                        }
                    },
                    'text': prediction_text  # Mantener el texto original para compatibilidad
                },
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'data_source': str(data_file)
                }
            }
            
            predictions.append(prediction)
            
            # Guardar predicción
            save_prediction(prediction)
            
            print(f"✅ Generado pronóstico para {away_team_name} @ {home_team_name} - Probabilidad YRFI: {game_data['final_prob']*100:.1f}%")
            
        except Exception as e:
            print(f"❌ Error al generar predicción para {game.get('away_team', {}).get('name', 'Desconocido')} @ {game.get('home_team', {}).get('name', 'Desconocido')}: {str(e)}")
    
    return predictions

def load_predictions_from_files(date_str: str = None) -> List[Dict]:
    """
    Carga las predicciones desde los archivos JSON generados.
    
    Args:
        date_str: Fecha en formato YYYY-MM-DD (opcional, usa la fecha actual si no se especifica)
        
    Returns:
        Lista de predicciones cargadas desde los archivos
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    predictions_dir = Path(__file__).parent.parent / 'predictions'
    predictions = []
    
    # Buscar archivos de predicción para la fecha especificada
    pattern = f"yrfi_{date_str}_*_at_*.json"
    prediction_files = list(predictions_dir.glob(pattern))
    
    if not prediction_files:
        print(f"No se encontraron archivos de predicción para la fecha {date_str}")
        return []
    
    # Cargar cada archivo de predicción
    for file_path in prediction_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                prediction = json.load(f)
                predictions.append(prediction)
        except Exception as e:
            print(f"Error al cargar el archivo {file_path}: {str(e)}")
    
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
    pred_text = prediction['prediction']['text']
    
    # Inicializar valores por defecto
    base_pct = team.get('yrfi_pct', 0)
    tendencia_pct = 0
    lanzador_pct = 0
    combinado_calc = 0
    ajuste_calc = 0
    final_pct = 0
    
    # Extraer datos del texto usando patrones específicos
    import re
    
    # Determinar si es local o visitante
    es_local = team_type == 'home_team'
    equipo_tipo = 'Local' if es_local else 'Visitante'
    
    # Buscar la sección de probabilidad del equipo
    prob_pattern = (
        fr"Probabilidad YRFI del Equipo {'Local' if es_local else 'Visitante'}\n"
        fr"\*\*(\d+\.?\d*)%\*\* de que {re.escape(team['name'])} anote"
    )
    prob_match = re.search(prob_pattern, pred_text)
    if prob_match:
        final_pct = float(prob_match.group(1))
    
    # Extraer rendimiento base
    base_pattern = fr"Rendimiento de {re.escape(team['name'])} como {'local' if es_local else 'visitante'}: (\d+\.?\d*)%"
    base_match = re.search(base_pattern, pred_text)
    if base_match:
        base_pct = float(base_match.group(1))
    
    # Extraer tendencia reciente (últimos 15 partidos)
    tendencia_patterns = [
        fr"Tendencia \(Últimos 15 partidos\)\n- \*\*{re.escape(team['name'])}.*?(\d+\.?\d*)% \(\d+/15 partidos\)",
        fr"Tendencia \(Últimos 15 partidos\)\n.*?\n- \*\*{re.escape(team['name'])}.*?(\d+\.?\d*)% \(\d+/15 partidos\)",
        fr"Tendencia \(Últimos 15 partidos\)\n.*?\n.*?\n- \*\*{re.escape(team['name'])}.*?(\d+\.?\d*)% \(\d+/15 partidos\)"
    ]
    
    for pattern in tendencia_patterns:
        tendencia_match = re.search(pattern, pred_text, re.DOTALL)
        if tendencia_match:
            tendencia_pct = float(tendencia_match.group(1))
            break
    
    # Extraer rendimiento del lanzador rival
    lanzador_pattern = fr"Rendimiento del lanzador {'visitante' if es_local else 'local'}: (\d+\.?\d*)%"
    lanzador_match = re.search(lanzador_pattern, pred_text)
    if lanzador_match:
        lanzador_pct = float(lanzador_match.group(1))
    
    # Extraer cálculos intermedios
    calculo_section_pattern = (
        fr"{re.escape(team['name'])} \(\w+\):"
        fr".*?Combinado \(equipo \+ tendencia\): (\d+\.?\d*)%"
        fr".*?Ajuste \(70% equipo \+ 30% lanzador rival\): (\d+\.?\d*)%"
    )
    calculo_match = re.search(calculo_section_pattern, pred_text, re.DOTALL)
    if calculo_match:
        combinado_calc = float(calculo_match.group(1))
        ajuste_calc = float(calculo_match.group(2))
    
    return {
        'name': team['name'],
        'type': equipo_tipo,
        'base_pct': base_pct,
        'tendencia_pct': tendencia_pct,
        'lanzador_rival': rival['pitcher'],
        'lanzador_rival_pct': lanzador_pct,
        'combinado_calc': combinado_calc,
        'ajuste_calc': ajuste_calc,
        'final_pct': final_pct or base_pct  # Usar base_pct si final_pct es 0
    }

def generate_summary_from_files(date_str: str = None) -> str:
    """
    Genera un resumen detallado de todas las predicciones a partir de los archivos generados.
    """
    # Cargar predicciones desde archivos
    predictions = load_predictions_from_files(date_str)
    
    if not predictions:
        return "No hay predicciones para mostrar."
    
    # Procesar todos los equipos y partidos
    all_teams = []
    all_games = []
    
    for pred in predictions:
        # Extraer detalles de equipos
        home_team = extract_team_details(pred, 'home_team')
        away_team = extract_team_details(pred, 'away_team')
        
        # Agregar equipos a la lista
        all_teams.extend([home_team, away_team])
        
        # Agregar información del partido
        game_info = {
            'home_team': home_team['name'],
            'away_team': away_team['name'],
            'home_prob': home_team['final_pct'],
            'away_prob': away_team['final_pct'],
            'final_prob': (home_team['final_pct'] + away_team['final_pct']) / 2,
            'home_pitcher': home_team['lanzador_rival'],  # El lanzador es el del equipo rival
            'away_pitcher': away_team['lanzador_rival']   # El lanzador es el del equipo rival
        }
        all_games.append(game_info)
    
    # Ordenar equipos por probabilidad final (de mayor a menor)
    all_teams_sorted = sorted(all_teams, key=lambda x: x['final_pct'], reverse=True)
    
    # Ordenar partidos por probabilidad final (de mayor a menor)
    all_games_sorted = sorted(all_games, key=lambda x: x['final_prob'], reverse=True)
    
    # Generar el resumen en formato Markdown
    summary = []
    
    # Encabezado
    game_date = predictions[0]['game_date'] if predictions else datetime.now().strftime('%Y-%m-%d')
    summary.append(f"# 🏆 Análisis YRFI - {game_date}\n")
    summary.append(f"**Total de partidos analizados:** {len(all_games)}\n")
    
    # Top 3 equipos con mayor probabilidad YRFI
    summary.append("## 🔝 Top 3 Equipos con Mayor Probabilidad YRFI")
    for i, team in enumerate(all_teams_sorted[:3], 1):
        summary.append(
            f"{i}. **{team['name']} ({team['type']}) - {team['final_pct']:.1f}%\n"
            f"   • Base como {team['type']}: {team['base_pct']:.1f}%\n"
            f"   • Tendencia Reciente: {team['tendencia_pct']:.1f}%\n"
            f"   • Lanzador Rival: {team['lanzador_rival']['name']} ({team['lanzador_rival_pct']:.1f}% YRFI permitido - {team['lanzador_rival']['yrfi_ratio']})\n"
            f"   • Cálculo:\n"
            f"     • Combinado: {team['combinado_calc']:.1f}%\n"
            f"     • Ajuste: {team['ajuste_calc']:.1f}%"
        )
    
    # Top 2 partidos con mayor probabilidad YRFI
    summary.append("\n## 🏆 Top 2 Partidos con Mayor Probabilidad YRFI")
    for i, game in enumerate(all_games_sorted[:2], 1):
        summary.append(
            f"{i}. **{game['away_team']} @ {game['home_team']} - {game['final_prob']:.1f}%\n"
            f"   • {game['away_team']} (Visitante): {game['away_prob']:.1f}% (vs {game['away_pitcher']['name']} - {game['away_pitcher']['yrfi_ratio']} YRFI)\n"
            f"   • {game['home_team']} (Local): {game['home_prob']:.1f}% (vs {game['home_pitcher']['name']} - {game['home_pitcher']['yrfi_ratio']} YRFI)"
        )
    
    # Top 3 equipos con menor probabilidad YRFI
    summary.append("\n## 📉 Top 3 Equipos con Menor Probabilidad YRFI")
    for i, team in enumerate(all_teams_sorted[-3:], 1):
        summary.append(
            f"{i}. **{team['name']} ({team['type']}) - {team['final_pct']:.1f}%\n"
            f"   • Base como {team['type']}: {team['base_pct']:.1f}%\n"
            f"   • Tendencia Reciente: {team['tendencia_pct']:.1f}%\n"
            f"   • Lanzador Rival: {team['lanzador_rival']['name']} ({team['lanzador_rival_pct']:.1f}% YRFI permitido - {team['lanzador_rival']['yrfi_ratio']})"
        )
    
    # Top 2 partidos con menor probabilidad YRFI
    summary.append("\n## 🚫 Top 2 Partidos con Menor Probabilidad YRFI")
    for i, game in enumerate(all_games_sorted[-2:], 1):
        summary.append(
            f"{i}. **{game['away_team']} @ {game['home_team']} - {game['final_prob']:.1f}%\n"
            f"   • {game['away_team']} (Visitante): {game['away_prob']:.1f}% (vs {game['away_pitcher']['name']} - {game['away_pitcher']['yrfi_ratio']} YRFI)\n"
            f"   • {game['home_team']} (Local): {game['home_prob']:.1f}% (vs {game['home_pitcher']['name']} - {game['home_pitcher']['yrfi_ratio']} YRFI)"
        )
    
    # Nota final
    summary.append(
        "\n*Nota: Los porcentajes mostrados son las probabilidades calculadas "
        "basadas en el rendimiento histórico de los equipos y lanzadores. "
        "Los cálculos detallados están disponibles en los archivos individuales de cada partido.*"
    )
    
    return '\n'.join(summary)

def main():
    """Función principal."""
    print("⚾ Obteniendo partidos de hoy...")
    games = get_next_day_games()
    
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
        
        # Generar y guardar resumen a partir de los archivos generados
        output_dir = Path(__file__).parent.parent / 'predictions'
        game_date = predictions[0]['game_date'] if predictions else datetime.now().strftime("%Y-%m-%d")
        summary = generate_summary_from_files(game_date)
        
        output_file = output_dir / f"resumen_yrfi_{game_date}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n✨ ¡Proceso completado! Resumen guardado en: {output_file}")
        print("\n" + "="*50)
        print(summary)
    else:
        print("No se generaron predicciones.")

if __name__ == "__main__":
    main()
