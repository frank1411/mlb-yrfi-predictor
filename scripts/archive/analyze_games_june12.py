#!/usr/bin/env python3
"""
Script para analizar los partidos del 12 de junio y generar predicciones YRFI.
"""
import json
from datetime import datetime
from pathlib import Path
import sys

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.data.data_manager import load_season_data
from src.yrfi_calculator import YRFICalculator

def get_games_by_date(season_data, target_date):
    """Obtiene los partidos de una fecha específica."""
    target_date_str = target_date.strftime('%Y-%m-%d')
    games = []
    
    for game in season_data.get('games', []):
        game_date = game.get('officialDate')
        if game_date == target_date_str and game.get('status', {}).get('abstractGameState') == 'Final':
            games.append(game)
    
    return games

def get_team_name(season_data, team_id):
    """Obtiene el nombre de un equipo por su ID."""
    team = season_data.get('teams', {}).get(str(team_id), {})
    return team.get('team', {}).get('name', f'Equipo {team_id}')

def analyze_games():
    """Analiza los partidos del 12 de junio y genera predicciones YRFI."""
    # Cargar datos de la temporada
    print("Cargando datos de la temporada...")
    season_data = load_season_data()
    
    # Obtener partidos del 11 de junio de 2025
    target_date = datetime(2025, 6, 11)
    games = get_games_by_date(season_data, target_date)
    
    if not games:
        print(f"No se encontraron partidos para la fecha {target_date.strftime('%Y-%m-%d')}")
        return
    
    print(f"\nAnalizando {len(games)} partidos del {target_date.strftime('%Y-%m-%d')}...\n")
    
    # Inicializar calculadora
    calculator = YRFICalculator(season_data, window_size=15)
    
    # Analizar cada partido
    for game in games:
        home_team = game.get('teams', {}).get('home', {}).get('team', {})
        away_team = game.get('teams', {}).get('away', {}).get('team', {})
        
        home_team_id = str(home_team.get('id'))
        away_team_id = str(away_team.get('id'))
        
        home_team_name = home_team.get('name', f'Equipo {home_team_id}')
        away_team_name = away_team.get('name', f'Equipo {away_team_id}')
        
        # Obtener IDs de lanzadores si están disponibles
        home_pitcher_id = None
        away_pitcher_id = None
        
        # Intentar obtener lanzadores del partido
        if 'probablePitcher' in game.get('teams', {}).get('home', {}):
            home_pitcher_id = str(game['teams']['home']['probablePitcher'].get('id'))
        if 'probablePitcher' in game.get('teams', {}).get('away', {}):
            away_pitcher_id = str(game['teams']['away']['probablePitcher'].get('id'))
        
        # Generar predicción
        try:
            prob, details = calculator.predict_yrfi_probability(
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                home_pitcher_id=home_pitcher_id,
                away_pitcher_id=away_pitcher_id,
                season_weight=0.6,
                recent_weight=0.4
            )
            
            # Obtener resultado real del partido
            home_runs_1st = 0
            away_runs_1st = 0
            yrfi_actual = False
            
            linescore = game.get('linescore', {})
            if linescore and 'innings' in linescore and len(linescore['innings']) > 0:
                for inning in linescore['innings']:
                    if inning.get('num') == 1:  # Primer inning
                        home_runs_1st = inning.get('home', {}).get('runs', 0)
                        away_runs_1st = inning.get('away', {}).get('runs', 0)
                        yrfi_actual = (home_runs_1st > 0) or (away_runs_1st > 0)
                        break
            
            # Mostrar resumen del partido
            print("=" * 80)
            print(f"PARTIDO: {away_team_name} @ {home_team_name}")
            print(f"PREDICCIÓN YRFI: {prob*100:.1f}%")
            print(f"RESULTADO REAL: {away_team_name} {away_runs_1st} - {home_team_name} {home_runs_1st}")
            print(f"YRFI REAL: {'SÍ' if yrfi_actual else 'NO'}")
            
            # Mostrar acierto/error
            prediction_correct = (prob > 0.5) == yrfi_actual
            print(f"PREDICCIÓN: {'ACERTADA' if prediction_correct else 'FALLIDA'}")
            
            # Mostrar estadísticas relevantes
            home_season = details['home_team']['season']['yrfi_pct']
            away_season = details['away_team']['season']['yrfi_pct']
            home_recent = details['home_team']['recent']['yrfi_pct']
            away_recent = details['away_team']['recent']['yrfi_pct']
            
            print(f"\nESTADÍSTICAS:")
            print(f"{home_team_name} - Temporada: {home_season*100:.1f}% | Recientes: {home_recent*100:.1f}%")
            print(f"{away_team_name} - Temporada: {away_season*100:.1f}% | Recientes: {away_recent*100:.1f}%")
            
            # Mostrar lanzadores si están disponibles
            if details['home_pitcher'] or details['away_pitcher']:
                print("\nLANZADORES:")
                if details['home_pitcher'] and details['home_pitcher']['starts_analyzed'] > 0:
                    p = details['home_pitcher']
                    print(f"  {p['name']} ({home_team_name}): {p['yrfi_pct']*100:.1f}% YRFI en {p['starts_analyzed']} aperturas")
                if details['away_pitcher'] and details['away_pitcher']['starts_analyzed'] > 0:
                    p = details['away_pitcher']
                    print(f"  {p['name']} ({away_team_name}): {p['yrfi_pct']*100:.1f}% YRFI en {p['starts_analyzed']} aperturas")
            
            print()
            
        except Exception as e:
            print(f"Error al analizar el partido {home_team_name} vs {away_team_name}: {e}")
            continue

if __name__ == "__main__":
    analyze_games()
