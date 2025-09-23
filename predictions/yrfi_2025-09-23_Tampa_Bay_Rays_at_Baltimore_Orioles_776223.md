# Análisis YRFI: Tampa Bay Rays @ Baltimore Orioles

**Fecha:** 2025-09-23  
**Lanzadores:** Ryan Pepiot (V) vs Dean Kremer (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 45.8%

## 🔍 Explicación de los Cálculos

### Baltimore Orioles (Local)
- **Estadística base YRFI:** 25.6% (20/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Tampa Bay Rays - Ryan Pepiot):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 22.0%

### Tampa Bay Rays (Visitante)
- **Estadística base YRFI:** 25.3% (19/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Baltimore Orioles - Dean Kremer):** 18.2% (2/11 partidos)
- **Puntuación ajustada:** 30.5%

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

- **Generado el:** 2025-09-23 09:40:26
- **Fuente de datos:** season_data.json
