# Análisis YRFI: St. Louis Cardinals @ Milwaukee Brewers

**Fecha:** 2025-09-14  
**Lanzadores:** Miles Mikolas (V) vs Jose Quintana (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.0%

## 🔍 Explicación de los Cálculos

### Milwaukee Brewers (Local)
- **Estadística base YRFI:** 17.6% (13/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (St. Louis Cardinals - Miles Mikolas):** 35.7% (5/14 partidos)
- **Puntuación ajustada:** 34.3%

### St. Louis Cardinals (Visitante)
- **Estadística base YRFI:** 27.0% (20/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Milwaukee Brewers - Jose Quintana):** 27.3% (3/11 partidos)
- **Puntuación ajustada:** 27.0%

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

- **Generado el:** 2025-09-14 09:36:39
- **Fuente de datos:** season_data.json
