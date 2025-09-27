# Análisis YRFI: Tampa Bay Rays @ Toronto Blue Jays

**Fecha:** 2025-09-27  
**Lanzadores:** Joe Boyle (V) vs Trey Yesavage (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.5%

## 🔍 Explicación de los Cálculos

### Toronto Blue Jays (Local)
- **Estadística base YRFI:** 29.1% (23/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Tampa Bay Rays - Joe Boyle):** 66.7% (2/3 partidos)
- **Puntuación ajustada:** 41.4%

### Tampa Bay Rays (Visitante)
- **Estadística base YRFI:** 25.3% (20/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Toronto Blue Jays - Trey Yesavage):** 0.0% (1/2 partidos)
- **Puntuación ajustada:** 24.1%

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

- **Generado el:** 2025-09-27 09:36:25
- **Fuente de datos:** season_data.json
