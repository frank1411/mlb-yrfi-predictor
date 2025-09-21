# Análisis YRFI: Cleveland Guardians @ Minnesota Twins

**Fecha:** 2025-09-21  
**Lanzadores:** Joey Cantillo (V) vs Simeon Woods Richardson (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 39.3%

## 🔍 Explicación de los Cálculos

### Minnesota Twins (Local)
- **Estadística base YRFI:** 25.0% (20/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (Cleveland Guardians - Joey Cantillo):** 28.6% (2/7 partidos)
- **Puntuación ajustada:** 22.1%

### Cleveland Guardians (Visitante)
- **Estadística base YRFI:** 23.8% (19/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Minnesota Twins - Simeon Woods Richardson):** 9.1% (1/11 partidos)
- **Puntuación ajustada:** 22.1%

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

- **Generado el:** 2025-09-21 09:36:24
- **Fuente de datos:** season_data.json
