#!/usr/bin/env python3
"""
Script para analizar los últimos 15 partidos de cada equipo y verificar estadísticas de YRFI.
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

# Configuración
WINDOW_SIZE = 15  # Número de partidos recientes a analizar
DATA_DIR = Path(__file__).parent.parent / "data"
SEASON_DATA_FILE = DATA_DIR / "season_data.json"

def load_season_data() -> Dict[str, Any]:
    """Carga los datos de la temporada desde el archivo JSON."""
    try:
        with open(SEASON_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar los datos de la temporada: {e}")
        sys.exit(1)

def get_team_name(team_data: Dict) -> str:
    """Obtiene el nombre del equipo a partir de los datos del equipo."""
    return team_data.get('team', {}).get('name', 'Desconocido')

def analyze_recent_games(season_data: Dict) -> Dict[str, Dict]:
    """
    Analiza los últimos partidos de cada equipo y calcula estadísticas de YRFI.
    
    Args:
        season_data: Datos completos de la temporada
        
    Returns:
        Dict con estadísticas de YRFI por equipo
    """
    # Diccionario para almacenar los partidos por equipo
    team_games = defaultdict(list)
    
    # Procesar todos los partidos
    for game in season_data.get('games', []):
        if game.get('status', {}).get('abstractGameState') != 'Final':
            continue  # Saltar partidos no finalizados
            
        game_date = game.get('officialDate')
        if not game_date:
            continue
            
        # Obtener información de los equipos
        home_team = game.get('teams', {}).get('home', {})
        away_team = game.get('teams', {}).get('away', {})
        
        home_team_id = home_team.get('team', {}).get('id')
        away_team_id = away_team.get('team', {}).get('id')
        
        if not home_team_id or not away_team_id:
            continue
            
        # Obtener carreras en el primer inning
        home_runs_1st = 0
        away_runs_1st = 0
        
        # Intentar obtener del linescore si está disponible
        linescore = game.get('linescore', {})
        if linescore:
            home_runs_1st = linescore.get('home', {}).get('runs', 0)
            away_runs_1st = linescore.get('away', {}).get('runs', 0)
        
        # Agregar partido al equipo local
        team_games[home_team_id].append({
            'date': game_date,
            'is_home': True,
            'opponent_id': away_team_id,
            'opponent_name': get_team_name(away_team),
            'runs_1st': home_runs_1st,
            'yrfi': home_runs_1st > 0
        })
        
        # Agregar partido al equipo visitante
        team_games[away_team_id].append({
            'date': game_date,
            'is_home': False,
            'opponent_id': home_team_id,
            'opponent_name': get_team_name(home_team),
            'runs_1st': away_runs_1st,
            'yrfi': away_runs_1st > 0
        })
    
    # Ordenar partidos por fecha (más reciente primero)
    for team_id in team_games:
        team_games[team_id].sort(key=lambda x: x['date'], reverse=True)
    
    # Calcular estadísticas de los últimos 15 partidos
    team_stats = {}
    for team_id, games in team_games.items():
        recent_games = games[:WINDOW_SIZE]
        total_games = len(recent_games)
        
        if total_games == 0:
            continue
            
        # Calcular estadísticas
        yrfi_count = sum(1 for g in recent_games if g['yrfi'])
        yrfi_pct = (yrfi_count / total_games) * 100
        
        # Calcular promedio de carreras en el primer inning
        avg_runs = sum(g['runs_1st'] for g in recent_games) / total_games
        
        # Obtener nombre del equipo
        team_name = recent_games[0]['opponent_name'] if recent_games else 'Desconocido'
        
        # Almacenar estadísticas
        team_stats[team_id] = {
            'name': team_name,
            'games_analyzed': total_games,
            'yrfi_count': yrfi_count,
            'yrfi_pct': yrfi_pct,
            'avg_runs_1st': avg_runs,
            'recent_games': [
                {
                    'date': g['date'],
                    'vs': f"{'vs' if g['is_home'] else '@'} {g['opponent_name']}",
                    'runs_1st': g['runs_1st'],
                    'yrfi': 'Sí' if g['yrfi'] else 'No'
                }
                for g in recent_games
            ]
        }
    
    return team_stats

def generate_report(team_stats: Dict[str, Dict], output_file: Optional[str] = None) -> str:
    """
    Genera un informe con las estadísticas de YRFI por equipo.
    
    Args:
        team_stats: Estadísticas de YRFI por equipo
        output_file: Ruta del archivo de salida (opcional)
        
    Returns:
        El informe generado como cadena de texto
    """
    report = []
    
    # Encabezado
    report.append("=" * 80)
    report.append(f"ANÁLISIS DE YRFI - ÚLTIMOS {WINDOW_SIZE} PARTIDOS")
    report.append("=" * 80)
    report.append("")
    
    # Ordenar equipos por porcentaje de YRFI (de mayor a menor)
    sorted_teams = sorted(
        team_stats.values(),
        key=lambda x: x['yrfi_pct'],
        reverse=True
    )
    
    # Resumen general
    total_teams = len(sorted_teams)
    total_games = sum(s['games_analyzed'] for s in sorted_teams) if total_teams > 0 else 0
    total_yrfi = sum(s['yrfi_count'] for s in sorted_teams) if total_teams > 0 else 0
    overall_yrfi_pct = (total_yrfi / total_games * 100) if total_games > 0 else 0
    
    report.append(f"Total de equipos analizados: {total_teams}")
    report.append(f"Total de partidos analizados: {total_games}")
    report.append(f"Promedio general de YRFI: {overall_yrfi_pct:.1f}%")
    report.append("")
    
    # Tabla de resumen
    report.append("-" * 80)
    report.append(f"{'EQUIPO':<25} {'PARTIDOS':>10} {'YRFI':>10} {'% YRFI':>10} {'AVG CARRERAS':>15}")
    report.append("-" * 80)
    
    for team in sorted_teams:
        report.append(
            f"{team['name']:<25} "
            f"{team['games_analyzed']:>10} "
            f"{team['yrfi_count']:>10} "
            f"{team['yrfi_pct']:>9.1f}% "
            f"{team['avg_runs_1st']:>14.2f}"
        )
    
    report.append("")
    
    # Detalle por equipo
    report.append("=" * 80)
    report.append("DETALLE POR EQUIPO")
    report.append("=" * 80)
    report.append("")
    
    for team in sorted_teams:
        report.append(f"{team['name']} - {team['games_analyzed']} partidos analizados")
        report.append(f"YRFI: {team['yrfi_count']}/{team['games_analyzed']} ({team['yrfi_pct']:.1f}%)")
        report.append(f"Promedio de carreras en 1er inning: {team['avg_runs_1st']:.2f}")
        report.append("")
        
        # Últimos partidos
        report.append("Últimos partidos (más recientes primero):")
        report.append("-" * 60)
        report.append(f"{'FECHA':<12} {'PARTIDO':<30} {'CARRERAS 1°':>12} {'YRFI':>6}")
        report.append("-" * 60)
        
        for game in team['recent_games']:
            report.append(
                f"{game['date']:<12} {game['vs']:<30} "
                f"{game['runs_1st']:>7} {'':>5} "
                f"{game['yrfi']:>6}"
            )
        
        report.append("")
    
    # Unir todo el informe en una sola cadena
    full_report = "\n".join(report)
    
    # Guardar en archivo si se especificó
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_report)
            print(f"Informe guardado en: {output_file}")
        except Exception as e:
            print(f"Error al guardar el informe: {e}")
    
    return full_report

def main():
    """Función principal."""
    print(f"Cargando datos de {SEASON_DATA_FILE}...")
    season_data = load_season_data()
    
    print(f"Analizando los últimos {WINDOW_SIZE} partidos de cada equipo...")
    team_stats = analyze_recent_games(season_data)
    
    # Generar informe
    output_file = f"yrfi_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report = generate_report(team_stats, output_file)
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE ANÁLISIS YRFI")
    print("=" * 60)
    print(f"Equipos analizados: {len(team_stats)}")
    
    # Mostrar top 5 equipos con mayor % YRFI
    print("\nTop 5 equipos con mayor % YRFI:")
    print("-" * 50)
    print(f"{'EQUIPO':<25} {'PARTIDOS':>8} {'YRFI':>8} {'% YRFI':>10} {'AVG CARRERAS':>15}")
    print("-" * 50)
    
    for team in sorted(
        team_stats.values(),
        key=lambda x: x['yrfi_pct'],
        reverse=True
    )[:5]:
        print(
            f"{team['name']:<25} "
            f"{team['games_analyzed']:>8} "
            f"{team['yrfi_count']:>8} "
            f"{team['yrfi_pct']:>9.1f}% "
            f"{team['avg_runs_1st']:>14.2f}"
        )
    
    print("\n¡Análisis completado!")
    print(f"El informe detallado se ha guardado en: {output_file}")

if __name__ == "__main__":
    main()
