# Análisis YRFI: Colorado Rockies @ Los Angeles Dodgers

**Fecha:** 2025-09-10  
**Lanzadores:** Germán Márquez (V) vs Emmet Sheehan (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 40.8%

## 🔍 Explicación de los Cálculos

### Los Angeles Dodgers (Local)
- **Estadística base YRFI:** 38.9% (28/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Colorado Rockies - Germán Márquez):** 50.0% (6/12 partidos)
- **Puntuación ajustada:** 38.4%

### Colorado Rockies (Visitante)
- **Estadística base YRFI:** 13.0% (9/69 partidos)
- **Tendencia reciente (últimos 15 partidos):** 0.0% (0/15 partidos)
- **Impacto del lanzador local (Los Angeles Dodgers - Emmet Sheehan):** 0.0% (0/5 partidos)
- **Puntuación ajustada:** 3.8%

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

- **Generado el:** 2025-09-09 09:40:50
- **Fuente de datos:** season_data.json
