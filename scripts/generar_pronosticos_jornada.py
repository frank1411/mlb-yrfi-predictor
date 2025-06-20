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
            
            # Crear resultado
            prediction = {
                'game_date': game_date_str,
                'home_team': {
                    'id': home_team_id,
                    'name': home_team_name,
                    'pitcher': home_pitcher.get('name', 'Por definir'),
                    'yrfi_pct': game_data['home_team']['yrfi_pct']
                },
                'away_team': {
                    'id': away_team_id,
                    'name': away_team_name,
                    'pitcher': away_pitcher.get('name', 'Por definir'),
                    'yrfi_pct': game_data['away_team']['yrfi_pct']
                },
                'prediction': {
                    'base_prob': game_data['base_prob'],
                    'final_prob': game_data['final_prob'],
                    'text': prediction_text
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

def generate_summary(predictions: List[Dict[str, Any]]) -> str:
    """
    Genera un resumen de todas las predicciones.
    
    Args:
        predictions: Lista de predicciones.
        
    Returns:
        String con el resumen formateado.
    """
    if not predictions:
        return "No hay predicciones para mostrar."
    
    # Ordenar predicciones por probabilidad (de mayor a menor)
    sorted_predictions = sorted(predictions, 
                              key=lambda x: x['prediction']['final_prob'], 
                              reverse=True)
    
    # Generar resumen
    summary = ["# Resumen de Pronósticos YRFI\n"]
    summary.append(f"**Fecha:** {predictions[0]['game_date']}\n")
    summary.append("## Partidos con mayor probabilidad de YRFI\n")
    
    for i, pred in enumerate(sorted_predictions, 1):
        home = pred['home_team']
        away = pred['away_team']
        prob = pred['prediction']['final_prob'] * 100
        
        summary.append(
            f"{i}. **{away['name']}** @ **{home['name']}** - "
            f"**{prob:.1f}%** (Lanzadores: {away['pitcher']} vs {home['pitcher']})"
        )
    
    return "\n".join(summary)

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
        # Generar y guardar resumen
        summary = generate_summary(predictions)
        output_dir = Path(__file__).parent.parent / 'predictions'
        output_file = output_dir / f"resumen_yrfi_{predictions[0]['game_date']}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n✨ ¡Proceso completado! Resumen guardado en: {output_file}")
        print("\n" + "="*50)
        print(summary)
    else:
        print("No se generaron predicciones.")

if __name__ == "__main__":
    main()
