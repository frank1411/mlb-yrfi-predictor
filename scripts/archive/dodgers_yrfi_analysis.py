#!/usr/bin/env python3
"""
Análisis de YRFI para Los Angeles Dodgers.
Este script genera un reporte detallado de los partidos de los Dodgers,
mostrando si hubo carreras en el primer inning o no.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mlb_client import MLBClient
from src.data.data_manager import load_season_data, save_season_data
from src.yrfi_calculator import YRFICalculator

# Configuración
TEAM_ID = 119  # ID de Los Angeles Dodgers en la API de MLB
SEASON = 2025
OUTPUT_FILE = "reports/dodgers_yrfi_analysis.csv"

def get_team_games(team_id: int, season: int) -> List[Dict]:
    """Obtiene todos los partidos de un equipo en una temporada."""
    client = MLBClient()
    all_games = []
    
    # Obtener la fecha de inicio y fin de la temporada regular
    start_date = f"{season}-03-20"  # Aprox. inicio de temporada
    end_date = f"{season}-10-01"    # Aprox. fin de temporada regular
    
    # Convertir a objetos de fecha para iterar
    from datetime import datetime, timedelta
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    print(f"Obteniendo partidos desde {start_date} hasta {end_date}...")
    
    # Iterar por cada día de la temporada
    current_date = start
    while current_date <= end:
        date_str = current_date.strftime("%Y-%m-%d")
        try:
            # Obtener partidos del día actual
            schedule = client.get_schedule(date=date_str)
            
            if schedule and 'dates' in schedule and schedule['dates']:
                for date_data in schedule['dates']:
                    for game in date_data.get('games', []):
                        # Verificar si el equipo está en este partido
                        teams = game.get('teams', {})
                        home_team = teams.get('home', {}).get('team', {}).get('id')
                        away_team = teams.get('away', {}).get('team', {}).get('id')
                        
                        if home_team == team_id or away_team == team_id:
                            all_games.append(game)
            
            # Procesar el siguiente día
            current_date += timedelta(days=1)
            
        except Exception as e:
            print(f"Error al obtener partidos para {date_str}: {str(e)}")
            current_date += timedelta(days=1)
    
    # Filtrar solo partidos ya jugados (status 'F' = Final)
    completed_games = [
        g for g in all_games 
        if g.get('status', {}).get('statusCode') in ['F', 'O']  # 'F' = Final, 'O' = En juego
    ]
    
    print(f"Se encontraron {len(completed_games)} partidos jugados de {len(all_games)} totales.")
    return completed_games

def analyze_games(games: List[Dict]) -> List[Dict]:
    """Analiza los partidos y determina si hubo carreras en el primer inning."""
    results = []
    
    for game in games:
        game_date = game.get('gameDate', '')
        home_team = game.get('teams', {}).get('home', {})
        away_team = game.get('teams', {}).get('away', {})
        
        # Determinar si los Dodgers son locales o visitantes
        is_home = home_team.get('team', {}).get('id') == TEAM_ID
        
        # Obtener el nombre del rival
        if is_home:
            rival_name = away_team.get('team', {}).get('name', 'Desconocido')
            rival_id = away_team.get('team', {}).get('id')
        else:
            rival_name = home_team.get('team', {}).get('name', 'Desconocido')
            rival_id = home_team.get('team', {}).get('id')
        
        # Obtener carreras en el primer inning
        home_runs_1st = 0
        away_runs_1st = 0
        
        # Intentar obtener del linescore
        linescore = game.get('linescore', {})
        if 'innings' in linescore:
            for inning in linescore['innings']:
                if inning.get('num') == 1:  # Primer inning
                    home_runs_1st = inning.get('home', {}).get('runs', 0)
                    away_runs_1st = inning.get('away', {}).get('runs', 0)
                    break
        
        # Determinar si hubo carreras para los Dodgers
        if is_home:
            yrfi = home_runs_1st > 0 or away_runs_1st > 0
            dodgers_runs = home_runs_1st
            rival_runs = away_runs_1st
        else:
            yrfi = home_runs_1st > 0 or away_runs_1st > 0
            dodgers_runs = away_runs_1st
            rival_runs = home_runs_1st
        
        # Agregar resultado
        results.append({
            'fecha': game_date,
            'rival': rival_name,
            'rival_id': rival_id,
            'es_local': is_home,
            'yrfi': 'Sí' if yrfi else 'No',
            'carreras_dodgers_1st': dodgers_runs,
            'carreras_rival_1st': rival_runs,
            'marcador_final': f"{home_team.get('score', 0)}-{away_team.get('score', 0)}",
            'game_id': game.get('gamePk')
        })
    
    return results

def save_to_csv(results: List[Dict], filename: str) -> None:
    """Guarda los resultados en un archivo CSV con separador '|'."""
    if not results:
        print("No hay resultados para guardar.")
        return
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Escribir archivo CSV con separador '|'
    with open(filename, 'w', encoding='utf-8') as f:
        # Escribir encabezados
        f.write('fecha|yrfi|rival\n')
        
        # Escribir datos
        for row in results:
            # Formatear fecha (de ISO a DD/MM)
            fecha_iso = row['fecha']
            fecha_obj = datetime.strptime(fecha_iso.split('T')[0], '%Y-%m-%d')
            fecha_formateada = fecha_obj.strftime('%d/%m')
            
            # Obtener datos para las columnas solicitadas
            yrfi = row['yrfi']
            rival = row['rival']
            
            # Crear línea con formato: fecha|yrfi|rival
            linea = f"{fecha_formateada}|{yrfi}|{rival}"
            f.write(linea + '\n')
    
    print(f"Reporte guardado en: {filename}")

def main():
    """Función principal."""
    print(f"Obteniendo partidos de Los Angeles Dodgers para la temporada {SEASON}...")
    
    try:
        # Obtener partidos de los Dodgers
        games = get_team_games(TEAM_ID, SEASON)
        
        if not games:
            print("No se encontraron partidos para analizar.")
            return
        
        print(f"Se encontraron {len(games)} partidos jugados.")
        
        # Analizar partidos
        results = analyze_games(games)
        
        # Ordenar por fecha (más reciente primero)
        results.sort(key=lambda x: x['fecha'], reverse=True)
        
        # Guardar resultados
        save_to_csv(results, OUTPUT_FILE)
        
        # Mostrar resumen
        total_games = len(results)
        yrfi_count = sum(1 for r in results if r['yrfi'] == 'Sí')
        yrfi_pct = (yrfi_count / total_games) * 100 if total_games > 0 else 0
        
        print(f"\nResumen de YRFI para Los Angeles Dodgers ({SEASON}):")
        print(f"Total de partidos: {total_games}")
        print(f"Partidos con YRFI: {yrfi_count} ({yrfi_pct:.1f}%)")
        
        # Estadísticas por condición (local/visitante)
        home_games = [r for r in results if r['es_local']]
        away_games = [r for r in results if not r['es_local']]
        
        if home_games:
            home_yrfi = sum(1 for g in home_games if g['yrfi'] == 'Sí')
            home_pct = (home_yrfi / len(home_games)) * 100
            print(f"\nEn casa: {home_yrfi}/{len(home_games)} ({home_pct:.1f}%)")
        
        if away_games:
            away_yrfi = sum(1 for g in away_games if g['yrfi'] == 'Sí')
            away_pct = (away_yrfi / len(away_games)) * 100
            print(f"De visita: {away_yrfi}/{len(away_games)} ({away_pct:.1f}%)")
        
    except Exception as e:
        print(f"Error al generar el reporte: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
