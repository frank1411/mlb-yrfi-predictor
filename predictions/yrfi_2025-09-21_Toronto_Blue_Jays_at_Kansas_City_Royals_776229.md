# Análisis YRFI: Toronto Blue Jays @ Kansas City Royals

**Fecha:** 2025-09-21  
**Lanzadores:** Trey Yesavage (V) vs Michael Wacha (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 68.8%

## 🔍 Explicación de los Cálculos

### Kansas City Royals (Local)
- **Estadística base YRFI:** 32.5% (26/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Toronto Blue Jays - Trey Yesavage):** 100.0% (1/1 partidos)
- **Puntuación ajustada:** 61.2%

### Toronto Blue Jays (Visitante)
- **Estadística base YRFI:** 26.6% (21/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Kansas City Royals - Michael Wacha):** 6.2% (1/16 partidos)
- **Puntuación ajustada:** 19.5%

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
