# Análisis YRFI: Chicago Cubs @ Milwaukee Brewers

**Fecha:** 2025-10-07  
**Lanzadores:** Shota Imanaga (V) vs Aaron Ashby (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 41.4%

## 🔍 Explicación de los Cálculos

### Milwaukee Brewers (Local)
- **Estadística base YRFI:** 17.3% (14/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador visitante (Chicago Cubs - Shota Imanaga):** 46.2% (6/13 partidos)
- **Puntuación ajustada:** 23.6%

### Chicago Cubs (Visitante)
- **Estadística base YRFI:** 30.9% (25/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Milwaukee Brewers - Aaron Ashby):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 23.3%

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

- **Generado el:** 2025-10-06 09:41:45
- **Fuente de datos:** season_data.json
