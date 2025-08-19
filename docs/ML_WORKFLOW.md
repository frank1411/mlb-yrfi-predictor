# Flujo de Trabajo de Machine Learning para Predicción YRFI

## 1. Estructura del Proyecto

```
mlb_api_project/
├── data/
│   └── dataset_mlb_MULTITARGET.csv  # Dataset principal
├── models/
│   ├── modelo_yrfi_local.pkl        # Modelo para equipo local
│   └── modelo_yrfi_visitante.pkl    # Modelo para equipo visitante
├── scripts/
│   ├── generar_dataset_final.py     # Genera el dataset
│   └── entrenar_modelos.py          # Entrena los modelos
└── models/
    └── predecir_partido.py          # Realiza predicciones
```

## 2. Flujo de Ejecución

### Paso 1: Generar el Dataset
**Script:** `scripts/generar_dataset_final.py`

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar generación de dataset
python scripts/generar_dataset_final.py
```

**Descripción:**
- Recopila datos de rendimiento de equipos y lanzadores
- Genera el archivo `dataset_mlb_MULTITARGET.csv`
- Incluye características como:
  - Porcentaje de anotación en primera entrada
  - Rendimiento reciente
  - Estadísticas de lanzadores

### Paso 2: Entrenar los Modelos
**Script:** `scripts/entrenar_modelos.py`

```bash
python scripts/entrenar_modelos.py
```

**Proceso:**
1. Carga el dataset generado
2. Divide los datos en entrenamiento (80%) y prueba (20%)
3. Entrena dos modelos de regresión logística:
   - Uno para predecir anotación del equipo local
   - Otro para predecir anotación del equipo visitante
4. Evalúa el rendimiento con métricas
5. Guarda los modelos en la carpeta `models/`

### Paso 3: Realizar Predicciones
**Script:** `models/predecir_partido.py`

```bash
python models/predecir_partido.py
```

**Salida:**
- Probabilidad de anotación del equipo local
- Probabilidad de anotación del equipo visitante
- Probabilidad combinada de que cualquiera anote

## 3. Requisitos del Sistema

1. **Entorno Python**:
   - Python 3.7+
   - Entorno virtual recomendado

2. **Dependencias** (instalables con `pip install -r requirements.txt`):
   ```
   pandas>=1.3.0
   scikit-learn>=1.0.0
   joblib>=1.1.0
   numpy>=1.21.0
   ```

## 4. Personalización

### Modificar Características
Editar la lista `FEATURES` en `entrenar_modelos.py`:
```python
FEATURES = [
    'local_pct_anota_1inn_local',
    'local_pct_anota_1inn_ult15',
    'visit_pct_anota_1inn_visit',
    'visit_pct_anota_1inn_ult15',
    'pitcher_local_pct_permite_carrera_suavizado',
    'pitcher_visit_pct_permite_carrera_suavizado'
]
```

### Ajustar Parámetros del Modelo
Modificar la función `train_and_evaluate_model()` en `entrenar_modelos.py`:
```python
model = LogisticRegression(
    penalty='l2',
    C=1.0,
    solver='liblinear',
    random_state=42
)
```

## 5. Mantenimiento

### Actualizar Datos
1. Ejecutar `generar_dataset_final.py` para actualizar estadísticas
2. Reentrenar modelos con `entrenar_modelos.py`

### Monitoreo
Revisar métricas de rendimiento:
- Precisión (Accuracy)
- ROC AUC
- Matriz de confusión
- Sensibilidad y especificidad

## 6. Solución de Problemas

### Error: "No se encuentra el dataset"
- Verificar que `dataset_mlb_MULTITARGET.csv` existe en `data/`
- Ejecutar primero `generar_dataset_final.py`

### Error al cargar modelos
- Asegurarse que los archivos `.pkl` existen en `models/`
- Verificar versiones de scikit-learn

### Bajo rendimiento
- Revisar calidad de los datos
- Ajustar hiperparámetros
- Considerar más características

## 7. Próximos Pasos Recomendados

1. **Mejora de Modelos**:
   - Prueba con otros algoritmos (Random Forest, XGBoost)
   - Ajuste de hiperparámetros
   - Validación cruzada más robusta

2. **Automatización**:
   - Script para actualización diaria
   - Monitoreo automático de rendimiento

3. **Interfaz**:
   - API REST para predicciones
   - Panel de control con métricas
