#!/usr/bin/env python3
"""
Script para mostrar los partidos programados para hoy y sus lanzadores anunciados.
"""
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Añadir el directorio raíz al path para poder importar src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mlb_client import MLBClient

def get_todays_games() -> List[Dict]:
    """Obtiene los partidos programados para hoy."""
    client = MLBClient()
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"Buscando partidos para la fecha: {today}")
    schedule = client.get_schedule(date=today)
    
    if 'dates' in schedule and schedule['dates']:
        games = schedule['dates'][0].get('games', [])
        print(f"Se encontraron {len(games)} partidos programados para hoy.")
        return games
    print("No se encontraron partidos programados para hoy.")
    return []

def get_probable_pitchers() -> List[Dict]:
    """Obtiene información de los partidos y lanzadores probables para hoy."""
    games = get_todays_games()
    games_info = []
    
    for game in games:
        try:
            game_id = game['gamePk']
            game_date = game.get('gameDate', 'Hora no disponible')
            home_team = game['teams']['home']['team'].get('name', 'Desconocido')
            away_team = game['teams']['away']['team'].get('name', 'Desconocido')
            
            # Intentar obtener lanzadores probables
            home_pitcher = game.get('teams', {}).get('home', {}).get('probablePitcher', {})
            away_pitcher = game.get('teams', {}).get('away', {}).get('probablePitcher', {})
            
            game_info = {
                'game_id': game_id,
                'game_time': game_date,
                'home_team': home_team,
                'away_team': away_team,
                'home_pitcher': home_pitcher.get('fullName', 'Por anunciar') if isinstance(home_pitcher, dict) else 'Por anunciar',
                'away_pitcher': away_pitcher.get('fullName', 'Por anunciar') if isinstance(away_pitcher, dict) else 'Por anunciar',
                'home_pitcher_id': home_pitcher.get('id') if isinstance(home_pitcher, dict) else None,
                'away_pitcher_id': away_pitcher.get('id') if isinstance(away_pitcher, dict) else None,
                'status': game.get('status', {}).get('detailedState', 'Estado desconocido')
            }
            
            games_info.append(game_info)
            
        except Exception as e:
            print(f"Error al procesar partido: {e}")
    
    return games_info

def main():
    """Función principal que muestra los partidos y lanzadores de hoy."""
    print("=== PARTIDOS PROGRAMADOS PARA HOY ===\n")
    
    games_info = get_probable_pitchers()
    
    if not games_info:
        print("No se encontraron partidos programados para hoy.")
        return
    
    for game in games_info:
        print(f"{game['away_team']} @ {game['home_team']}")
        print(f"Hora: {game['game_time']}")
        print(f"Estado: {game['status']}")
        print(f"Lanzador visitante: {game['away_pitcher']}")
        print(f"Lanzador local:     {game['home_pitcher']}")
        print(f"ID del juego: {game['game_id']}")
        print("-" * 50)
        print()

if __name__ == "__main__":
    main()
