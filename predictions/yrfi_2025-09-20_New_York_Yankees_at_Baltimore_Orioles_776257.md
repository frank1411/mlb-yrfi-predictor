# Análisis YRFI: New York Yankees @ Baltimore Orioles

**Fecha:** 2025-09-20  
**Lanzadores:** Carlos Rodón (V) vs Tomoyuki Sugano (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 60.4%

## 🔍 Explicación de los Cálculos

### Baltimore Orioles (Local)
- **Estadística base YRFI:** 26.3% (20/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (New York Yankees - Carlos Rodón):** 17.6% (3/17 partidos)
- **Puntuación ajustada:** 25.8%

### New York Yankees (Visitante)
- **Estadística base YRFI:** 43.0% (34/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (Baltimore Orioles - Tomoyuki Sugano):** 42.9% (6/14 partidos)
- **Puntuación ajustada:** 46.7%

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
