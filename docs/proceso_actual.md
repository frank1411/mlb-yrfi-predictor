# 📋 Documentación del Proceso Actual - MLB YRFI Predictor

*Última actualización: 26 de Junio 2025*

## 📌 Visión General

Este documento describe el proceso actual de generación de pronósticos YRFI (Yes Run First Inning) para partidos de las Grandes Ligas de Béisbol.

## 🔄 Flujo de Trabajo

### 1. Inicialización de Datos

**Script:** `scripts/initialize_season_data.py`

**Propósito:**
- Actualizar los datos de la temporada con los resultados más recientes
- Procesar la información de los partidos finalizados
- Preparar la base de datos para la generación de pronósticos

**Entrada:**
- Datos de la API de MLB
- Archivo de configuración de temporada

**Salida:**
- Archivo `data/season_data.json` actualizado
- Estadísticas de la temporada

---

### 2. Generación de Pronósticos

**Script:** `scripts/generar_pronosticos_jornada.py`

**Propósito:**
- Generar predicciones YRFI para los partidos del día
- Calcular probabilidades ajustadas
- Generar archivos de salida

**Proceso:**
1. Cargar datos de temporada actualizados
2. Identificar partidos del día
3. Para cada partido:
   - Calcular probabilidad base del equipo local
   - Calcular probabilidad base del equipo visitante
   - Aplicar ajustes por tendencia reciente
   - Aplicar ajustes por rendimiento de lanzadores
   - Calcular probabilidad final del partido
4. Generar archivos de salida

**Salida:**
- Archivos JSON en `predictions/` (uno por partido)
- Resumen en `predictions/resumen_yrfi_YYYY-MM-DD.md`

---

### 3. Análisis de Resultados

**Ubicación:** `predictions/`

**Contenido:**
- Archivos JSON con predicciones detalladas
- Archivos Markdown con resúmenes formateados

**Estructura de archivos:**
```
predictions/
├── resumen_yrfi_YYYY-MM-DD.md
├── yrfi_YYYY-MM-DD_EquipoLocal_at_EquipoVisitante.json
└── ...
```

## 📊 Fórmulas de Cálculo

### 1. Probabilidad Base del Equipo

```
Probabilidad Base = (YRFI Totales / Total de Partidos) * 100
```

### 2. Ajuste por Tendencia (Últimos 15 partidos)

```
Tendencia = (YRFI Recientes / 15) * 100
```

### 3. Combinación Base + Tendencia

```
Probabilidad Combinada = (Base * 0.6) + (Tendencia * 0.4)
```

### 4. Ajuste por Lanzador Rival

```
Probabilidad Ajustada = (Prob. Combinada * 0.7) + (Rendimiento Lanzador * 0.3)
```

### 5. Probabilidad Final del Partido

```
Prob. Partido = 1 - ((1 - Prob. Local) * (1 - Prob. Visitante))
```

## 📝 Formato de Entrega

### 1. Encabezado
```markdown
# 📊 Resumen de Pronósticos YRFI - YYYY-MM-DD
```

### 2. Top 3 Equipos con Mayor Probabilidad

```markdown
### 1. [Nombre Equipo] - XX.X%
- **Base:** XX.X% (Y/Y partidos)
- **Tendencia:** XX.X% (Y/15 partidos)
- **Lanzador Rival:** [Nombre] (XX.X% - X/Y aperturas)
```

### 3. Top 2 Partidos con Mayor Probabilidad

```markdown
### 1. [Equipo Local] vs [Equipo Visitante] - XX.X%
- **Local:** XX.X% (Base: XX.X%, Tendencia: XX.X%)
- **Visitante:** XX.X% (Base: XX.X%, Tendencia: XX.X%)
- **Lanzadores:** [Local] vs [Visitante]
```

### 4. Secciones Adicionales
- Top 3 Equipos con Menor Probabilidad
- Top 2 Partidos con Menor Probabilidad
- Notas y Consideraciones

## ⚠️ Consideraciones Especiales

1. **Lanzadores con Pocas Aperturas:**
   - Menos de 5 aperturas: considerar con precaución
   - Menos de 3 aperturas: datos insuficientes

2. **Partidos con Datos Incompletos:**
   - Verificar disponibilidad de lanzadores
   - Validar estadísticas recientes

3. **Doble Jornada:**
   - Considerar desgaste de bullpen
   - Verificar cambios de última hora

## 📅 Frecuencia de Actualización

1. **Datos:** Diariamente antes de la generación de pronósticos
2. **Modelo:** Semanalmente o según necesidad
3. **Documentación:** Con cada cambio significativo

---

*Documentación creada el 26 de Junio 2025*
*Próxima revisión programada: 10 de Julio 2025*
