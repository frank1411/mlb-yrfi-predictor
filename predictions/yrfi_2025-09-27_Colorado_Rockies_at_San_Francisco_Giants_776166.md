# Análisis YRFI: Colorado Rockies @ San Francisco Giants

**Fecha:** 2025-09-27  
**Lanzadores:** Germán Márquez (V) vs Trevor McDonald (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 48.4%

## 🔍 Explicación de los Cálculos

### San Francisco Giants (Local)
- **Estadística base YRFI:** 32.1% (25/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Colorado Rockies - Germán Márquez):** 50.0% (7/14 partidos)
- **Puntuación ajustada:** 43.6%

### Colorado Rockies (Visitante)
- **Estadística base YRFI:** 12.8% (10/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (San Francisco Giants - Trevor McDonald):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 8.5%

### 📝 Fórmula de Cálculo

La probabilidad final de que anoten en la primera entrada se calcula en tres pasos:

1. **Puntuación combinada** para cada equipo (45% estadística base + 55% tendencia reciente):
   - `Puntuación = (0.45 × Estadística Base) + (0.55 × Tendencia Reciente)`

2. **Ajuste por lanzador** (65% puntuación combinada + 35% impacto del lanzador contrario):
   - `Puntuación Ajustada = (0.65 × Puntuación) + (0.35 × Rendimiento Lanzador Rival)`

3. **Probabilidad final** considerando ambos equipos como eventos independientes:
   - `Probabilidad Final = 1 - ((1 - P_local) × (1 - P_visitante))`
   - Donde P_local y P_visitante son las probabilidades ajustadas convertidas a decimal (0-1)

### 📌 Notas Adicionales

- **Generado el:** 2025-09-26 09:39:49
- **Fuente de datos:** season_data.json
