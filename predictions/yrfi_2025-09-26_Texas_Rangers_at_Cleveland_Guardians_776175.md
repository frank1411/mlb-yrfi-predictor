# Análisis YRFI: Texas Rangers @ Cleveland Guardians

**Fecha:** 2025-09-26  
**Lanzadores:** Jack Leiter (V) vs Slade Cecconi (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 42.5%

## 🔍 Explicación de los Cálculos

### Cleveland Guardians (Local)
- **Estadística base YRFI:** 30.8% (24/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Texas Rangers - Jack Leiter):** 35.7% (5/14 partidos)
- **Puntuación ajustada:** 31.0%

### Texas Rangers (Visitante)
- **Estadística base YRFI:** 29.5% (23/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (Cleveland Guardians - Slade Cecconi):** 9.1% (1/11 partidos)
- **Puntuación ajustada:** 16.6%

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
