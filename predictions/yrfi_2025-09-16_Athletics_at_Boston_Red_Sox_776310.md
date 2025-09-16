# Análisis YRFI: Athletics @ Boston Red Sox

**Fecha:** 2025-09-16  
**Lanzadores:** Jeffrey Springs (V) vs Connelly Early (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 41.5%

## 🔍 Explicación de los Cálculos

### Boston Red Sox (Local)
- **Estadística base YRFI:** 33.3% (25/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Athletics - Jeffrey Springs):** 26.7% (4/15 partidos)
- **Puntuación ajustada:** 28.6%

### Athletics (Visitante)
- **Estadística base YRFI:** 29.3% (22/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Boston Red Sox - Connelly Early):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 18.1%

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

- **Generado el:** 2025-09-16 09:40:57
- **Fuente de datos:** season_data.json
