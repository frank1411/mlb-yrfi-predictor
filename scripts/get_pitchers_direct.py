#!/usr/bin/env python3
"""
Script para obtener los lanzadores probables de los partidos de hoy
usando diferentes métodos de la API de MLB.
"""
import sys
import os
from datetime import datetime
import requests

# Añadir el directorio raíz al path para poder importar src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_todays_games():
    """Obtiene los partidos de hoy usando el endpoint de schedule."""
    today = datetime.now().strftime('%m/%d/%Y')
    url = f"https://statsapi.mlb.com/api/v1/schedule"
    params = {
        'sportId': 1,  # MLB
        'date': today,
        'hydrate': 'probablePitcher,linescore,team'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'dates' in data and data['dates']:
            return data['dates'][0].get('games', [])
        return []
    except Exception as e:
        print(f"Error al obtener partidos: {e}")
        return []

def get_pitcher_stats(pitcher_id):
    """Obtiene estadísticas de un lanzador."""
    if not pitcher_id:
        return {}
        
    try:
        url = f"https://statsapi.mlb.com/api/v1/people/{pitcher_id}"
        params = {
            'hydrate': 'stats(group=[pitching],type=[season])'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al obtener estadísticas del lanzador {pitcher_id}: {e}")
        return {}

def main():
    """Función principal."""
    print("=== LANZADORES PROBABLES DE HOY (" + datetime.now().strftime('%Y-%m-%d') + ") ===\n")
    
    games = get_todays_games()
    
    if not games:
        print("No se encontraron partidos para hoy.")
        return
    
    for game in games:
        try:
            game_date = game.get('gameDate', '').replace('T', ' ').replace('Z', ' UTC')
            home_team = game.get('teams', {}).get('home', {}).get('team', {}).get('name', 'Desconocido')
            away_team = game.get('teams', {}).get('away', {}).get('team', {}).get('name', 'Desconocido')
            
            # Intentar obtener lanzadores probables
            home_pitcher = game.get('teams', {}).get('home', {}).get('probablePitcher', {})
            away_pitcher = game.get('teams', {}).get('away', {}).get('probablePitcher', {})
            
            # Si no están en probablePitcher, buscar en el boxscore
            if not home_pitcher or not away_pitcher:
                linescore = game.get('linescore', {})
                if not home_pitcher and 'home' in linescore.get('teams', {}):
                    home_pitcher = linescore['teams']['home'].get('probablePitcher', {})
                if not away_pitcher and 'away' in linescore.get('teams', {}):
                    away_pitcher = linescore['teams']['away'].get('probablePitcher', {})
            
            home_pitcher_name = home_pitcher.get('fullName', 'Por anunciar') if isinstance(home_pitcher, dict) else 'Por anunciar'
            away_pitcher_name = away_pitcher.get('fullName', 'Por anunciar') if isinstance(away_pitcher, dict) else 'Por anunciar'
            home_pitcher_id = home_pitcher.get('id') if isinstance(home_pitcher, dict) else None
            away_pitcher_id = away_pitcher.get('id') if isinstance(away_pitcher, dict) else None
            
            print(f"{away_team} @ {home_team}")
            print(f"Hora: {game_date}")
            print(f"Lanzador visitante: {away_pitcher_name} (ID: {away_pitcher_id or 'N/A'})")
            print(f"Lanzador local:     {home_pitcher_name} (ID: {home_pitcher_id or 'N/A'})")
            print("-" * 60)
            
        except Exception as e:
            print(f"Error al procesar partido: {e}")
            continue

if __name__ == "__main__":
    main()
