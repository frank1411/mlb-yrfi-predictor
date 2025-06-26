import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="MLB YRFI Predictor",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título de la aplicación
st.title("⚾ MLB YRFI Predictor")
st.markdown("### Predicciones de Carreras en la Primera Entrada (YRFI)")

# Barra lateral para filtros
with st.sidebar:
    st.header("Filtros")
    fecha = st.date_input("Seleccionar fecha", value=datetime.today())
    st.markdown("---")
    st.markdown("### Acerca de")
    st.markdown("Dashboard de predicciones YRFI (Yes Run First Inning)")

# Sección principal
def cargar_predicciones(fecha):
    """Carga las predicciones para la fecha especificada"""
    try:
        # Buscar archivos de predicción para la fecha
        fecha_str = fecha.strftime("%Y-%m-%d")
        # Usar ruta absoluta para evitar problemas
        base_dir = Path(__file__).parent.parent
        archivo_prediccion = base_dir / "predictions" / f"resumen_yrfi_{fecha_str}.md"
        
        if archivo_prediccion.exists():
            with open(archivo_prediccion, 'r', encoding='utf-8') as f:
                contenido = f.read()
                # Convertir markdown a HTML para mejor visualización
                return contenido
        else:
            return f"No hay predicciones disponibles para la fecha {fecha_str}"
    except Exception as e:
        import traceback
        return f"Error al cargar las predicciones: {str(e)}\n\n{traceback.format_exc()}"

# Contenedor para las predicciones
# Mostrar el resumen de predicciones
st.header(f"📊 Resumen de Predicciones YRFI - {fecha.strftime('%d/%m/%Y')}")
predicciones = cargar_predicciones(fecha)

if isinstance(predicciones, str):
    # Dividir el contenido en secciones
    secciones = predicciones.split('## ')
    
    # Mostrar la primera sección (título y resumen)
    if secciones:
        st.markdown(f"## {secciones[0]}")
    
    # Mostrar las demás secciones
    for seccion in secciones[1:]:
        if not seccion.strip():
            continue
        
        titulo = seccion.split('\n', 1)[0]
        contenido = seccion[len(titulo):].strip()
        
        with st.expander(f"🔍 {titulo}", expanded=True):
            st.markdown(contenido)
else:
    st.error("Error al cargar las predicciones")

# Footer
st.markdown("---")
st.markdown("### 📊 Métricas de Precisión")
st.warning("🔧 Sección en desarrollo - Próximamente métricas de precisión histórica")

# Nota: Agregaremos más funcionalidades en próximas iteraciones
