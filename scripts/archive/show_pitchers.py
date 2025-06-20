#!/usr/bin/env python3
"""
Script para mostrar los lanzadores anunciados para hoy.
"""
from datetime import datetime
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient

def get_todays_pitchers():
    """Obtiene y muestra los lanzadores anunciados para hoy."""
    client = MLBClient()
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"📅 Lanzadores anunciados para hoy ({today}):\n")
    
    try:
        # Obtener el calendario para hoy con lanzadores probables
        schedule = client.get_schedule(date=today, include_probables=True)
        
        if 'dates' in schedule and schedule['dates']:
            games = schedule['dates'][0].get('games', [])
            
            if not games:
                print("No hay partidos programados para hoy.")
                return
            
            for game in games:
                home_team = game['teams']['home']['team']['name']
                away_team = game['teams']['away']['team']['name']
                game_time = game.get('gameDate', 'Hora no disponible').split('T')[1][:5] + ' ET'
                
                # Obtener lanzadores probables
                home_pitcher = "No anunciado"
                away_pitcher = "No anunciado"
                
                if 'probablePitchers' in game:
                    for pitcher in game['probablePitchers']:
                        if pitcher['team']['id'] == game['teams']['home']['team']['id']:
                            home_pitcher = f"{pitcher['fullName']} ({pitcher.get('wins', '?')}-{pitcher.get('losses', '?')}, {pitcher.get('era', '?.??')} ERA)"
                        elif pitcher['team']['id'] == game['teams']['away']['team']['id']:
                            away_pitcher = f"{pitcher['fullName']} ({pitcher.get('wins', '?')}-{pitcher.get('losses', '?')}, {pitcher.get('era', '?.??')} ERA)"
                
                print(f"⚾ {away_team} @ {home_team}")
                print(f"   🕒 {game_time}")
                print(f"   🏠 Local: {home_pitcher}")
                print(f"   ✈️ Visitante: {away_pitcher}\n")
        else:
            print("No se encontraron partidos programados para hoy.")
    
    except Exception as e:
        print(f"Error al obtener los lanzadores: {str(e)}")

if __name__ == "__main__":
    get_todays_pitchers()