# Análisis YRFI: Chicago Cubs @ Milwaukee Brewers

**Fecha:** 2025-10-04  
**Lanzadores:** Matthew Boyd (V) vs Freddy Peralta (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 35.8%

## 🔍 Explicación de los Cálculos

### Milwaukee Brewers (Local)
- **Estadística base YRFI:** 17.3% (14/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador visitante (Chicago Cubs - Matthew Boyd):** 18.8% (3/16 partidos)
- **Puntuación ajustada:** 14.0%

### Chicago Cubs (Visitante)
- **Estadística base YRFI:** 30.9% (25/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Milwaukee Brewers - Freddy Peralta):** 5.9% (1/17 partidos)
- **Puntuación ajustada:** 25.4%

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

- **Generado el:** 2025-10-04 09:36:14
- **Fuente de datos:** season_data.json
