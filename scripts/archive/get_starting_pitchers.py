#!/usr/bin/env python3
"""
Script para obtener los lanzadores abridores de todos los juegos de la temporada actual.
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient
from src.data.data_manager import SEASON_DATA_FILE, load_season_data

def get_pitchers_for_games(games: List[Dict[str, Any]]) -> Dict[str, Dict]:
    """
    Obtiene los lanzadores abridores para una lista de juegos.
    
    Args:
        games: Lista de diccionarios con información de los juegos.
        
    Returns:
        Diccionario con los lanzadores abridores por juego:
        {
            'game_id': {
                'home': {'id': '123', 'name': 'Pitcher Name'},
                'away': {'id': '456', 'name': 'Pitcher Name'}
            },
            ...
        }
    """
    client = MLBClient()
    pitchers_data = {}
    
    for game in games:
        game_id = game.get('game_id')
        game_pk = game.get('gamePk')
        
        if not game_id or not game_pk:
            print(f"[WARNING] Juego sin ID o gamePk: {game}")
            continue
        
        print(f"Obteniendo lanzadores para el juego {game_id} (gamePk: {game_pk})...")
        
        try:
            pitchers = client.get_starting_pitchers(game_pk)
            if pitchers and 'home' in pitchers and 'away' in pitchers:
                pitchers_data[game_id] = pitchers
                print(f"  - Lanzadores: {pitchers['away']['name']} @ {pitchers['home']['name']}")
            else:
                print(f"  [WARNING] No se pudieron obtener los lanzadores para el juego {game_id}")
        except Exception as e:
            print(f"  [ERROR] Error al obtener lanzadores para el juego {game_id}: {str(e)}")
        
        # Pequeña pausa para no sobrecargar la API
        import time
        time.sleep(0.5)
    
    return pitchers_data

def main():
    """Función principal."""
    print("=== OBTENIENDO LANZADORES ABRIDORES DE LA TEMPORADA 2025 ===\n")
    
    # Cargar datos de la temporada
    print("Cargando datos de la temporada...")
    season_data = load_season_data()
    
    if not season_data or 'games' not in season_data or not season_data['games']:
        print("[ERROR] No se pudieron cargar los juegos de la temporada.")
        return
    
    print(f"Se encontraron {len(season_data['games'])} juegos en la temporada.")
    
    # Obtener lanzadores para cada juego
    pitchers_data = get_pitchers_for_games(season_data['games'])
    
    # Guardar los resultados
    output_file = Path(__file__).parent.parent / 'data' / 'pitchers_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pitchers_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSe guardaron los datos de lanzadores en {output_file}")
    print(f"Total de juegos procesados: {len(pitchers_data)}")

if __name__ == "__main__":
    main()
