#!/usr/bin/env python3
"""
Script para actualizar los datos con los partidos más recientes.
Este script debe ejecutarse diariamente para mantener los datos actualizados.
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

def get_recent_games() -> list:
    """Obtiene los juegos desde la última actualización."""
    client = MLBClient()
    
    # Obtener la fecha de la última actualización
    last_update = get_last_update_date()
    
    # Si no hay última actualización, obtener datos de los últimos 7 días
    if not last_update:
        last_update = datetime.now() - timedelta(days=7)
        print("No se encontró una fecha de última actualización. Obteniendo datos de los últimos 7 días.")
    else:
        print(f"Última actualización: {last_update.strftime('%Y-%m-%d')}")
    
    # Asegurarse de no incluir el día de la última actualización
    start_date = last_update + timedelta(days=1)
    end_date = datetime.now()
    
    # Si no hay días nuevos para actualizar, salir
    if start_date > end_date:
        print("Los datos ya están actualizados hasta la fecha actual.")
        return []
    
    print(f"Obteniendo juegos desde {start_date.strftime('%Y-%m-%d')} hasta {end_date.strftime('%Y-%m-%d')}...")
    
    # Obtener juegos para cada día en el rango
    all_games = []
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Procesando fecha: {date_str}")
        
        try:
            schedule = client.get_schedule(date=date_str)
            if 'dates' in schedule and schedule['dates']:
                games = schedule['dates'][0].get('games', [])
                all_games.extend(games)
                print(f"  Encontrados {len(games)} juegos")
        except Exception as e:
            print(f"  Error al obtener juegos para {date_str}: {e}")
        
        current_date += timedelta(days=1)
    
    print(f"Total de juegos nuevos obtenidos: {len(all_games)}")
    return all_games

def main():
    print("=== Actualización diaria de datos ===")
    
    # Cargar datos existentes
    existing_data = load_season_data()
    
    # Obtener juegos recientes
    new_games = get_recent_games()
    
    if not new_games:
        print("No hay juegos nuevos para actualizar.")
        return
    
    # Combinar con juegos existentes
    merged_games = merge_games(existing_data.get('games', []), new_games)
    
    # Actualizar estadísticas
    teams = update_team_stats(existing_data.get('teams', {}).copy(), new_games)
    pitchers = update_pitcher_stats(existing_data.get('pitchers', {}).copy(), new_games)
    
    # Preparar datos actualizados
    updated_data = {
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'games': merged_games,
        'teams': teams,
        'pitchers': pitchers
    }
    
    # Guardar datos actualizados
    save_season_data(updated_data)
    
    print(f"\nDatos actualizados exitosamente.")
    print(f"- Juegos totales: {len(merged_games)}")
    print(f"- Equipos registrados: {len(teams)}")
    print(f"- Lanzadores registrados: {len(pitchers)}")
    print(f"- Última actualización: {updated_data['last_updated']}")

if __name__ == "__main__":
    main()
