#!/usr/bin/env python3
"""
Script para regenerar completamente los datos de la temporada.
Este script descarga todos los partidos de la temporada actual y actualiza las estadísticas.
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient
from src.data.data_manager import (
    save_season_data, load_season_data, 
    merge_games, update_team_stats, 
    update_pitcher_stats, get_last_update_date
)

def get_season_games() -> list:
    """Obtiene todos los juegos de la temporada actual."""
    client = MLBClient()
    
    # Definir el rango de fechas para la temporada regular
    # La temporada regular generalmente va desde finales de marzo hasta principios de octubre
    current_year = datetime.now().year
    season_start = datetime(current_year, 3, 1)  # 1 de marzo
    season_end = datetime(current_year, 10, 31)   # 31 de octubre
    
    print(f"Obteniendo todos los juegos de la temporada {current_year}...")
    print(f"Rango de fechas: {season_start.strftime('%Y-%m-%d')} a {season_end.strftime('%Y-%m-%d')}")
    
    # Obtener juegos para cada día en el rango
    all_games = []
    current_date = season_start
    
    while current_date <= season_end:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Procesando fecha: {date_str}")
        
        try:
            # Obtener el calendario para la fecha actual
            schedule = client.get_schedule(date_str)
            
            if schedule and 'dates' in schedule and schedule['dates']:
                for date in schedule['dates']:
                    if 'games' in date:
                        all_games.extend(date['games'])
                        print(f"  - Encontrados {len(date['games'])} juegos")
            
        except Exception as e:
            print(f"Error al obtener datos para {date_str}: {str(e)}")
        
        current_date += timedelta(days=1)
    
    print(f"Total de juegos obtenidos: {len(all_games)}")
    return all_games

def main():
    """Función principal."""
    print("=== Regenerando datos de la temporada ===")
    
    # Obtener todos los juegos de la temporada
    new_games = get_season_games()
    
    if not new_games:
        print("No se encontraron juegos para actualizar.")
        return
    
    # Cargar datos existentes (si los hay)
    existing_data = load_season_data()
    
    # Si no hay datos existentes, crear una estructura vacía
    if not existing_data:
        existing_data = {
            'games': [],
            'teams': {},
            'pitchers': {},
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
    
    # Combinar juegos existentes con los nuevos, eliminando duplicados
    existing_games = existing_data.get('games', [])
    all_games = merge_games(existing_games, new_games)
    
    # Actualizar estadísticas de equipos
    print("Actualizando estadísticas de equipos...")
    teams_data = update_team_stats({}, all_games)
    
    # Actualizar estadísticas de lanzadores
    print("Actualizando estadísticas de lanzadores...")
    pitchers_data = update_pitcher_stats({}, all_games)
    
    # Crear el nuevo diccionario de datos
    new_data = {
        'games': all_games,
        'teams': teams_data,
        'pitchers': pitchers_data,
        'last_updated': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Guardar los datos actualizados
    print("Guardando datos actualizados...")
    save_season_data(new_data)
    
    print("¡Datos de la temporada actualizados exitosamente!")
    print(f"Total de juegos: {len(all_games)}")
    print(f"Equipos: {len(teams_data)}")
    print(f"Lanzadores: {len(pitchers_data)}")

if __name__ == "__main__":
    main()
