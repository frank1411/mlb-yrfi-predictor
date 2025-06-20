# ⚾ MLB YRFI Predictor

Sistema avanzado para predecir la probabilidad de carreras en el primer inning (YRFI - Yes Runs First Inning) en partidos de la MLB. El sistema analiza estadísticas históricas, rendimiento de lanzadores y tendencias recientes para generar predicciones diarias.

## 🚀 Características Principales

- Predicciones diarias de YRFI para todos los partidos de la MLB
- Análisis detallado de rendimiento de lanzadores
- Seguimiento de tendencias recientes de equipos
- Generación de informes en formato Markdown y JSON
- Sistema de caché para optimizar el rendimiento

## 📦 Estructura del Proyecto

```
mlb_api_project/
├── data/                  # Datos de temporada y caché
│   ├── season_data.json   # Datos completos de la temporada
│   └── cache/             # Datos en caché para optimización
│
├── predictions/          # Predicciones generadas
│   ├── resumen_yrfi_YYYY-MM-DD.md  # Informe resumido
│   └── yrfi_YYYY-MM-DD_*.json     # Predicciones por partido
│
├── scripts/              # Scripts principales
│   ├── generar_pronostico.py         # Lógica de predicción
│   ├── generar_pronosticos_jornada.py # Generación de predicciones
│   ├── initialize_season_data.py     # Inicialización de datos
│   └── get_pitchers_direct.py        # Obtención de lanzadores
│
├── src/                  # Módulos reutilizables
│   └── ... (módulos adicionales)
│
├── tests/                # Pruebas unitarias
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🛠️ Configuración

1. **Requisitos:**
   - Python 3.8+

2. **Instalación:**
   ```bash
   # Clonar el repositorio
   git clone [URL_DEL_REPOSITORIO]
   cd mlb_api_project

   # Crear y activar entorno virtual
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

   # Instalar dependencias
   pip install -r requirements.txt
   ```

## 🚦 Uso Básico

### 1. Inicializar Datos de Temporada
```bash
python scripts/initialize_season_data.py
```
*Nota: Este paso solo es necesario al inicio o para forzar una actualización completa.*

### 2. Generar Predicciones Diarias
```bash
python scripts/generar_pronosticos_jornada.py
```

### 3. Resultados
- **Resumen general:** `predictions/resumen_yrfi_YYYY-MM-DD.md`
- **Predicciones detalladas:** `predictions/yrfi_YYYY-MM-DD_*.json`

## 📊 Entendiendo las Predicciones

### Factores Considerados
1. **Rendimiento del Equipo Local/Visitante**
   - Estadísticas de temporada completa
   - Tendencias recientes (últimos 15 partidos)

2. **Rendimiento de Lanzadores**
   - Estadísticas de YRFI permitido
   - Desempeño como abridor local/visitante

3. **Ajustes**
   - Ponderación entre estadísticas de temporada y tendencias recientes
   - Ajustes por rol (local/visitante)

### Ejemplo de Salida
```markdown
## Philadelphia Phillies @ Miami Marlins
- **Probabilidad YRFI:** 27.5%
- **Lanzadores:** Cristopher Sánchez vs Edward Cabrera
- **Tendencia Local (MIA):** 26.7% (4/15)
- **Tendencia Visitante (PHI):** 40.0% (6/15)
```

## 🔄 Mantenimiento

### Actualización de Datos
Los datos se actualizan automáticamente al generar predicciones. Para forzar una actualización manual:

```bash
python scripts/initialize_season_data.py
```

### Limpieza de Caché
```bash
# Limpiar caché de Python
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete
```

## 🤝 Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

## ✉️ Contacto

[Tu nombre] - [@tu_twitter](https://twitter.com/tu_twitter)

Enlace del proyecto: [https://github.com/tuusuario/mlb-yrfi-predictor](https://github.com/tuusuario/mlb-yrfi-predictor)

## 🙏 Agradecimientos

- A todos los contribuyentes que han ayudado a mejorar este proyecto
- A la comunidad de desarrollo de software de código abierto
- A los datos públicos proporcionados por la MLB
