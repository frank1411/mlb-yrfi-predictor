#!/usr/bin/env python3
"""
Script temporal para verificar los lanzadores anunciados para los partidos de hoy.
"""
import sys
import os
from datetime import datetime
from pathlib import Path

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient

def get_todays_games():
    """Obtiene los partidos programados para hoy."""
    client = MLBClient()
    
    # Obtener la fecha de hoy en formato YYYY-MM-DD
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Parámetros para la API
    params = {
        'sportId': 1,  # MLB
        'date': today,
        'hydrate': 'probablePitcher,linescore,team,venue'
    }
    
    try:
        # Obtener el schedule para hoy
        schedule = client._make_request('schedule', params=params)
        
        # Verificar si hay partidos programados
        if 'dates' not in schedule or not schedule['dates']:
            print(f"No hay partidos programados para hoy ({today}).")
            return []
        
        # Obtener los juegos del día
        games = schedule['dates'][0]['games']
        return games
        
    except Exception as e:
        print(f"Error al obtener los partidos de hoy: {e}")
        return []

def format_pitcher_info(pitcher_data):
    """Formatea la información de un lanzador."""
    if not pitcher_data:
        return "No anunciado"
    
    full_name = pitcher_data.get('fullName', 'Desconocido')
    handedness = "Zurdo" if pitcher_data.get('pitchHand', {}).get('code') == 'L' else "Derecho"
    
    stats = pitcher_data.get('stats', [{}])[0].get('splits', [{}])[0].get('stat', {})
    era = stats.get('era', 'N/A')
    wins = stats.get('wins', 0)
    losses = stats.get('losses', 0)
    
    return f"{full_name} ({handedness}) - {wins}-{losses}, {era} ERA"

def main():
    """Función principal."""
    print("Obteniendo información de lanzadores para los partidos de hoy...\n")
    
    # Obtener los partidos de hoy
    games = get_todays_games()
    
    if not games:
        print("No se encontraron partidos para hoy.")
        return
    
    # Mostrar información de cada partido
    for game in games:
        home_team = game['teams']['home']['team']['name']
        away_team = game['teams']['away']['team']['name']
        game_time = game.get('gameDate', '').split('T')[1][:5] if 'gameDate' in game else 'Hora no disponible'
        
        home_pitcher = game['teams']['home'].get('probablePitcher', {})
        away_pitcher = game['teams']['away'].get('probablePitcher', {})
        
        print(f"{away_team} @ {home_team} - {game_time} ET")
        print(f"  Lanzador Visitante: {format_pitcher_info(away_pitcher)}")
        print(f"  Lanzador Local:     {format_pitcher_info(home_pitcher)}")
        print()

if __name__ == "__main__":
    main()
