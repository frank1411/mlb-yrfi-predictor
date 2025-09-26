# Análisis YRFI: Baltimore Orioles @ New York Yankees

**Fecha:** 2025-09-26  
**Lanzadores:** Trevor Rogers (V) vs Will Warren (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.5%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 34.6% (27/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador visitante (Baltimore Orioles - Trevor Rogers):** 10.0% (1/10 partidos)
- **Puntuación ajustada:** 32.7%

### Baltimore Orioles (Visitante)
- **Estadística base YRFI:** 26.9% (21/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (New York Yankees - Will Warren):** 13.3% (2/15 partidos)
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

- **Generado el:** 2025-09-26 09:39:49
- **Fuente de datos:** season_data.json
