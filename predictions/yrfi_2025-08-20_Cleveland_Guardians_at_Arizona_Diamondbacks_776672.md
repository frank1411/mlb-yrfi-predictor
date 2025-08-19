# Análisis YRFI: Cleveland Guardians @ Arizona Diamondbacks

**Fecha:** 2025-08-20  
**Lanzadores:** Tanner Bibee (V) vs Eduardo Rodriguez (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 64.6%

## 🔍 Explicación de los Cálculos

### Arizona Diamondbacks (Local)
- **Estadística base YRFI:** 42.6% (26/61 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador visitante (Cleveland Guardians - Tanner Bibee):** 28.6% (4/14 partidos)
- **Puntuación ajustada:** 43.9%

### Cleveland Guardians (Visitante)
- **Estadística base YRFI:** 24.2% (15/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Arizona Diamondbacks - Eduardo Rodriguez):** 44.4% (4/9 partidos)
- **Puntuación ajustada:** 36.9%

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

- **Generado el:** 2025-08-19 12:49:11
- **Fuente de datos:** season_data.json
