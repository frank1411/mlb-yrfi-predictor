# Análisis YRFI: Tampa Bay Rays @ Chicago Cubs

**Fecha:** 2025-09-12  
**Lanzadores:** Shane Baz (V) vs Matthew Boyd (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.6%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 27.8% (20/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Tampa Bay Rays - Shane Baz):** 15.4% (2/13 partidos)
- **Puntuación ajustada:** 23.0%

### Tampa Bay Rays (Visitante)
- **Estadística base YRFI:** 23.6% (17/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Matthew Boyd):** 30.8% (4/13 partidos)
- **Puntuación ajustada:** 32.0%

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

- **Generado el:** 2025-09-12 09:38:12
- **Fuente de datos:** season_data.json
