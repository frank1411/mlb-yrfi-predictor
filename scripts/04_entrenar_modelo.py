#!/usr/bin/env python3
"""
Script para entrenar un modelo de predicción YRFI (Yes Run First Inning).
Incluye funcionalidad de backtesting y evaluación de resultados.
"""
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score, make_scorer, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import joblib
import xgboost as xgb
from xgboost import XGBClassifier
from datetime import datetime, timedelta
import warnings
from tqdm import tqdm
from scipy.stats import uniform, randint
warnings.filterwarnings('ignore')

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'ml_datasets'
MODELS_DIR = PROJECT_ROOT / 'models'
OUTPUT_DIR = PROJECT_ROOT / 'evaluation'

# Configuración
warnings.filterwarnings('ignore')
RANDOM_STATE = 42
DECISION_THRESHOLD = 0.35  # Umbral para la decisión de predicciones

# Crear directorios necesarios
MODELS_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Configuración de parámetros
WARMUP_DAYS = 30  # Días iniciales para entrenamiento inicial

# Características específicas para cada modelo
FEATURES_HOME_SCORING = [
    'local_pct_anota_1inn_local',  # Porcentaje de veces que el equipo local anota en la 1ra entrada
    'local_pct_anota_1inn_ult15',  # Porcentaje de las últimas 15 veces que el equipo local anotó en la 1ra
    'pitcher_visit_pct_permite_carrera_suavizado'  # Porcentaje suavizado de carreras permitidas por el lanzador visitante
]

FEATURES_AWAY_SCORING = [
    'visit_pct_anota_1inn_visit',  # Porcentaje de veces que el equipo visitante anota en la 1ra entrada
    'visit_pct_anota_1inn_ult15',  # Porcentaje de las últimas 15 veces que el equipo visitante anotó en la 1ra
    'pitcher_local_pct_permite_carrera_suavizado'  # Porcentaje suavizado de carreras permitidas por el lanzador local
]

# Para el modelo de partido completo, usamos todas las características
FEATURES_GAME = list(set(FEATURES_HOME_SCORING + FEATURES_AWAY_SCORING))

# Mapeo de características por tipo de modelo
FEATURES = {
    'home': FEATURES_HOME_SCORING,
    'away': FEATURES_AWAY_SCORING,
    'game': FEATURES_GAME
}

def load_data():
    """Carga y prepara los datos para el modelo."""
    print("\n=== Cargando datos ===")
    try:
        # Cargar el dataset
        df = pd.read_csv(DATA_DIR / 'yrfi_ml_dataset.csv')
        
        # Convertir fechas
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('fecha').reset_index(drop=True)
        
        # Renombrar columnas si es necesario
        if 'game_yrfi_target' in df.columns and 'game_yrfi_real' not in df.columns:
            df = df.rename(columns={'game_yrfi_target': 'game_yrfi_real'})
        
        # Verificar columnas requeridas
        all_features = list(set(FEATURES['home'] + FEATURES['away'] + FEATURES['game']))
        required_columns = set(all_features + 
                             ['fecha', 'id_partido', 'home_yrfi_target', 'away_yrfi_target', 'game_yrfi_real',
                              'equipo_local', 'equipo_visitante'])
        
        # Verificar columnas faltantes
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            print(f"Advertencia: Faltan columnas en el dataset: {missing_columns}")
            print("Se intentará continuar con las columnas disponibles...")
            
            # Eliminar las columnas faltantes de las características
            for model_type in ['home', 'away', 'game']:
                FEATURES[model_type] = [col for col in FEATURES[model_type] if col in df.columns]
        
        # Seleccionar solo las columnas que vamos a usar
        columns_to_keep = list(set(all_features + 
                                 ['fecha', 'id_partido', 'home_yrfi_target', 'away_yrfi_target', 'game_yrfi_real',
                                  'equipo_local', 'equipo_visitante']))
        
        # Filtrar el dataframe para mantener solo las columnas necesarias
        df = df[columns_to_keep].copy()
        
        # Verificar que las columnas sean numéricas
        for col in FEATURES['home'] + FEATURES['away']:
            if col in df.columns:
                # Convertir a numérico, forzando los errores a NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Rellenar valores faltantes con la mediana
                if df[col].isna().any():
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                    
                    print(f"Advertencia: Se rellenaron {df[col].isna().sum()} valores faltantes en {col} con la mediana")
        
        # Verificar valores faltantes en columnas numéricas
        feature_columns = list(set(FEATURES['home'] + FEATURES['away']))
        missing_values = df[feature_columns].isnull().sum()
        
        if missing_values.any() and missing_values.any() > 0:
            print("\nAdvertencia: Se encontraron valores faltantes después de la conversión:")
            for col, count in missing_values[missing_values > 0].items():
                print(f"- {col}: {count} valores faltantes")
        else:
            print("\nTodas las columnas numéricas se han procesado correctamente sin valores faltantes.")
        
        # Eliminar filas con valores faltantes en las columnas objetivo
        target_columns = ['home_yrfi_target', 'away_yrfi_target', 'game_yrfi_real']
        initial_count = len(df)
        df = df.dropna(subset=target_columns)
        if len(df) < initial_count:
            print(f"\nSe eliminaron {initial_count - len(df)} filas con valores faltantes en las columnas objetivo.")
        
        return df
        
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def train_model(X_train, y_train, model_type='game'):
    """
    Entrena un modelo XGBoost con búsqueda de hiperparámetros.
    
    Args:
        X_train: DataFrame con características de entrenamiento
        y_train: Series con variable objetivo
        model_type: Tipo de modelo ('game', 'home' o 'away')
        
    Returns:
        Mejor modelo encontrado
    """
    print(f"\n=== Entrenando modelo {model_type.upper()} ===")
    print(f"Características utilizadas: {X_train.columns.tolist()}")
    print(f"Tamaño del conjunto de entrenamiento: {len(X_train)} muestras")
    print(f"Distribución de clases: {y_train.value_counts().to_dict()}")
    
    # Identificar columnas numéricas y categóricas
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Preprocesamiento para características numéricas
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Preprocesamiento para características categóricas
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combinar preprocesadores
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Crear pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(
            objective='binary:logistic',
            eval_metric='logloss',
            use_label_encoder=False,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            scale_pos_weight=len(y_train[y_train==0])/len(y_train[y_train==1]) if len(y_train[y_train==1]) > 0 else 1
        ))
    ])
    
    # Configuración de hiperparámetros según el tipo de modelo
    if model_type == 'game':
        # Para el modelo de partido completo (YRFI)
        param_dist = {
            'classifier__n_estimators': [200, 300, 400],
            'classifier__max_depth': [4, 5, 6],
            'classifier__learning_rate': [0.05, 0.1, 0.15],
            'classifier__subsample': [0.8, 0.9, 1.0],
            'classifier__colsample_bytree': [0.8, 0.9, 1.0],
            'classifier__gamma': [0, 0.1, 0.2],
            'classifier__min_child_weight': [1, 2, 3]
        }
        scoring = 'f1'  # Buscamos un buen balance entre precisión y recall
    else:
        # Para modelos individuales (local/visitante)
        param_dist = {
            'classifier__n_estimators': [100, 200, 300],
            'classifier__max_depth': [3, 4, 5],
            'classifier__learning_rate': [0.1, 0.2, 0.3],
            'classifier__subsample': [0.6, 0.7, 0.8],
            'classifier__colsample_bytree': [0.6, 0.7, 0.8],
            'classifier__gamma': [0, 0.1, 0.2],
            'classifier__min_child_weight': [1, 2]
        }
        scoring = 'f1_macro'  # Para manejar mejor el desbalance de clases
    
    # Configurar validación cruzada estratificada
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    
    # Configurar búsqueda aleatoria
    random_search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_dist,
        scoring=scoring,  # Usamos la métrica definida según el tipo de modelo
        n_iter=30,  # Aumentar iteraciones para mejor búsqueda
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
        verbose=2,  # Más información durante el entrenamiento
        n_jobs=-1,
        random_state=RANDOM_STATE
    )
    
    # Ejecutar búsqueda
    print(f"Iniciando búsqueda de hiperparámetros para {model_type}...")
    random_search.fit(X_train, y_train)
    
    # Mostrar resultados
    print(f"\nMejores parámetros para {model_type}:")
    for param, value in random_search.best_params_.items():
        print(f"{param}: {value}")
    
    print(f"\nMejor puntuación (F1): {random_search.best_score_:.4f}")
    
    return random_search.best_estimator_

def run_prediction_backtest(df):
    """
    Ejecuta el bucle de backtesting a lo largo de la temporada.
    """
    print("\n=== Iniciando Backtesting ===")
    
    # Convertir fechas a datetime y ordenar
    df['fecha_dt'] = pd.to_datetime(df['fecha'])
    df = df.sort_values('fecha_dt')
    
    # Obtener fechas únicas ordenadas
    fechas_unicas = df['fecha_dt'].unique()
    
    if len(fechas_unicas) <= WARMUP_DAYS:
        print(f"No hay suficientes datos para el período de calentamiento de {WARMUP_DAYS} días.")
        return pd.DataFrame()
    
    # Lista para almacenar resultados de cada día
    resultados = []
    
    # Inicializar modelos
    modelo_yrfi = None
    modelo_local = None
    modelo_visitante = None
    
    # Bucle principal de backtesting
    for i in tqdm(range(WARMUP_DAYS, len(fechas_unicas)), desc="Procesando días"):
        fecha_actual = fechas_unicas[i]
        
        # Filtrar datos históricos hasta el día anterior
        datos_historicos = df[df['fecha_dt'] < fecha_actual].copy()
        
        # Si es el primer día después del período de calentamiento o si no hay modelos
        if i == WARMUP_DAYS or modelo_yrfi is None:
            # Preparar datos para cada modelo
            # 1. Modelo de partido completo (YRFI)
            X_train_yrfi = datos_historicos[FEATURES['game']]
            y_train_yrfi = datos_historicos['game_yrfi_real']
            
            # 2. Modelo de anotación local
            X_train_local = datos_historicos[FEATURES['home']]
            y_train_local = datos_historicos['home_yrfi_target']
            
            # 3. Modelo de anotación visitante
            X_train_visitante = datos_historicos[FEATURES['away']]
            y_train_visitante = datos_historicos['away_yrfi_target']
            
            # Entrenar modelos con sus respectivas características
            print("\nEntrenando modelo YRFI...")
            modelo_yrfi = train_model(X_train_yrfi, y_train_yrfi, 'game')
            
            print("\nEntrenando modelo de anotación local...")
            modelo_local = train_model(X_train_local, y_train_local, 'home')
            
            print("\nEntrenando modelo de anotación visitante...")
            modelo_visitante = train_model(X_train_visitante, y_train_visitante, 'away')
            
            # Guardar los modelos
            joblib.dump(modelo_yrfi, MODELS_DIR / 'modelo_yrfi.pkl')
            joblib.dump(modelo_local, MODELS_DIR / 'modelo_local.pkl')
            joblib.dump(modelo_visitante, MODELS_DIR / 'modelo_visitante.pkl')
        
        # Filtrar partidos del día actual
        partidos_hoy = df[df['fecha_dt'] == fecha_actual].copy()
        
        if len(partidos_hoy) == 0:
            continue
            
        try:
            # Predecir para el día actual con los modelos correspondientes
            # 1. Predecir YRFI completo
            features_disponibles = [f for f in FEATURES['game'] if f in partidos_hoy.columns]
            X_hoy_yrfi = partidos_hoy[features_disponibles]
            prob_yrfi = modelo_yrfi.predict_proba(X_hoy_yrfi)[:, 1]
            
            # 2. Predecir anotación local
            features_disponibles = [f for f in FEATURES['home'] if f in partidos_hoy.columns]
            X_hoy_local = partidos_hoy[features_disponibles]
            prob_local = modelo_local.predict_proba(X_hoy_local)[:, 1]
            
            # 3. Predecir anotación visitante
            features_disponibles = [f for f in FEATURES['away'] if f in partidos_hoy.columns]
            X_hoy_visitante = partidos_hoy[features_disponibles]
            prob_visitante = modelo_visitante.predict_proba(X_hoy_visitante)[:, 1]
            
        except Exception as e:
            print(f"Error al hacer predicciones para {fecha_actual}: {str(e)}")
            continue
        
        # Almacenar resultados
        for idx, (_, partido) in enumerate(partidos_hoy.iterrows()):
            resultados.append({
                'fecha': fecha_actual,
                'id_partido': partido['id_partido'],
                'equipo_local': partido['equipo_local'],
                'equipo_visitante': partido['equipo_visitante'],
                'prob_yrfi_predicha': prob_yrfi[idx],
                'prob_local_anota': prob_local[idx],
                'prob_visitante_anota': prob_visitante[idx],
                'game_yrfi_real': partido['game_yrfi_real'],
                'home_yrfi_target': partido['home_yrfi_target'],
                'away_yrfi_target': partido['away_yrfi_target']
            })
        
        # Reentrenar modelos periódicamente (semanalmente)
        if i % 7 == 0:
            X_train = datos_historicos.drop(columns=['fecha', 'fecha_dt', 'id_partido', 'equipo_local', 'equipo_visitante', 
                                                   'home_yrfi_target', 'away_yrfi_target', 'game_yrfi_real'])
            y_train_yrfi = datos_historicos['game_yrfi_real']
            y_train_local = datos_historicos['home_yrfi_target']
            y_train_visitante = datos_historicos['away_yrfi_target']
            
            modelo_yrfi = train_model(X_train, y_train_yrfi)
            modelo_local = train_model(X_train, y_train_local)
            modelo_visitante = train_model(X_train, y_train_visitante)
            
            # Guardar los modelos actualizados
            joblib.dump(modelo_yrfi, MODELS_DIR / 'modelo_yrfi.pkl')
            joblib.dump(modelo_local, MODELS_DIR / 'modelo_local.pkl')
            joblib.dump(modelo_visitante, MODELS_DIR / 'modelo_visitante.pkl')
    
    # Convertir resultados a DataFrame
    if not resultados:
        print("No se generaron resultados.")
        return pd.DataFrame()
    
    resultados_df = pd.DataFrame(resultados)
    
    # Eliminar columna temporal si existe
    if 'fecha_dt' in df.columns:
        df.drop(columns=['fecha_dt'], inplace=True)
    
    return resultados_df

def evaluate_predictions(df, threshold, output_file):
    """Evalúa las predicciones y muestra métricas para los tres tipos de YRFI."""
    # Hacer copia para no modificar el DataFrame original
    eval_df = df.copy()
    
    # Aplicar umbral a las tres predicciones
    eval_df['prediccion_yrfi'] = (eval_df['prob_yrfi_predicha'] >= threshold).astype(int)
    eval_df['prediccion_local'] = (eval_df['prob_local_anota'] >= threshold).astype(int)
    eval_df['prediccion_visitante'] = (eval_df['prob_visitante_anota'] >= threshold).astype(int)
    
    # Filtrar solo los partidos con predicción YRFI
    pred_df = eval_df[eval_df['prediccion_yrfi'] == 1].copy()
    
    # Calcular métricas generales
    total_games = len(eval_df)
    predicted_games = len(pred_df)
    
    # Calcular aciertos para cada tipo de predicción
    correct_yrfi = pred_df['game_yrfi_real'].sum()
    correct_local = (eval_df['home_yrfi_target'] == eval_df['prediccion_local']).sum()
    correct_visitante = (eval_df['away_yrfi_target'] == eval_df['prediccion_visitante']).sum()
    
    # Calcular precisiones
    precision_yrfi = correct_yrfi / predicted_games if predicted_games > 0 else 0
    precision_local = correct_local / total_games
    precision_visitante = correct_visitante / total_games
    
    # Calcular rentabilidades (asumiendo cuota fija de 1.90)
    profit_yrfi = (correct_yrfi * 0.90) - (predicted_games - correct_yrfi) * 1
    roi_yrfi = (profit_yrfi / predicted_games) * 100 if predicted_games > 0 else 0
    
    # Imprimir informe detallado
    print("\n" + "="*60)
    print(f"                 EVALUACIÓN CON UMBRAL {threshold:.2f}                 ")
    print("="*60)
    print(f"Período: {eval_df['fecha'].min().date()} - {eval_df['fecha'].max().date()}")
    print(f"Total de partidos evaluados: {total_games}")
    print(f"Umbral de decisión: {threshold:.2f}\n")
    
    print("1. PREDICCIÓN YRFI (PARTIDO COMPLETO):")
    print(f"   - Predicciones realizadas: {predicted_games} ({predicted_games/total_games*100:.1f}% de los partidos)")
    print(f"   - Aciertos: {correct_yrfi} de {predicted_games} ({precision_yrfi*100:.1f}% de precisión)")
    print(f"   - Rentabilidad: {roi_yrfi:.1f}% (asumiendo cuota de 1.90)\n")
    
    print("2. PREDICCIÓN YRFI LOCAL:")
    print(f"   - Precisión: {precision_local*100:.1f}% ({correct_local} de {total_games} partidos)")
    
    print("3. PREDICCIÓN YRFI VISITANTE:")
    print(f"   - Precisión: {precision_visitante*100:.1f}% ({correct_visitante} de {total_games} partidos)\n")
    
    print("-"*60)
    print("                     REPORTE DETALLADO                      ")
    print("-"*60)
    
    # Mostrar métricas de clasificación para YRFI completo
    y_true = eval_df['game_yrfi_real']
    y_pred = eval_df['prediccion_yrfi']
    
    # Calcular métricas de clasificación
    if len(set(y_true)) > 1:  # Asegurarse de que hay al menos dos clases
        print("\nMétricas para YRFI (Partido Completo):")
        print(classification_report(y_true, y_pred, target_names=['NRFI', 'YRFI']))
    else:
        print("No hay suficientes clases para calcular métricas de clasificación")
    
    # Columnas a guardar en el archivo de salida
    output_columns = [
        'fecha', 'id_partido', 'equipo_local', 'equipo_visitante',
        'prob_yrfi_predicha', 'prob_local_anota', 'prob_visitante_anota',
        'game_yrfi_real', 'home_yrfi_target', 'away_yrfi_target',
        'prediccion_yrfi', 'prediccion_local', 'prediccion_visitante'
    ]
    
    # Mantener solo las columnas que existen en el DataFrame
    existing_columns = [col for col in output_columns if col in eval_df.columns]
    
    # Agregar cualquier columna faltante con valores predeterminados
    for col in output_columns:
        if col not in existing_columns and col in ['home_yrfi_target', 'away_yrfi_target']:
            eval_df[col] = 0
            existing_columns.append(col)
    
    # Guardar resultados detallados
    output_path = OUTPUT_DIR / output_file
    eval_df[existing_columns].to_csv(output_path, index=False)
    print(f"\nResultados guardados en: {output_path}")
    print(f"Columnas incluidas: {', '.join(existing_columns)}")
    
    # Mostrar un resumen de los datos guardados
    print("\nResumen de los datos guardados:")
    print(eval_df[['fecha', 'equipo_local', 'equipo_visitante', 
                  'prob_yrfi_predicha', 'prob_local_anota', 'prob_visitante_anota',
                  'game_yrfi_real', 'home_yrfi_target', 'away_yrfi_target',
                  'prediccion_yrfi', 'prediccion_local', 'prediccion_visitante']].head())
    
    # Mostrar recomendación basada en el rendimiento
    print("\n" + "="*60)
    if precision_yrfi >= 0.52:
        print(f"✅ ¡BUEN RESULTADO! Precisión del {precision_yrfi*100:.1f}% (umbral: {threshold})")
    elif predicted_games == 0:
        print("⚠️  No se realizaron predicciones YRFI con este umbral.")
    else:
        print(f"⚠️  Precisión del {precision_yrfi*100:.1f}% - Por debajo del 52% objetivo (umbral: {threshold})")
    
    print(f"📊 Resultados guardados en: {output_path}")
    print("="*60 + "\n")
    
    # Devolver métricas para comparación
    return {
        'threshold': threshold,
        'total_games': total_games,
        'predicted_games': predicted_games,
        'correct_predictions': correct_yrfi,
        'precision': precision_yrfi,
        'roi': roi_yrfi
    }

def main():
    """Función principal."""
    print("\n" + "="*60)
    print(f"{'ENTRENAMIENTO DE MODELO YRFI':^60}")
    print("="*60)
    
    # Cargar datos
    print("\n=== Cargando datos ===")
    try:
        df = load_data()
        if df is None or df.empty:
            print("No se pudieron cargar los datos. Saliendo...")
            return
        
        print(f"Datos cargados correctamente. Total de registros: {len(df)}")
        
        # Verificar columnas necesarias
        required_columns = ['fecha', 'id_partido', 'equipo_local', 'equipo_visitante', 
                           'home_yrfi_target', 'away_yrfi_target', 'game_yrfi_real']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Faltan columnas requeridas: {', '.join(missing_columns)}")
            return
            
        # Asegurar que las fechas estén en el formato correcto
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Ejecutar backtesting
        print("\n=== Iniciando Backtesting ===")
        results_df = run_prediction_backtest(df)
        
        if results_df is None or results_df.empty:
            print("No se generaron resultados del backtesting. Saliendo...")
            return
        
        print(f"\nBacktesting completado. Total de partidos procesados: {len(results_df)}")
        
        # Evaluar con diferentes umbrales
        thresholds = [0.45, 0.48, 0.50, 0.52, 0.55]
        results = []
        
        for threshold in thresholds:
            print(f"\n{'='*30} UMBRAL: {threshold:.2f} {'='*30}")
            try:
                precision, roi, predicted = evaluate_predictions(
                    results_df, 
                    threshold, 
                    f'backtesting_results_threshold_{threshold:.2f}.csv'
                )
                results.append({
                    'threshold': threshold,
                    'precision': precision,
                    'roi': roi,
                    'predicted': predicted
                })
            except Exception as e:
                print(f"Error al evaluar con umbral {threshold}: {str(e)}")
                continue
        
        # Mostrar resumen de todos los umbrales
        if not results:
            print("No se pudieron evaluar los umbrales. Saliendo...")
            return
        
        print("\n" + "="*60)
        print(f"{'RESUMEN DE TODOS LOS UMBRALES':^60}")
        print("="*60)
        print(f"{'Umbral':<10} {'Predicciones':<15} {'Precisión':<15} {'ROI':<15}")
        print("-"*60)
        
        for r in results:
            print(f"{r['threshold']:<10.2f} {r['predicted']:<15} {r['precision']*100:<15.1f}% {r['roi']:<15.1f}%")
        
        # Encontrar el mejor umbral basado en el ROI
        if results:
            best = max(results, key=lambda x: x['roi'] if x['predicted'] > 0 else -1)
            print("\n" + "="*60)
            print(f"MEJOR UMBRAL: {best['threshold']:.2f}")
            print(f"Precisión: {best['precision']*100:.1f}%")
            print(f"ROI: {best['roi']:.1f}%")
            print(f"Predicciones: {best['predicted']}")
            print("="*60)
            
            # Guardar resultados con el mejor umbral
            best_threshold = best['threshold']
            best_results = results_df.copy()
            best_results['prediction'] = (best_results['prob_yrfi_predicha'] >= best_threshold).astype(int)
            best_results['prediccion_local'] = (best_results['prob_local_anota'] >= best_threshold).astype(int)
            best_results['prediccion_visitante'] = (best_results['prob_visitante_anota'] >= best_threshold).astype(int)
            
            output_file = OUTPUT_DIR / 'mejores_predicciones_yrfi.csv'
            best_results.to_csv(output_file, index=False)
            print(f"\nMejores predicciones guardadas en: {output_file}")
            
    except Exception as e:
        print(f"Error en la ejecución principal: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()