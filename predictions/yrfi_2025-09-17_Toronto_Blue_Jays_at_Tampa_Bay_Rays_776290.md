# Análisis YRFI: Toronto Blue Jays @ Tampa Bay Rays

**Fecha:** 2025-09-17  
**Lanzadores:** Kevin Gausman (V) vs Ian Seymour (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 46.8%

## 🔍 Explicación de los Cálculos

### Tampa Bay Rays (Local)
- **Estadística base YRFI:** 34.2% (26/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Toronto Blue Jays - Kevin Gausman):** 20.0% (3/15 partidos)
- **Puntuación ajustada:** 33.7%

### Toronto Blue Jays (Visitante)
- **Estadística base YRFI:** 26.7% (20/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Tampa Bay Rays - Ian Seymour):** 0.0% (1/3 partidos)
- **Puntuación ajustada:** 19.7%

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

- **Generado el:** 2025-09-17 09:39:33
- **Fuente de datos:** season_data.json
