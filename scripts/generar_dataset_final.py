import json
import pandas as pd
from datetime import datetime

# --- PARÁMETROS DE CONFIGURACIÓN ---
import os

# --- PARÁMETROS DE CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_JSON_FILE = os.path.join(BASE_DIR, 'data', 'season_data.json')
# Cambiamos el nombre del archivo de salida para no sobreescribir el anterior
OUTPUT_CSV_FILE = os.path.join(BASE_DIR, 'data', 'dataset_mlb_MULTITARGET.csv') 
CREDIBILITY_CONSTANT_C = 15
LAST_N_GAMES = 15

def create_ml_dataset():
    """
    Carga los datos de la temporada y crea un dataset optimizado para
    predecir YRFI basándose en duelos ofensivos y defensivos.
    """
    print(f"Cargando datos desde '{INPUT_JSON_FILE}'...")
    with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_games = data.get('games', [])
    final_games = [g for g in all_games if g.get('status', {}).get('statusCode') == 'F']
    sorted_games = sorted(final_games, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    
    print(f"Se encontraron {len(sorted_games)} partidos finalizados. Iniciando procesamiento...")

    processed_data = []
    total_games = len(sorted_games)

    for i, current_game in enumerate(sorted_games):
        history = sorted_games[:i]
        
        if len(history) < 30:
            continue
            
        if (i + 1) % 100 == 0:
            print(f"Procesando partido {i + 1}/{total_games}...")

        # --- El resto del código de cálculo es idéntico y correcto ---

        total_team_yrfi_chances = 2 * len(history)
        total_team_yrfi_scored = sum(g.get('home_yrfi', False) for g in history) + sum(g.get('away_yrfi', False) for g in history)
        league_avg_team_yrfi = total_team_yrfi_scored / total_team_yrfi_chances

        local_team_id = current_game.get('home_team')
        visit_team_id = current_game.get('away_team')
        pitchers = current_game.get('pitchers', {})
        local_pitcher_id = pitchers.get('home', {}).get('id') if pitchers.get('home') else None
        visit_pitcher_id = pitchers.get('away', {}).get('id') if pitchers.get('away') else None

        local_games_history = [g for g in history if local_team_id in (g.get('home_team'), g.get('away_team'))]
        visit_games_history = [g for g in history if visit_team_id in (g.get('home_team'), g.get('away_team'))]

        local_home_games = [g for g in local_games_history if g.get('home_team') == local_team_id]
        local_pct_anota_1inn_local = sum(g['home_yrfi'] for g in local_home_games) / len(local_home_games) if local_home_games else 0.0
        local_last_n = local_games_history[-LAST_N_GAMES:]
        local_anota_ult15 = sum(1 for g in local_last_n if (g.get('home_team') == local_team_id and g['home_yrfi']) or (g.get('away_team') == local_team_id and g['away_yrfi']))
        local_pct_anota_1inn_ult15 = local_anota_ult15 / len(local_last_n) if local_last_n else 0.0

        visit_away_games = [g for g in visit_games_history if g.get('away_team') == visit_team_id]
        visit_pct_anota_1inn_visit = sum(g['away_yrfi'] for g in visit_away_games) / len(visit_away_games) if visit_away_games else 0.0
        visit_last_n = visit_games_history[-LAST_N_GAMES:]
        visit_anota_ult15 = sum(1 for g in visit_last_n if (g.get('home_team') == visit_team_id and g['home_yrfi']) or (g.get('away_team') == visit_team_id and g['away_yrfi']))
        visit_pct_anota_1inn_ult15 = visit_anota_ult15 / len(visit_last_n) if visit_last_n else 0.0
        
        def get_pitcher_stats(pitcher_id, history_games, is_home_pitcher):
            if not pitcher_id or not history_games:
                return league_avg_team_yrfi
                
            starts = []
            for game in history_games:
                pitchers = game.get('pitchers')
                if not pitchers:
                    continue
                    
                home_pitcher = pitchers.get('home', {}) if isinstance(pitchers, dict) else {}
                away_pitcher = pitchers.get('away', {}) if isinstance(pitchers, dict) else {}
                
                if (isinstance(home_pitcher, dict) and home_pitcher.get('id') == pitcher_id) or \
                   (isinstance(away_pitcher, dict) and away_pitcher.get('id') == pitcher_id):
                    starts.append(game)
            
            n = len(starts)
            if n == 0:
                return league_avg_team_yrfi
                
            runs_allowed = 0
            for game in starts:
                pitchers = game.get('pitchers', {})
                if not pitchers:
                    continue
                    
                home_pitcher = pitchers.get('home', {}) if isinstance(pitchers, dict) else {}
                away_pitcher = pitchers.get('away', {}) if isinstance(pitchers, dict) else {}
                
                if (isinstance(home_pitcher, dict) and home_pitcher.get('id') == pitcher_id and game.get('away_yrfi')) or \
                   (isinstance(away_pitcher, dict) and away_pitcher.get('id') == pitcher_id and game.get('home_yrfi')):
                    runs_allowed += 1
            
            p_raw = runs_allowed / n if n > 0 else 0
            p_smoothed = ((n * p_raw) + (CREDIBILITY_CONSTANT_C * league_avg_team_yrfi)) / (n + CREDIBILITY_CONSTANT_C)
            return p_smoothed
        
        pitcher_local_pct_permite_carrera_suavizado = get_pitcher_stats(local_pitcher_id, history, is_home_pitcher=True)
        pitcher_visit_pct_permite_carrera_suavizado = get_pitcher_stats(visit_pitcher_id, history, is_home_pitcher=False)

        # --- INICIO DEL CAMBIO ---
        # Aquí se construye la fila final. Añadimos las 3 columnas objetivo.
        row = {
            'id_partido': current_game.get('game_id'),
            'fecha': current_game.get('date'),
            'equipo_local': current_game.get('home_team_name'),
            'equipo_visitante': current_game.get('away_team_name'),
            'local_pct_anota_1inn_local': round(local_pct_anota_1inn_local, 4),
            'local_pct_anota_1inn_ult15': round(local_pct_anota_1inn_ult15, 4),
            'visit_pct_anota_1inn_visit': round(visit_pct_anota_1inn_visit, 4),
            'visit_pct_anota_1inn_ult15': round(visit_pct_anota_1inn_ult15, 4),
            'pitcher_local_pct_permite_carrera_suavizado': round(pitcher_local_pct_permite_carrera_suavizado, 4),
            'pitcher_visit_pct_permite_carrera_suavizado': round(pitcher_visit_pct_permite_carrera_suavizado, 4),
            
            # --- Las 3 Columnas Objetivo ---
            # Las renombro con el sufijo "_target" por claridad, pero puedes usar los nombres que propusiste.
            'game_yrfi_target': 1 if current_game.get('game_yrfi') else 0,
            'home_yrfi_target': 1 if current_game.get('home_yrfi') else 0,
            'away_yrfi_target': 1 if current_game.get('away_yrfi') else 0,
        }
        # --- FIN DEL CAMBIO ---
        
        processed_data.append(row)

    df = pd.DataFrame(processed_data)
    df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8')
    
    print(f"\n¡Éxito! Archivo '{OUTPUT_CSV_FILE}' creado con {len(df)} filas.")
    print("\nEjemplo de las últimas 5 filas del archivo DEFINITIVO:")
    print(df.tail())

if __name__ == "__main__":
    create_ml_dataset()