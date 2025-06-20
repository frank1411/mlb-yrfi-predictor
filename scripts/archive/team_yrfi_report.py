#!/usr/bin/env python3
"""
Script para generar un informe de YRFI de un equipo específico en la temporada actual.
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Configuración
DATA_DIR = Path(__file__).parent.parent / "data"
SEASON_DATA_FILE = DATA_DIR / "season_data.json"
TEAM_ID = 144  # ID de los Atlanta Braves en la MLB
TEAM_NAME = "Atlanta Braves"

def load_season_data() -> Dict[str, Any]:
    """Carga los datos de la temporada desde el archivo JSON."""
    try:
        with open(SEASON_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar los datos de la temporada: {e}")
        sys.exit(1)

def get_team_games(season_data: Dict, team_id: int) -> List[Dict]:
    """Obtiene todos los partidos de un equipo específico."""
    team_games = []
    
    for game in season_data.get('games', []):
        # Verificar si el partido ya terminó
        if game.get('status', {}).get('abstractGameState') != 'Final':
            continue
            
        game_date = game.get('officialDate')
        if not game_date:
            continue
            
        home_team = game.get('teams', {}).get('home', {})
        away_team = game.get('teams', {}).get('away', {})
        
        home_team_id = home_team.get('team', {}).get('id')
        away_team_id = away_team.get('team', {}).get('id')
        
        # Verificar si el equipo participó en este partido
        if team_id not in (home_team_id, away_team_id):
            continue
            
        # Determinar si es local o visitante
        is_home = team_id == home_team_id
        opponent = home_team if not is_home else away_team
        opponent_name = opponent.get('team', {}).get('name', 'Desconocido')
        
        # Obtener carreras en el primer inning
        home_runs_1st = 0
        away_runs_1st = 0
        
        # Intentar obtener del linescore si está disponible
        linescore = game.get('linescore', {})
        if linescore and 'innings' in linescore and len(linescore['innings']) > 0:
            # Buscar el primer inning (inning 1)
            for inning in linescore['innings']:
                if inning.get('num') == 1:  # Primer inning
                    home_runs_1st = inning.get('home', {}).get('runs', 0)
                    away_runs_1st = inning.get('away', {}).get('runs', 0)
                    break
        
        # Determinar carreras del equipo y del oponente
        team_runs = home_runs_1st if is_home else away_runs_1st
        opponent_runs = away_runs_1st if is_home else home_runs_1st
        
        # Determinar si hubo YRFI (carreras en el primer inning)
        yrfi = team_runs > 0 or opponent_runs > 0
        
        # Agregar información del partido
        team_games.append({
            'date': game_date,
            'is_home': is_home,
            'opponent': opponent_name,
            'team_runs_1st': team_runs,
            'opponent_runs_1st': opponent_runs,
            'yrfi': yrfi,
            'game_data': game  # Guardar datos completos por si acaso
        })
    
    # Ordenar partidos por fecha (más antiguo primero)
    team_games.sort(key=lambda x: x['date'])
    
    return team_games

def generate_report(team_name: str, games: List[Dict]) -> str:
    """
    Genera un informe con los partidos del equipo.
    
    Args:
        team_name: Nombre del equipo
        games: Lista de partidos del equipo
        
    Returns:
        El informe generado como cadena de texto
    """
    report = []
    
    # Encabezado
    report.append(f"REPORTE DE YRFI - {team_name.upper()}")
    report.append("=" * 60)
    report.append(f"Total de partidos: {len(games)}")
    
    # Calcular estadísticas
    yrfi_count = sum(1 for g in games if g['yrfi'])
    yrfi_pct = (yrfi_count / len(games) * 100) if games else 0
    
    report.append(f"Partidos con YRFI: {yrfi_count}/{len(games)} ({yrfi_pct:.1f}%)")
    report.append("")
    
    # Tabla de partidos
    report.append("-" * 80)
    report.append(f"{'FECHA':<12} {'PARTIDO':<40} {'RESULTADO 1°':<15} {'YRFI'}")
    report.append("-" * 80)
    
    for game in games:
        vs_team = f"vs {game['opponent']}" if game['is_home'] else f"@ {game['opponent']}"
        result_1st = f"{game['team_runs_1st']}-{game['opponent_runs_1st']}"
        yrfi = "Sí" if game['yrfi'] else "No"
        
        report.append(f"{game['date']:<12} {vs_team:<40} {result_1st:<15} {yrfi}")
    
    # Resumen
    report.append("")
    report.append("-" * 80)
    report.append(f"RESUMEN - {team_name}")
    report.append("-" * 80)
    report.append(f"Total partidos: {len(games)}")
    report.append(f"Partidos con YRFI: {yrfi_count} ({yrfi_pct:.1f}%)")
    report.append(f"Partidos sin YRFI: {len(games) - yrfi_count} ({100 - yrfi_pct:.1f}%)")
    
    # Calcular racha actual de YRFI/No YRFI
    if games:
        current_streak = 1
        current_type = games[-1]['yrfi']
        
        for game in reversed(games[:-1]):
            if game['yrfi'] == current_type:
                current_streak += 1
            else:
                break
                
        streak_type = "YRFI" if current_type else "No YRFI"
        report.append(f"Racha actual ({streak_type}): {current_streak} partidos")
    
    return "\n".join(report)

def main():
    """Función principal."""
    print(f"Cargando datos de {SEASON_DATA_FILE}...")
    season_data = load_season_data()
    
    print(f"Buscando partidos de {TEAM_NAME}...")
    games = get_team_games(season_data, TEAM_ID)
    
    if not games:
        print(f"No se encontraron partidos para {TEAM_NAME}")
        return
    
    # Generar y mostrar el informe
    report = generate_report(TEAM_NAME, games)
    
    # Guardar el informe en un archivo
    output_file = f"{TEAM_NAME.lower().replace(' ', '_')}_yrfi_report.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Mostrar el informe en la consola
    print("\n" + "=" * 80)
    print(f"REPORTE DE YRFI - {TEAM_NAME.upper()}")
    print("=" * 80)
    print(f"Total de partidos: {len(games)}")
    
    # Mostrar resumen
    yrfi_count = sum(1 for g in games if g['yrfi'])
    yrfi_pct = (yrfi_count / len(games) * 100) if games else 0
    print(f"Partidos con YRFI: {yrfi_count}/{len(games)} ({yrfi_pct:.1f}%)")
    
    # Mostrar los últimos 10 partidos
    print("\nÚLTIMOS 10 PARTIDOS:")
    print("-" * 60)
    print(f"{'FECHA':<12} {'PARTIDO':<40} {'RESULTADO 1°':<15} {'YRFI'}")
    print("-" * 60)
    
    for game in games[-10:]:
        vs_team = f"vs {game['opponent']}" if game['is_home'] else f"@ {game['opponent']}"
        result_1st = f"{game['team_runs_1st']}-{game['opponent_runs_1st']}"
        yrfi = "Sí" if game['yrfi'] else "No"
        
        print(f"{game['date']:<12} {vs_team:<40} {result_1st:<15} {yrfi}")
    
    print("\n¡Informe generado con éxito!")
    print(f"El informe completo se ha guardado en: {output_file}")

if __name__ == "__main__":
    main()
