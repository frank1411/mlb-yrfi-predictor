#!/usr/bin/env python3
"""
Script temporal para analizar los registros de Jesús Luzardo.
"""
import sys
from pathlib import Path
from typing import Dict, Any
import json

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

# Importar la función get_pitcher_stats
try:
    from scripts.generar_pronostico import get_pitcher_stats, load_season_data
    from src.data.data_manager import SEASON_DATA_FILE
    
    # Cargar los datos de la temporada
    print("Cargando datos de la temporada...")
    season_data = load_season_data(SEASON_DATA_FILE)
    
    # Buscar a Jesús Luzardo por nombre
    print("\nBuscando estadísticas de Jesús Luzardo...")
    luzardo_stats = get_pitcher_stats(season_data, pitcher_name="Jesús Luzardo")
    
    if not luzardo_stats or 'name' not in luzardo_stats:
        print("No se encontraron estadísticas para Jesús Luzardo")
    else:
        print(f"\n=== ESTADÍSTICAS DE {luzardo_stats.get('name', 'Jesús Luzardo').upper()} ===")
        print(f"ID: {luzardo_stats.get('id', 'N/A')}")
        print(f"Juegos totales: {luzardo_stats.get('total_games', 0)}")
        print(f"YRFI totales: {luzardo_stats.get('yrfi_games', 0)} ({(luzardo_stats.get('yrfi_pct', 0)):.1f}%)")
        
        print("\nComo LOCAL:")
        print(f"- Juegos: {luzardo_stats.get('home_games', 0)}")
        print(f"- YRFI: {luzardo_stats.get('home_yrfi', 0)} ({(luzardo_stats.get('home_yrfi_pct', 0)):.1f}%)")
        
        print("\nComo VISITANTE:")
        print(f"- Juegos: {luzardo_stats.get('away_games', 0)}")
        print(f"- YRFI: {luzardo_stats.get('away_yrfi', 0)} ({(luzardo_stats.get('away_yrfi_pct', 0)):.1f}%)")
        
        # Mostrar los juegos individuales si hay pocos
        if luzardo_stats.get('total_games', 0) <= 15:
            print("\nDetalle de juegos:")
            for game in luzardo_stats.get('games', []):
                game_date = game.get('gameDate', '').split('T')[0]
                home_team = game.get('home_team_name', '?')
                away_team = game.get('away_team_name', '?')
                is_home = game.get('is_home', False)
                yrfi = "SÍ" if game.get('yrfi', False) else "NO"
                
                print(f"{game_date}: {away_team} @ {home_team} - YRFI: {yrfi}")
        
        print("\n=== ANÁLISIS ===")
        if luzardo_stats.get('home_games', 0) < 3 and luzardo_stats.get('away_games', 0) < 3:
            print("ADVERTENCIA: Muy pocos juegos tanto como local como visitante. Se recomienda usar estadísticas totales.")
        elif luzardo_stats.get('home_games', 0) < 3:
            print("NOTA: Pocos juegos como local. Considerar usar estadísticas totales para local.")
        elif luzardo_stats.get('away_games', 0) < 3:
            print("NOTA: Pocos juegos como visitante. Considerar usar estadísticas totales para visitante.")
        else:
            print("Suficientes juegos tanto como local como visitante. Se pueden usar estadísticas diferenciadas.")
            
        print("\nRecomendación: Usar estadísticas totales cuando haya menos de 3 juegos en una categoría (local/visitante).")
        
except Exception as e:
    print(f"Error al analizar los datos: {str(e)}")
    raise
