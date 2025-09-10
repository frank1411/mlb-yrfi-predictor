# Análisis YRFI: Pittsburgh Pirates @ Baltimore Orioles

**Fecha:** 2025-09-10  
**Lanzadores:** Paul Skenes (V) vs Tyler Wells (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 41.2%

## 🔍 Explicación de los Cálculos

### Baltimore Orioles (Local)
- **Estadística base YRFI:** 26.4% (19/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Pittsburgh Pirates - Paul Skenes):** 6.7% (1/15 partidos)
- **Puntuación ajustada:** 22.0%

### Pittsburgh Pirates (Visitante)
- **Estadística base YRFI:** 27.1% (19/70 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Baltimore Orioles - Tyler Wells):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 24.6%

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

- **Generado el:** 2025-09-10 09:39:09
- **Fuente de datos:** season_data.json
