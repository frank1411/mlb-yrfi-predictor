import os
import sys
import pandas as pd
import joblib
from pathlib import Path

# --- Configuración de rutas ---
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / 'models'

# --- Nombres de los archivos de modelos ---
MODELO_LOCAL_FILE = MODELS_DIR / 'modelo_yrfi_local.pkl'
MODELO_VISITANTE_FILE = MODELS_DIR / 'modelo_yrfi_visitante.pkl'

# --- ¡MUY IMPORTANTE! ---
# Las características (features) deben estar EXACTAMENTE en el mismo orden
# en que se usaron para entrenar los modelos.
FEATURES_ORDER = [
    'local_pct_anota_1inn_local',
    'local_pct_anota_1inn_ult15',
    'visit_pct_anota_1inn_visit',
    'visit_pct_anota_1inn_ult15',
    'pitcher_local_pct_permite_carrera_suavizado',
    'pitcher_visit_pct_permite_carrera_suavizado'
]

def cargar_modelos():
    """Carga los dos modelos entrenados desde los archivos .pkl."""
    try:
        print(f"Buscando modelos en: {MODELS_DIR}")
        print(f"- {MODELO_LOCAL_FILE}")
        print(f"- {MODELO_VISITANTE_FILE}")
        
        if not os.path.exists(MODELO_LOCAL_FILE):
            raise FileNotFoundError(f"No se encontró el archivo: {MODELO_LOCAL_FILE}")
        if not os.path.exists(MODELO_VISITANTE_FILE):
            raise FileNotFoundError(f"No se encontró el archivo: {MODELO_VISITANTE_FILE}")
        
        # Cargar modelos usando joblib
        model_home = joblib.load(MODELO_LOCAL_FILE)
        model_away = joblib.load(MODELO_VISITANTE_FILE)
            
        print("✅ Modelos cargados correctamente con joblib")
        return model_home, model_away
        
    except Exception as e:
        print(f"\n❌ Error al cargar los modelos: {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Asegúrate de que los archivos .pkl existen en la carpeta models/")
        print("2. Ejecuta primero el script de entrenamiento: python scripts/entrenar_modelos.py")
        print("3. Verifica que las versiones de scikit-learn sean compatibles")
        import traceback
        traceback.print_exc()
        return None, None

def hacer_predicciones(model_home, model_away, datos_partido):
    """
    Toma los modelos cargados y los datos de un partido para generar las 3 predicciones.
    """
    # 1. Convertir los datos del partido a un DataFrame de pandas
    # El modelo espera recibir los datos en este formato.
    partido_df = pd.DataFrame([datos_partido])

    # 2. Asegurar el orden correcto de las columnas
    partido_df = partido_df[FEATURES_ORDER]

    print("\n--- Datos del partido a predecir ---")
    print(partido_df.to_string(index=False))

    # 3. Predecir las probabilidades con cada modelo
    # Usamos `predict_proba` que nos da la probabilidad de [clase_0, clase_1]
    # Nos interesa la probabilidad de la clase 1 (que SÍ anote).
    prob_local_anota = model_home.predict_proba(partido_df)[0][1]
    prob_visit_anota = model_away.predict_proba(partido_df)[0][1]

    # 4. Calcular la probabilidad de que CUALQUIERA de los dos anote
    prob_nadie_anota = (1 - prob_local_anota) * (1 - prob_visit_anota)
    prob_partido_yrfi = 1 - prob_nadie_anota

    # 5. Mostrar los resultados de forma clara
    print("\n--- PREDICCIONES DEL MODELO ---")
    print(f"Probabilidad de que el Equipo Local anote: {prob_local_anota:.2%}")
    print(f"Probabilidad de que el Equipo Visitante anote: {prob_visit_anota:.2%}")
    print("-------------------------------------------------")
    print(f"Probabilidad de que CUALQUIERA de los dos anote: {prob_partido_yrfi:.2%}")


if __name__ == "__main__":
    # --- PASO 1: CARGAR LOS MODELOS ---
    modelo_local, modelo_visitante = cargar_modelos()

    if modelo_local and modelo_visitante:
        # --- PASO 2: PREPARAR LOS DATOS DEL PARTIDO A PREDECIR ---
        #
        # ¡ESTA ES LA PARTE QUE DEBES MODIFICAR!
        # Reemplaza estos valores de ejemplo con los datos reales del partido
        # que calculaste para el día de hoy.
        #
        DATOS_DEL_PARTIDO_A_PREDECIR = {
        "local_pct_anota_1inn_local": 0.4262295081967213,
        "local_pct_anota_1inn_ult15": 0.6,
        "visit_pct_anota_1inn_visit": 0.24193548387096775,
        "visit_pct_anota_1inn_ult15": 0.4,
        "pitcher_local_pct_permite_carrera_suavizado": 0.34773676261549397,
        "pitcher_visit_pct_permite_carrera_suavizado": 0.2877821483714433
      }

        # --- PASO 3: HACER Y MOSTRAR LAS PREDICCIONES ---
        hacer_predicciones(modelo_local, modelo_visitante, DATOS_DEL_PARTIDO_A_PREDECIR)