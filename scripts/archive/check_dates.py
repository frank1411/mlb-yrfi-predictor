#!/usr/bin/env python3
"""
Script para verificar las fechas disponibles en los datos.
"""
import sys
from pathlib import Path
from datetime import datetime

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.data.data_manager import load_season_data

def list_available_dates():
    """Lista todas las fechas únicas de partidos en los datos."""
    season_data = load_season_data()
    dates = set()
    
    for game in season_data.get('games', []):
        game_date = game.get('officialDate')
        if game_date and game.get('status', {}).get('abstractGameState') == 'Final':
            dates.add(game_date)
    
    # Ordenar fechas
    sorted_dates = sorted(dates)
    
    print(f"Fechas disponibles ({len(sorted_dates)} en total):")
    for i, date in enumerate(sorted_dates, 1):
        print(f"{i}. {date}")
    
    return sorted_dates

if __name__ == "__main__":
    list_available_dates()
