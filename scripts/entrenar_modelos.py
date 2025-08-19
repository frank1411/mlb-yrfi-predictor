import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, classification_report

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models'

# Crear directorios si no existen
MODELS_DIR.mkdir(exist_ok=True, parents=True)

# --- CONSTANTES ---
DATASET_FILE = DATA_DIR / 'dataset_mlb_MULTITARGET.csv' 

# Definimos nuestras columnas para tener el código más limpio
FEATURES = [
    'local_pct_anota_1inn_local',
    'local_pct_anota_1inn_ult15',
    'visit_pct_anota_1inn_visit',
    'visit_pct_anota_1inn_ult15',
    'pitcher_local_pct_permite_carrera_suavizado',
    'pitcher_visit_pct_permite_carrera_suavizado'
]

TARGET_HOME = 'home_yrfi_target'
TARGET_AWAY = 'away_yrfi_target'

def main():
    """
    Función principal para cargar datos, entrenar y evaluar los modelos de YRFI.
    """
    print("="*80)
    print("ENTRENAMIENTO DE MODELOS DE PREDICCIÓN YRFI")
    print("="*80 + "\n")

    # 1. Cargar el Dataset
    print(f"📂 Cargando dataset desde: {DATASET_FILE}")
    try:
        df = pd.read_csv(DATASET_FILE)
        print(f"✅ Dataset cargado exitosamente con {len(df)} partidos.")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{DATASET_FILE}'.")
        print("   Asegúrate de que el script 'generar_dataset_final.py' se haya ejecutado correctamente.")
        return
    except Exception as e:
        print(f"❌ Error al cargar el dataset: {str(e)}")
        return

    # 2. Verificar que todas las columnas necesarias estén presentes
    required_columns = FEATURES + [TARGET_HOME, TARGET_AWAY]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ Error: Faltan columnas en el dataset: {', '.join(missing_columns)}")
        return

    # 3. Definir Características (X) y Objetivos (y)
    X = df[FEATURES]
    y_home = df[TARGET_HOME]
    y_away = df[TARGET_AWAY]

    # 4. Dividir los datos en Entrenamiento y Prueba
    print("\n🔀 Dividiendo los datos en conjuntos de entrenamiento (80%) y prueba (20%)...")
    X_train, X_test, y_home_train, y_home_test, y_away_train, y_away_test = train_test_split(
        X, y_home, y_away, test_size=0.2, random_state=42, stratify=y_home
    )
    
    print(f"   - Datos de entrenamiento: {len(X_train)} partidos")
    print(f"   - Datos de prueba: {len(X_test)} partidos")

    # 5. Entrenar y evaluar modelos
    print("\n" + "="*50)
    print("ENTRENANDO MODELO: PREDICCIÓN LOCAL")
    print("="*50)
    model_home = train_and_evaluate_model(
        X_train, y_home_train, X_test, y_home_test, 
        model_name="YRFI Local", target_name="equipo local"
    )

    print("\n" + "="*50)
    print("ENTRENANDO MODELO: PREDICCIÓN VISITANTE")
    print("="*50)
    model_away = train_and_evaluate_model(
        X_train, y_away_train, X_test, y_away_test,
        model_name="YRFI Visitante", target_name="equipo visitante"
    )

    # 6. Guardar modelos
    save_model(model_home, "modelo_yrfi_local.pkl")
    save_model(model_away, "modelo_yrfi_visitante.pkl")

    # 7. Mostrar ejemplos de predicción
    print("\n" + "="*50)
    print("EJEMPLOS DE PREDICCIÓN")
    print("="*50)
    show_prediction_examples(model_home, model_away, X_test.head(5), y_home_test.head(5), y_away_test.head(5))


def train_and_evaluate_model(X_train, y_train, X_test, y_test, model_name, target_name):
    """
    Entrena y evalúa un modelo de clasificación.
    
    Args:
        X_train: Datos de entrenamiento
        y_train: Objetivos de entrenamiento
        X_test: Datos de prueba
        y_test: Objetivos de prueba
        model_name: Nombre del modelo para mostrar en los logs
        target_name: Nombre del objetivo (para logs)
        
    Returns:
        Modelo entrenado
    """
    print(f"\n🏋️  Entrenando modelo para predecir si {target_name} anotará en la primera entrada...")
    
    # Crear y entrenar el modelo
    model = LogisticRegression(
        random_state=42,
        class_weight='balanced',
        max_iter=1000,
        solver='liblinear'
    )
    
    # Entrenar el modelo
    model.fit(X_train, y_train)
    print("✅ Modelo entrenado exitosamente")
    
    # Evaluar el modelo
    print(f"\n📊 Evaluación del modelo {model_name}:")
    evaluate_model(model, X_train, y_train, X_test, y_test)
    
    return model


def save_model(model, filename):
    """Guarda un modelo en el directorio de modelos."""
    try:
        model_path = MODELS_DIR / filename
        joblib.dump(model, model_path)
        print(f"\n💾 Modelo guardado en: {model_path}")
    except Exception as e:
        print(f"❌ Error al guardar el modelo {filename}: {str(e)}")


def evaluate_model(model, X, y, X_test=None, y_test=None, cv=5):
    """
    Evalúa el rendimiento de un modelo con múltiples métricas y validación cruzada.
    
    Args:
        model: Modelo de scikit-learn entrenado
        X: Características para entrenamiento (usado en validación cruzada)
        y: Objetivos para entrenamiento (usado en validación cruzada)
        X_test: Características para prueba (opcional)
        y_test: Objetivos para prueba (opcional)
        cv: Número de folds para validación cruzada
    """
    # Validación cruzada
    print("\n--- Validación Cruzada ---")
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='roc_auc')
    print(f"ROC AUC (CV {cv}-folds): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    if X_test is not None and y_test is not None:
        # Predicciones en el conjunto de prueba
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # Métricas de evaluación
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        print("\n--- Métricas en Conjunto de Prueba ---")
        print(f"Precisión (Accuracy): {accuracy:.2%}")
        print(f"ROC AUC: {roc_auc:.4f}")
        print("\nReporte de Clasificación:")
        print(classification_report(y_test, y_pred, target_names=['No Anotó', 'Sí Anotó']))
        
        print("Matriz de Confusión:")
        print(f"{'':<25} {'Predicción: No':<15} {'Predicción: Sí':<15}")
        print(f"{'Realidad: No':<25} {f'TN: {cm[0][0]}':<15} {f'FP: {cm[0][1]}':<15}")
        print(f"{'Realidad: Sí':<25} {f'FN: {cm[1][0]}':<15} {f'TP: {cm[1][1]}':<15}")
        
        # Métricas adicionales
        sensitivity = cm[1,1] / (cm[1,0] + cm[1,1]) if (cm[1,0] + cm[1,1]) > 0 else 0
        specificity = cm[0,0] / (cm[0,0] + cm[0,1]) if (cm[0,0] + cm[0,1]) > 0 else 0
        
        print(f"\nSensibilidad (Recall de la clase positiva): {sensitivity:.2%}")
        print(f"Especificidad (Recall de la clase negativa): {specificity:.2%}")


def show_prediction_examples(model_home, model_away, X_sample, y_home_true, y_away_true):
    """
    Muestra las 3 predicciones para una muestra de datos.
    """
    # Obtener probabilidades de ambos modelos
    prob_home = model_home.predict_proba(X_sample)[:, 1]
    prob_away = model_away.predict_proba(X_sample)[:, 1]

    # Calcular la probabilidad combinada de YRFI en el partido
    prob_game = 1 - ((1 - prob_home) * (1 - prob_away))

    # Crear un DataFrame para mostrar los resultados de forma clara
    results = pd.DataFrame({
        'Prob. Local Anota': [f"{p:.2%}" for p in prob_home],
        'Resultado Real Local': y_home_true.values,
        'Prob. Visit. Anota': [f"{p:.2%}" for p in prob_away],
        'Resultado Real Visit.': y_away_true.values,
        'Prob. CUALQUIERA Anota': [f"{p:.2%}" for p in prob_game]
    })
    
    print(results)


# Ejecutar la función principal
if __name__ == "__main__":
    main()