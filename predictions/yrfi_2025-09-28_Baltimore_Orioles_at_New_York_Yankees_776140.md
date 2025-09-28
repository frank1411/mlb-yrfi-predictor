# Análisis YRFI: Baltimore Orioles @ New York Yankees

**Fecha:** 2025-09-28  
**Lanzadores:** Kyle Bradish (V) vs Luis Gil (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 60.6%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 36.2% (29/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador visitante (Baltimore Orioles - Kyle Bradish):** 50.0% (1/2 partidos)
- **Puntuación ajustada:** 49.5%

### Baltimore Orioles (Visitante)
- **Estadística base YRFI:** 26.2% (21/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (New York Yankees - Luis Gil):** 20.0% (1/5 partidos)
- **Puntuación ajustada:** 21.8%

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

- **Generado el:** 2025-09-28 09:35:53
- **Fuente de datos:** season_data.json
