#!/usr/bin/env python3
"""
Script para generar un dataset de Machine Learning para predicciones YRFI (Yes Run First Inning).
Incluye mejoras en el seguimiento de estadísticas y manejo de datos.
"""
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from pathlib import Path

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'ml_datasets'
SEASON_DATA_PATH = DATA_DIR / 'season_data.json'

# Crear directorio de salida si no existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def safe_division(numerator, denominator):
    """Evita la división por cero, devolviendo 0.0 en su lugar."""
    if denominator == 0 or denominator is None or pd.isna(denominator):
        return 0.0
    return numerator / denominator

def bayesian_smoothing(value, sample_size, global_mean, K):
    """
    Aplica suavizado bayesiano a una estadística.
    
    Args:
        value: Valor observado de la estadística
        sample_size: Tamaño de la muestra
        global_mean: Media global de la estadística
        K: Factor de suavizado (mayor K = más peso a la media global)
    """
    if sample_size == 0 or sample_size is None or pd.isna(sample_size):
        return global_mean
    return (sample_size * value + K * global_mean) / (sample_size + K)

def load_season_data(file_path):
    """Carga y procesa los datos de la temporada."""
    print(f"Cargando datos desde {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error al cargar el archivo {file_path}: {e}")
        return None

def process_season_data(season_data, K_smoothing=5):
    """
    Procesa los datos de la temporada para generar características de ML.
    
    Args:
        season_data: Datos de la temporada cargados desde JSON
        K_smoothing: Factor de suavizado bayesiano
        
    Returns:
        DataFrame con las características generadas
    """
    if not season_data or 'games' not in season_data:
        print("Datos de temporada no válidos o vacíos.")
        return pd.DataFrame()
        
    games_list = season_data['games']
    print(f"Procesando {len(games_list)} juegos...")
    
    # 1. Aplanar la estructura de los juegos
    flat_games = []
    for game in games_list:
        if game.get('status', {}).get('statusCode') == 'F':
            flat_game = {
                'id_partido': game['game_id'],
                'fecha': pd.to_datetime(game['date']),
                'equipo_local': game['home_team'],
                'equipo_visitante': game['away_team'],
                'pitcher_local_id': game['pitchers']['home']['id'] if game['pitchers'].get('home') else None,
                'pitcher_visit_id': game['pitchers']['away']['id'] if game['pitchers'].get('away') else None,
                'home_yrfi_target': int(game['home_yrfi']),
                'away_yrfi_target': int(game['away_yrfi']),
                'game_yrfi_target': int(game['game_yrfi'])
            }
            flat_games.append(flat_game)

    if not flat_games:
        print("No se encontraron juegos finalizados en el archivo JSON.")
        return pd.DataFrame()

    # 2. Convertir a DataFrame y ordenar cronológicamente
    df = pd.DataFrame(flat_games).sort_values('fecha').reset_index(drop=True)
    processed_rows = []
    
    print(f"Generando características para {len(df)} partidos...")

    # 3. Bucle principal para generar características
    for i in tqdm(range(len(df)), desc="Procesando partidos"):
        current_game = df.iloc[i]
        history_df = df.iloc[:i]  # Solo datos históricos
        
        if history_df.empty:
            continue
            
        # --- Calcular promedios globales ---
        league_avg_home_score_pct = history_df['home_yrfi_target'].mean()
        league_avg_away_score_pct = history_df['away_yrfi_target'].mean()
        total_runs_allowed = history_df['home_yrfi_target'].sum() + history_df['away_yrfi_target'].sum()
        total_pitching_apps = len(history_df) * 2
        league_avg_pitcher_allow_pct = safe_division(total_runs_allowed, total_pitching_apps)

        # --- Features del Equipo Local ---
        home_team_id = current_game['equipo_local']
        
        # Estadísticas como local
        home_team_as_home_hist = history_df[history_df['equipo_local'] == home_team_id]
        if not home_team_as_home_hist.empty:
            local_anota_local_count = home_team_as_home_hist['home_yrfi_target'].sum()
            local_juegos_local_count = len(home_team_as_home_hist)
            local_pct_anota_1inn_local = safe_division(local_anota_local_count, local_juegos_local_count)
            ratio_local_pct_anota_1inn_local = f"{int(local_anota_local_count)}/{local_juegos_local_count}"
        else:
            local_pct_anota_1inn_local = league_avg_home_score_pct
            ratio_local_pct_anota_1inn_local = "0/0"
            
        # Últimos 15 juegos (local o visitante)
        home_team_all_hist = history_df[
            (history_df['equipo_local'] == home_team_id) | 
            (history_df['equipo_visitante'] == home_team_id)
        ].tail(15)
        
        if not home_team_all_hist.empty:
            scored_in_game = np.where(
                home_team_all_hist['equipo_local'] == home_team_id, 
                home_team_all_hist['home_yrfi_target'], 
                home_team_all_hist['away_yrfi_target']
            )
            local_anota_ult15_count = int(np.sum(scored_in_game))
            local_juegos_ult15_count = len(home_team_all_hist)
            local_pct_anota_1inn_ult15 = np.mean(scored_in_game)
            ratio_local_pct_anota_1inn_ult15 = f"{local_anota_ult15_count}/{local_juegos_ult15_count}"
        else:
            local_pct_anota_1inn_ult15 = (league_avg_home_score_pct + league_avg_away_score_pct) / 2
            ratio_local_pct_anota_1inn_ult15 = "0/0"

        # --- Features del Equipo Visitante ---
        away_team_id = current_game['equipo_visitante']
        
        # Estadísticas como visitante
        away_team_as_away_hist = history_df[history_df['equipo_visitante'] == away_team_id]
        if not away_team_as_away_hist.empty:
            visit_anota_visit_count = away_team_as_away_hist['away_yrfi_target'].sum()
            visit_juegos_visit_count = len(away_team_as_away_hist)
            visit_pct_anota_1inn_visit = safe_division(visit_anota_visit_count, visit_juegos_visit_count)
            ratio_visit_pct_anota_1inn_visit = f"{int(visit_anota_visit_count)}/{visit_juegos_visit_count}"
        else:
            visit_pct_anota_1inn_visit = league_avg_away_score_pct
            ratio_visit_pct_anota_1inn_visit = "0/0"

        # Últimos 15 juegos (local o visitante)
        away_team_all_hist = history_df[
            (history_df['equipo_local'] == away_team_id) | 
            (history_df['equipo_visitante'] == away_team_id)
        ].tail(15)
        
        if not away_team_all_hist.empty:
            scored_in_game_away = np.where(
                away_team_all_hist['equipo_local'] == away_team_id, 
                away_team_all_hist['home_yrfi_target'], 
                away_team_all_hist['away_yrfi_target']
            )
            visit_anota_ult15_count = int(np.sum(scored_in_game_away))
            visit_juegos_ult15_count = len(away_team_all_hist)
            visit_pct_anota_1inn_ult15 = np.mean(scored_in_game_away)
            ratio_visit_pct_anota_1inn_ult15 = f"{visit_anota_ult15_count}/{visit_juegos_ult15_count}"
        else:
            visit_pct_anota_1inn_ult15 = (league_avg_home_score_pct + league_avg_away_score_pct) / 2
            ratio_visit_pct_anota_1inn_ult15 = "0/0"

        # --- Features del Pitcher Local ---
        home_pitcher_id = current_game['pitcher_local_id']
        pitcher_local_pct_permite_carrera = league_avg_pitcher_allow_pct
        pitcher_local_pct_permite_carrera_suavizado = league_avg_pitcher_allow_pct
        ratio_pitcher_local_pct_permite_carrera = "0/0"
        
        if home_pitcher_id:
            hp_hist = history_df[
                (history_df['pitcher_local_id'] == home_pitcher_id) | 
                (history_df['pitcher_visit_id'] == home_pitcher_id)
            ]
            if not hp_hist.empty:
                runs_allowed = np.where(
                    hp_hist['pitcher_local_id'] == home_pitcher_id,
                    hp_hist['away_yrfi_target'],
                    hp_hist['home_yrfi_target']
                )
                hp_runs_allowed_count = int(np.sum(runs_allowed))
                hp_games_count = len(hp_hist)
                pitcher_local_pct_permite_carrera = np.mean(runs_allowed)
                pitcher_local_pct_permite_carrera_suavizado = bayesian_smoothing(
                    value=pitcher_local_pct_permite_carrera, 
                    sample_size=hp_games_count,
                    global_mean=league_avg_pitcher_allow_pct, 
                    K=K_smoothing
                )
                ratio_pitcher_local_pct_permite_carrera = f"{hp_runs_allowed_count}/{hp_games_count}"

        # --- Features del Pitcher Visitante ---
        away_pitcher_id = current_game['pitcher_visit_id']
        pitcher_visit_pct_permite_carrera = league_avg_pitcher_allow_pct
        pitcher_visit_pct_permite_carrera_suavizado = league_avg_pitcher_allow_pct
        ratio_pitcher_visit_pct_permite_carrera = "0/0"

        if away_pitcher_id:
            ap_hist = history_df[
                (history_df['pitcher_local_id'] == away_pitcher_id) | 
                (history_df['pitcher_visit_id'] == away_pitcher_id)
            ]
            if not ap_hist.empty:
                runs_allowed = np.where(
                    ap_hist['pitcher_local_id'] == away_pitcher_id,
                    ap_hist['away_yrfi_target'],
                    ap_hist['home_yrfi_target']
                )
                ap_runs_allowed_count = int(np.sum(runs_allowed))
                ap_games_count = len(ap_hist)
                pitcher_visit_pct_permite_carrera = np.mean(runs_allowed)
                pitcher_visit_pct_permite_carrera_suavizado = bayesian_smoothing(
                    value=pitcher_visit_pct_permite_carrera, 
                    sample_size=ap_games_count,
                    global_mean=league_avg_pitcher_allow_pct, 
                    K=K_smoothing
                )
                ratio_pitcher_visit_pct_permite_carrera = f"{ap_runs_allowed_count}/{ap_games_count}"

        # --- Ensamblar la fila de datos ---
        row = {
            # Identificadores
            'id_partido': current_game['id_partido'],
            'fecha': current_game['fecha'],
            'equipo_local': current_game['equipo_local'],
            'equipo_visitante': current_game['equipo_visitante'],
            
            # Estadísticas del equipo local
            'ratio_local_pct_anota_1inn_local': ratio_local_pct_anota_1inn_local,
            'local_pct_anota_1inn_local': local_pct_anota_1inn_local,
            'ratio_local_pct_anota_1inn_ult15': ratio_local_pct_anota_1inn_ult15,
            'local_pct_anota_1inn_ult15': local_pct_anota_1inn_ult15,
            
            # Estadísticas del equipo visitante
            'ratio_visit_pct_anota_1inn_visit': ratio_visit_pct_anota_1inn_visit,
            'visit_pct_anota_1inn_visit': visit_pct_anota_1inn_visit,
            'ratio_visit_pct_anota_1inn_ult15': ratio_visit_pct_anota_1inn_ult15,
            'visit_pct_anota_1inn_ult15': visit_pct_anota_1inn_ult15,
            
            # Estadísticas del lanzador local
            'ratio_pitcher_local_pct_permite_carrera': ratio_pitcher_local_pct_permite_carrera,
            'pitcher_local_pct_permite_carrera': pitcher_local_pct_permite_carrera,
            'pitcher_local_pct_permite_carrera_suavizado': pitcher_local_pct_permite_carrera_suavizado,
            
            # Estadísticas del lanzador visitante
            'ratio_pitcher_visit_pct_permite_carrera': ratio_pitcher_visit_pct_permite_carrera,
            'pitcher_visit_pct_permite_carrera': pitcher_visit_pct_permite_carrera,
            'pitcher_visit_pct_permite_carrera_suavizado': pitcher_visit_pct_permite_carrera_suavizado,
            
            # Variables objetivo
            'home_yrfi_target': current_game['home_yrfi_target'],
            'away_yrfi_target': current_game['away_yrfi_target'],
            'game_yrfi_target': current_game['game_yrfi_target']
        }
        processed_rows.append(row)

    return pd.DataFrame(processed_rows)

def main():
    """Función principal."""
    print("=== Generador de Dataset YRFI ===\n")
    
    # Cargar datos
    season_data = load_season_data(SEASON_DATA_PATH)
    if not season_data:
        print("No se pudieron cargar los datos de la temporada.")
        return
    
    # Procesar datos
    print("\nProcesando datos...")
    K_SMOOTHING = 20  # Factor de suavizado bayesiano
    dataset = process_season_data(season_data, K_smoothing=K_SMOOTHING)
    
    if dataset.empty:
        print("No se generaron datos. Verifica los datos de entrada.")
        return
    
    # Guardar resultados
    output_file = OUTPUT_DIR / 'yrfi_ml_dataset.csv'
    dataset.to_csv(output_file, index=False)
    
    print(f"\n✅ Dataset generado exitosamente en: {output_file}")
    print(f"Número de partidos procesados: {len(dataset)}")
    print("\nResumen de las primeras filas:")
    print(dataset.head())
    
    # Mostrar estadísticas básicas
    print("\nEstadísticas de las variables numéricas:")
    print(dataset.select_dtypes(include=[np.number]).describe())

if __name__ == "__main__":
    main()
