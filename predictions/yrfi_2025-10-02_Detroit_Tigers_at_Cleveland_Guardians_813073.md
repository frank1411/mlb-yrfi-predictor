# Análisis YRFI: Detroit Tigers @ Cleveland Guardians

**Fecha:** 2025-10-02  
**Lanzadores:** Jack Flaherty (V) vs Slade Cecconi (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 40.9%

## 🔍 Explicación de los Cálculos

### Cleveland Guardians (Local)
- **Estadística base YRFI:** 33.3% (27/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Detroit Tigers - Jack Flaherty):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 29.1%

### Detroit Tigers (Visitante)
- **Estadística base YRFI:** 21.0% (17/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (Cleveland Guardians - Slade Cecconi):** 16.7% (2/12 partidos)
- **Puntuación ajustada:** 16.7%

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

- **Generado el:** 2025-10-02 09:38:48
- **Fuente de datos:** season_data.json
