"""
Script para analizar estadísticas de lanzadores basado en datos históricos.
"""
import json
from typing import Dict, List, Tuple
from pathlib import Path

def load_season_data(file_path: str) -> dict:
    """Carga los datos de la temporada desde el archivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_pitcher_stats(season_data: dict) -> Dict[str, dict]:
    """
    Calcula estadísticas de YRFI para cada lanzador.
    
    Args:
        season_data: Datos de la temporada cargados desde el JSON
        
    Returns:
        Dict con estadísticas por lanzador
    """
    pitcher_stats = {}
    
    # Procesar cada juego
    for game in season_data.get('games', []):
        if 'pitchers' not in game:
            continue
            
        # Verificar si hay información de YRFI para el juego
        if 'home_yrfi' not in game or 'away_yrfi' not in game:
            continue
            
        # Procesar lanzador local
        if game['pitchers'].get('home') and isinstance(game['pitchers']['home'], dict):
            home_pitcher = game['pitchers']['home']
            if 'id' not in home_pitcher or 'name' not in home_pitcher:
                continue
                
            pitcher_id = str(home_pitcher['id'])
            pitcher_name = home_pitcher['name']
            yrfi = game['home_yrfi']  # True si permitió carreras en el 1er inning
            
            if pitcher_id not in pitcher_stats:
                pitcher_stats[pitcher_id] = {
                    'name': pitcher_name,
                    'total_games': 0,
                    'yrfi_games': 0,
                    'home_games': 0,
                    'home_yrfi': 0,
                    'away_games': 0,
                    'away_yrfi': 0
                }
                
            pitcher_stats[pitcher_id]['total_games'] += 1
            pitcher_stats[pitcher_id]['home_games'] += 1
            if yrfi:
                pitcher_stats[pitcher_id]['yrfi_games'] += 1
                pitcher_stats[pitcher_id]['home_yrfi'] += 1
        
        # Procesar lanzador visitante
        if game['pitchers'].get('away') and isinstance(game['pitchers']['away'], dict):
            away_pitcher = game['pitchers']['away']
            if 'id' not in away_pitcher or 'name' not in away_pitcher:
                continue
                
            pitcher_id = str(away_pitcher['id'])
            pitcher_name = away_pitcher['name']
            yrfi = game['away_yrfi']  # True si permitió carreras en el 1er inning
            
            if pitcher_id not in pitcher_stats:
                pitcher_stats[pitcher_id] = {
                    'name': pitcher_name,
                    'total_games': 0,
                    'yrfi_games': 0,
                    'home_games': 0,
                    'home_yrfi': 0,
                    'away_games': 0,
                    'away_yrfi': 0
                }
                
            pitcher_stats[pitcher_id]['total_games'] += 1
            pitcher_stats[pitcher_id]['away_games'] += 1
            if yrfi:
                pitcher_stats[pitcher_id]['yrfi_games'] += 1
                pitcher_stats[pitcher_id]['away_yrfi'] += 1
    
    # Calcular porcentajes
    for pitcher_id in pitcher_stats:
        stats = pitcher_stats[pitcher_id]
        
        # Porcentaje general
        stats['yrfi_pct'] = (stats['yrfi_games'] / stats['total_games'] * 100) if stats['total_games'] > 0 else 0
        
        # Porcentaje como local
        stats['home_yrfi_pct'] = (stats['home_yrfi'] / stats['home_games'] * 100) if stats['home_games'] > 0 else 0
        
        # Porcentaje como visitante
        stats['away_yrfi_pct'] = (stats['away_yrfi'] / stats['away_games'] * 100) if stats['away_games'] > 0 else 0
    
    return pitcher_stats

def get_pitcher_by_name(pitcher_stats: dict, name: str) -> dict:
    """Busca un lanzador por nombre (parcial o completo)."""
    name_lower = name.lower()
    for pitcher_id, stats in pitcher_stats.items():
        if name_lower in stats['name'].lower():
            return {**stats, 'id': pitcher_id}
    return None

def format_pitcher_stats(stats: dict) -> str:
    """Formatea las estadísticas de un lanzador para mostrarlas."""
    if not stats:
        return "Lanzador no encontrado"
        
    return f"""
Estadísticas de {stats['name']} (ID: {stats['id']}):
- Partidos totales: {stats['total_games']}
- Partidos con YRFI: {stats['yrfi_games']} ({stats['yrfi_pct']:.1f}%)

Como local:
- Partidos: {stats['home_games']}
- YRFI: {stats['home_yrfi']} ({stats['home_yrfi_pct']:.1f}%)

Como visitante:
- Partidos: {stats['away_games']}
- YRFI: {stats['away_yrfi']} ({stats['away_yrfi_pct']:.1f}%)
"""

def main():
    # Ruta al archivo de datos
    data_dir = Path(__file__).parent.parent / 'data'
    data_file = data_dir / 'season_data.json'
    
    # Cargar datos
    print(f"🔍 Cargando datos desde {data_file}...")
    season_data = load_season_data(data_file)
    
    # Calcular estadísticas de lanzadores
    print("📊 Calculando estadísticas de lanzadores...")
    pitcher_stats = get_pitcher_stats(season_data)
    
    # Mostrar estadísticas de algunos lanzadores conocidos
    print(f"\n📈 Estadísticas de lanzadores calculadas para {len(pitcher_stats)} lanzadores")
    
    # Buscar lanzadores específicos
    pitchers_to_check = ["Paul Skenes", "Cade Horton", "Sandy Alcantara", "Jacob deGrom"]
    
    for pitcher_name in pitchers_to_check:
        stats = get_pitcher_by_name(pitcher_stats, pitcher_name)
        print(format_pitcher_stats(stats))
        print("-" * 50)

if __name__ == "__main__":
    main()
