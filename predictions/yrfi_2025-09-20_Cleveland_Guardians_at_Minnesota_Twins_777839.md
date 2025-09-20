# Análisis YRFI: Cleveland Guardians @ Minnesota Twins

**Fecha:** 2025-09-20  
**Lanzadores:** Slade Cecconi (V) vs Joe Ryan (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 38.1%

## 🔍 Explicación de los Cálculos

### Minnesota Twins (Local)
- **Estadística base YRFI:** 25.6% (20/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Cleveland Guardians - Slade Cecconi):** 20.0% (2/10 partidos)
- **Puntuación ajustada:** 21.6%

### Cleveland Guardians (Visitante)
- **Estadística base YRFI:** 23.1% (18/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Minnesota Twins - Joe Ryan):** 13.3% (2/15 partidos)
- **Puntuación ajustada:** 20.9%

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

- **Generado el:** 2025-09-20 09:36:49
- **Fuente de datos:** season_data.json
