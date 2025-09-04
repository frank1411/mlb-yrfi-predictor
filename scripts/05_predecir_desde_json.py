import json
import pandas as pd
import numpy as np
import os
import joblib
from xgboost import XGBClassifier

# ==============================================================================
# --- CONFIGURACIÓN DE PARÁMETROS DE MODELADO Y PREDICCIÓN ---
# ==============================================================================
# Estos son los umbrales ÓPTIMOS que encontraste en tu análisis
THRESHOLDS = {
    'partido': 0.48,
    'local': 0.50,
    'visitante': 0.48
}

# Constante de suavizado (debe coincidir con la usada para crear el dataset)
K_SMOOTHING_CONSTANT = 5

# Características para cada modelo (ajustadas a los modelos reales)
FEATURES_GAME = [
    'local_pct_anota_1inn_local',
    'pitcher_visit_pct_permite_carrera_suavizado',
    'pitcher_local_pct_permite_carrera_suavizado',
    'visit_pct_anota_1inn_ult15',
    'visit_pct_anota_1inn_visit',
    'local_pct_anota_1inn_ult15'
]

FEATURES_HOME_SCORING = [
    'local_pct_anota_1inn_local',
    'pitcher_visit_pct_permite_carrera_suavizado',
    'pitcher_local_pct_permite_carrera_suavizado',
    'visit_pct_anota_1inn_ult15',
    'visit_pct_anota_1inn_visit',
    'local_pct_anota_1inn_ult15'
]

FEATURES_AWAY_SCORING = [
    'local_pct_anota_1inn_local',
    'pitcher_visit_pct_permite_carrera_suavizado',
    'pitcher_local_pct_permite_carrera_suavizado',
    'visit_pct_anota_1inn_ult15',
    'visit_pct_anota_1inn_visit',
    'local_pct_anota_1inn_ult15'
]

# ==============================================================================
# --- FUNCIONES DE AYUDA ---
# ==============================================================================

def safe_division(numerator, denominator):
    return numerator / denominator if denominator != 0 else 0.0

def bayesian_smoothing(value, sample_size, global_mean, K):
    if sample_size == 0: return global_mean
    return (sample_size * value + K * global_mean) / (sample_size + K)

def parse_ratio(ratio_str):
    try:
        numerator, denominator = map(int, ratio_str.split('/'))
        return numerator, denominator
    except (ValueError, AttributeError):
        return 0, 0

# --- CONFIGURACIÓN ---
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
predictions_folder = os.path.join(script_dir, '../predictions')
models_folder = os.path.join(script_dir, '../models')

# --- SCRIPT PRINCIPAL DE PREDICCIÓN ---

def predict_daily_games(
    models_folder=models_folder,
    predictions_folder=predictions_folder
):
    """
    Entrena los modelos si no existen, o los carga, y predice los juegos del día.
    """
    os.makedirs(models_folder, exist_ok=True)
    model_paths = {
        'partido': os.path.join(models_folder, 'model_yrfi_partido.joblib'),
        'local': os.path.join(models_folder, 'model_yrfi_local.joblib'),
        'visitante': os.path.join(models_folder, 'model_yrfi_visitante.joblib')
    }

    # --- CARGA DE MODELOS ---
    print("1. Cargando modelos...")
    models = {}
    
    # Mapeo de modelos reales a los nombres usados en el script
    model_mapping = {
        'partido': '../models/modelo_yrfi.pkl',
        'local': '../models/modelo_local.pkl',
        'visitante': '../models/modelo_visitante.pkl'
    }
    
    # Cargar los modelos reales
    for name, path in model_mapping.items():
        try:
            if os.path.exists(path):
                models[name] = joblib.load(path)
                print(f"   - Modelo {name} cargado exitosamente desde {path}")
            else:
                print(f"   - Advertencia: No se encontró el modelo en {path}")
                raise FileNotFoundError(f"Modelo no encontrado: {path}")
        except Exception as e:
            print(f"   - Error cargando el modelo {name}: {str(e)}")
            print("   - Usando modelo dummy en su lugar")
            # Usar modelo dummy como respaldo
            class DummyModel:
                def predict_proba(self, X):
                    n_samples = X.shape[0]
                    prob_1 = np.random.uniform(0.3, 0.7, size=(n_samples, 1))
                    return np.hstack([1 - prob_1, prob_1])
            models[name] = DummyModel()

    # --- PROCESAMIENTO DE JUEGOS DEL DÍA ---
    print("\n2. Procesando juegos del día...")
    
    # Leer archivos JSON de predicción
    json_files = [f for f in os.listdir(predictions_folder) if f.endswith('.json')]
    if not json_files:
        print(f"No se encontraron archivos JSON en la carpeta '{predictions_folder}'.")
        return
    
    # Calcular promedios de la liga (puedes ajustar estos valores según tus datos)
    LEAGUE_AVG_YRFI = 0.45  # 45% de probabilidad de que un equipo anote en la primera entrada
    
    games_to_predict = []
    
    # Procesar cada archivo JSON
    for file_name in json_files:
        file_path = os.path.join(predictions_folder, file_name)
        try:
            with open(file_path, 'r') as f:
                game_data = json.load(f)
            
            # Extraer información básica del juego
            home_team_data = game_data.get('home_team', {})
            away_team_data = game_data.get('away_team', {})
            
            home_team = home_team_data.get('name', 'Equipo Local')
            away_team = away_team_data.get('name', 'Equipo Visitante')
            
            home_pitcher = home_team_data.get('pitcher', {}).get('name', 'Lanzador Local')
            away_pitcher = away_team_data.get('pitcher', {}).get('name', 'Lanzador Visitante')
            
            game_date = game_data.get('game_date', 'Fecha no disponible')
            
            # Extraer estadísticas de pitcheo
            home_pitcher_data = home_team_data.get('pitcher', {})
            away_pitcher_data = away_team_data.get('pitcher', {})
            
            # Obtener estadísticas de pitcheo
            pitcher_local_pct_permite_carrera = home_pitcher_data.get('yrfi_allowed', 30.0) / 100  # Convertir de porcentaje a decimal
            pitcher_visit_pct_permite_carrera = away_pitcher_data.get('yrfi_allowed', 30.0) / 100  # Convertir de porcentaje a decimal
            
            # Obtener el número de muestras del ratio (ej: '5/12' -> 12 muestras)
            def get_sample_size(ratio_str):
                try:
                    return int(ratio_str.split('/')[1])
                except (IndexError, AttributeError, ValueError):
                    return 0
            
            pitcher_local_muestras = get_sample_size(home_pitcher_data.get('yrfi_ratio', '0/1'))
            pitcher_visit_muestras = get_sample_size(away_pitcher_data.get('yrfi_ratio', '0/1'))
            
            # Obtener estadísticas de equipos
            home_stats = home_team_data.get('stats', {})
            away_stats = away_team_data.get('stats', {})
            
            home_base_stats = home_stats.get('base', {})
            home_tendency_stats = home_stats.get('tendency', {})
            away_base_stats = away_stats.get('base', {})
            away_tendency_stats = away_stats.get('tendency', {})
            
            # Suavizado bayesiano para estadísticas de pitcheo (usando la media global de 0.3 como prior)
            pitcher_local_pct_permite_carrera_suavizado = bayesian_smoothing(
                pitcher_local_pct_permite_carrera, 
                pitcher_local_muestras,
                0.3,  # Media global estimada
                K_SMOOTHING_CONSTANT
            )
            
            pitcher_visit_pct_permite_carrera_suavizado = bayesian_smoothing(
                pitcher_visit_pct_permite_carrera,
                pitcher_visit_muestras,
                0.3,  # Media global estimada
                K_SMOOTHING_CONSTANT
            )
            
            # Obtener estadísticas de anotación de equipos (convertir de porcentaje a decimal)
            local_pct_anota_1inn_local = home_base_stats.get('value', 30.0) / 100.0
            local_pct_anota_1inn_ult15 = home_tendency_stats.get('value', 30.0) / 100.0
            
            visit_pct_anota_1inn_visit = away_base_stats.get('value', 30.0) / 100.0
            visit_pct_anota_1inn_ult15 = away_tendency_stats.get('value', 30.0) / 100.0
            
            # Crear diccionario con características para el modelo
            features = {
                'game_pk': game_data.get('game_pk', 'N/A'),
                'game_date': game_date,
                'home_team_name': home_team,
                'away_team_name': away_team,
                'home_pitcher': home_pitcher,
                'away_pitcher': away_pitcher,
                'local_pct_anota_1inn_local': local_pct_anota_1inn_local,
                'pitcher_visit_pct_permite_carrera_suavizado': pitcher_visit_pct_permite_carrera_suavizado,
                'pitcher_local_pct_permite_carrera_suavizado': pitcher_local_pct_permite_carrera_suavizado,
                'visit_pct_anota_1inn_ult15': visit_pct_anota_1inn_ult15,
                'visit_pct_anota_1inn_visit': visit_pct_anota_1inn_visit,
                'local_pct_anota_1inn_ult15': local_pct_anota_1inn_ult15
            }
            games_to_predict.append(features)
            
        except Exception as e:
            print(f"Error procesando {file_name}: {str(e)}")

    # Verificar que tenemos juegos para predecir
    if not games_to_predict:
        print("No se encontraron juegos válidos para predecir.")
        return
        
    # Convertir a DataFrame
    X_test_df = pd.DataFrame(games_to_predict)
    
    # Verificar que tenemos las columnas necesarias
    required_columns = FEATURES_GAME + ['home_team_name', 'away_team_name', 'home_pitcher', 'away_pitcher', 'game_date']
    for col in required_columns:
        if col not in X_test_df.columns:
            print(f"Error: Falta la columna requerida: {col}")
            return

    # --- REALIZAR PREDICCIONES ---
    print("\n3. Procesando predicciones...")
    
    # Usar las probabilidades ya calculadas en los archivos JSON
    prob_game = []
    prob_local = []
    prob_away = []
    
    for file_name in json_files:
        file_path = os.path.join(predictions_folder, file_name)
        try:
            with open(file_path, 'r') as f:
                game_data = json.load(f)
                
            # Obtener las probabilidades ajustadas del JSON
            home_adjusted = game_data.get('prediction', {}).get('calculation', {}).get('home_team', {}).get('adjusted', 30.0) / 100.0
            away_adjusted = game_data.get('prediction', {}).get('calculation', {}).get('away_team', {}).get('adjusted', 30.0) / 100.0
            game_prob = game_data.get('prediction', {}).get('yrfi_probability', 50.0) / 100.0
            
            prob_local.append(home_adjusted)
            prob_away.append(away_adjusted)
            prob_game.append(game_prob)
            
        except Exception as e:
            print(f"Error procesando {file_name}: {str(e)}")
            # Usar valores por defecto si hay un error
            prob_local.append(0.3)
            prob_away.append(0.3)
            prob_game.append(0.5)
    
    # Convertir listas a arrays de NumPy
    prob_local_np = np.array(prob_local)
    prob_away_np = np.array(prob_away)
    prob_game_np = np.array(prob_game)
    
    # Almacenar las probabilidades
    X_test_df['prob_home_yrfi'] = prob_local_np
    X_test_df['prob_away_yrfi'] = prob_away_np
    X_test_df['prob_game_yrfi'] = prob_game_np
    
    # Tomar decisiones basadas en los umbrales
    X_test_df['decision_home'] = np.where(prob_local_np > THRESHOLDS['local'], 'SÍ', 'NO')
    X_test_df['decision_away'] = np.where(prob_away_np > THRESHOLDS['visitante'], 'SÍ', 'NO')
    X_test_df['decision_game'] = np.where(prob_game_np > THRESHOLDS['partido'], 'SÍ (YRFI)', 'NO (NRFI)')
    
    # --- PRESENTAR REPORTE FINAL ---
    print("\n" + "="*80)
    print("       🚀 PREDICCIONES DE YRFI PARA LOS JUEGOS DE HOY 🚀".center(80))
    print("="*80)
    
    # Ordenar por la probabilidad del YRFI de partido para ver los más interesantes primero
    for i, row in X_test_df.sort_values('prob_game_yrfi', ascending=False).iterrows():
        print(f"\n{' FECHA: ' + row.get('game_date', 'N/A')} ".ljust(80, '-'))
        print(f"🔵 {row['away_team_name']} @ {row['home_team_name']} 🔴")
        print("-"*80)
        print(f"🎯 PARTIDO YRFI:   {row['prob_game_yrfi']*100:.1f}% | Umbral: {THRESHOLDS['partido']} | {row['decision_game']}")
        print(f"   🏠 LOCAL:       {row['prob_home_yrfi']*100:.1f}% | Umbral: {THRESHOLDS['local']} | {row['decision_home']}")
        print(f"   🏃 VISITANTE:   {row['prob_away_yrfi']*100:.1f}% | Umbral: {THRESHOLDS['visitante']} | {row['decision_away']}")
        print("-"*80)
        print("💡 Recomendación:")
        if row['decision_game'] == 'SÍ (YRFI)':
            print(f"   - Considera una apuesta a YRFI (ambos equipos anotan en la 1ra entrada)")
        if row['decision_home'] == 'SÍ':
            print(f"   - El equipo local ({row['home_team_name']}) tiene alta probabilidad de anotar")
        if row['decision_away'] == 'SÍ':
            print(f"   - El equipo visitante ({row['away_team_name']}) tiene alta probabilidad de anotar")
        if row['decision_game'] != 'SÍ (YRFI)' and row['decision_home'] != 'SÍ' and row['decision_away'] != 'SÍ':
            print("   - No se recomiendan apuestas para este partido según los umbrales actuales")
            
        print("\n" + "-"*80)
    
    # Generar reporte en markdown
    generar_reporte_markdown(X_test_df)

# --- OBTENER ARCHIVOS JSON ---
print("\n3. Procesando predicciones...")
    
# Obtener la lista de archivos JSON en el directorio de predicciones
json_files = [f for f in os.listdir(predictions_folder) if f.endswith('.json') and f.startswith('yrfi_')]

if not json_files:
    print("No se encontraron archivos de predicción en el directorio.")
    exit(1)

print(f"Se encontraron {len(json_files)} archivos de predicción.")

# Listas para almacenar predicciones de todos los juegos
all_games_data = []
    
# Procesar cada archivo JSON
for file_name in json_files:
    file_path = os.path.join(predictions_folder, file_name)
    try:
        with open(file_path, 'r') as f:
            game_data = json.load(f)
            
        # Extraer información del juego
        game_info = {
            'game_pk': game_data.get('game_pk', ''),
            'game_date': game_data.get('game_date', ''),
            'home_team_name': game_data.get('home_team', {}).get('name', 'Equipo Local'),
            'away_team_name': game_data.get('away_team', {}).get('name', 'Equipo Visitante'),
            'home_pitcher': game_data.get('home_team', {}).get('pitcher', {}).get('name', 'Lanzador Local'),
            'away_pitcher': game_data.get('away_team', {}).get('pitcher', {}).get('name', 'Lanzador Visitante'),
            'prob_home_yrfi': game_data.get('prediction', {}).get('calculation', {}).get('home_team', {}).get('adjusted', 30.0) / 100.0,
            'prob_away_yrfi': game_data.get('prediction', {}).get('calculation', {}).get('away_team', {}).get('adjusted', 30.0) / 100.0,
            'prob_game_yrfi': game_data.get('prediction', {}).get('yrfi_probability', 50.0) / 100.0
        }
        
        all_games_data.append(game_info)
        
    except Exception as e:
        print(f"Error procesando {file_name}: {str(e)}")
        continue

# Convertir a DataFrame
X_test_df = pd.DataFrame(all_games_data)

# Verificar que tenemos datos para procesar
if X_test_df.empty:
    print("No se pudo cargar ningún juego válido.")
    exit(1)

# Tomar decisiones basadas en los umbrales
X_test_df['decision_home'] = np.where(X_test_df['prob_home_yrfi'] > THRESHOLDS['local'], 'SÍ', 'NO')
X_test_df['decision_away'] = np.where(X_test_df['prob_away_yrfi'] > THRESHOLDS['visitante'], 'SÍ', 'NO')
X_test_df['decision_game'] = np.where(X_test_df['prob_game_yrfi'] > THRESHOLDS['partido'], 'SÍ (YRFI)', 'NO (NRFI)')
def generar_reporte_markdown(X_test_df, predictions_folder=None):
    """
    Genera un archivo markdown con el resumen de predicciones en el formato especificado.
    """
    from datetime import datetime
    
    # Usar el directorio de trabajo actual si no se especifica uno
    if predictions_folder is None:
        predictions_folder = os.path.join(os.getcwd(), 'predictions')
    
    # Asegurar que el directorio de salida exista
    os.makedirs(predictions_folder, exist_ok=True)
    
    # Crear nombre del archivo con la fecha actual
    fecha_actual = datetime.now().strftime("%d%m%Y")
    nombre_archivo = os.path.join(predictions_folder, f'predicciones_ML_{fecha_actual}.md')
    
    print(f"\n📁 Guardando reporte en: {os.path.abspath(nombre_archivo)}")
    
    # Ordenar por probabilidad de juego
    df_sorted = X_test_df.sort_values('prob_game_yrfi', ascending=False)
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        # Encabezado
        f.write("# 🚀 PREDICCIONES YRFI - MLB\n\n")
        fecha_bonita = datetime.now().strftime("%d/%m/%Y")
        f.write(f"## 📅 Fecha: {fecha_bonita}\n\n")
        
        # Sección 1: Resumen de predicciones
        f.write("## 📊 RESUMEN DE PREDICCIONES\n\n")
        f.write("### 🔝 MEJORES APUESTAS\n\n")
        
        # Tabla de mejores apuestas
        f.write("| Partido | Prob. YRFI | Recomendación |\n")
        f.write("|---------|------------|---------------|\n")
        
        for _, row in df_sorted.iterrows():
            local = row['home_team_name']
            visitante = row['away_team_name']
            prob = row['prob_game_yrfi'] * 100
            
            if prob >= 52:
                recomendacion = "✅ APUESTA"
            elif prob >= 48:
                recomendacion = "🟡 CERCANO"
            else:
                recomendacion = "❌ NO APUESTA"
                
            f.write(f"| {local} vs {visitante} | {prob:.1f}% | {recomendacion} |\n")
        
        # Sección 2: Mejores equipos para YRFI
        f.write("\n## ⚾ EQUIPOS CON MAYOR PROBABILIDAD DE ANOTAR EN 1RA ENTRADA\n\n")
        
        # Crear lista de equipos con sus probabilidades
        equipos = []
        for _, row in df_sorted.iterrows():
            equipos.append({
                'Equipo': row['home_team_name'],
                'Prob. Anotar': row['prob_home_yrfi'] * 100,
                'Local/Visitante': '🏠 Local'
            })
            equipos.append({
                'Equipo': row['away_team_name'],
                'Prob. Anotar': row['prob_away_yrfi'] * 100,
                'Local/Visitante': '✈️ Visitante'
            })
        
        # Ordenar equipos por probabilidad
        equipos_ordenados = sorted(equipos, key=lambda x: x['Prob. Anotar'], reverse=True)
        
        # Tabla de equipos
        f.write("| Equipo | Prob. Anotar | Condición |\n")
        f.write("|--------|--------------|-----------|\n")
        
        for equipo in equipos_ordenados:
            prob = equipo['Prob. Anotar']
            if prob >= 50:
                condicion = "✅ Alta"
            elif prob >= 40:
                condicion = "🟡 Media"
            else:
                condicion = "🔴 Baja"
                
            f.write(f"| {equipo['Equipo']} | {prob:.1f}% | {equipo['Local/Visitante']} {condicion} |\n")
        
        # Sección 3: Análisis detallado por partido
        f.write("\n## 🔍 ANÁLISIS DETALLADO POR PARTIDO\n\n")
        
        for _, row in df_sorted.iterrows():
            local = row['home_team_name']
            visitante = row['away_team_name']
            prob_local = row['prob_home_yrfi'] * 100
            prob_visitante = row['prob_away_yrfi'] * 100
            prob_partido = row['prob_game_yrfi'] * 100
            
            f.write(f"### {local} vs {visitante}\n")
            f.write(f"- **Probabilidad YRFI:** {prob_partido:.1f}%\n")
            f.write(f"- **{local} (Local):** {prob_local:.1f}%\n")
            f.write(f"- **{visitante} (Visitante):** {prob_visitante:.1f}%\n\n")
            
            # Recomendación
            if prob_partido >= 52:
                f.write("**Recomendación:** ✅ APUESTA ALTA\n\n")
            elif prob_partido >= 48:
                f.write("**Recomendación:** 🟡 APUESTA CON PRECAUCIÓN\n\n")
            else:
                f.write("**Recomendación:** ❌ NO RECOMENDADO\n\n")
        
        # Pie de página
        f.write("---\n")
        f.write("*Nota: Las predicciones están basadas en datos históricos y modelos estadísticos.\n")
        f.write("Siempre considera otros factores antes de realizar apuestas.*\n")
    
    print(f"\n✅ Reporte generado exitosamente: {nombre_archivo}")
    return nombre_archivo

if __name__ == "__main__":
    predict_daily_games()