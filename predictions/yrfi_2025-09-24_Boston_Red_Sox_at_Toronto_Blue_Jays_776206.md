# Análisis YRFI: Boston Red Sox @ Toronto Blue Jays

**Fecha:** 2025-09-24  
**Lanzadores:** Garrett Crochet (V) vs Max Scherzer (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.7%

## 🔍 Explicación de los Cálculos

### Toronto Blue Jays (Local)
- **Estadística base YRFI:** 28.9% (22/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Boston Red Sox - Garrett Crochet):** 17.6% (3/17 partidos)
- **Puntuación ajustada:** 21.8%

### Boston Red Sox (Visitante)
- **Estadística base YRFI:** 27.8% (22/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Toronto Blue Jays - Max Scherzer):** 55.6% (5/9 partidos)
- **Puntuación ajustada:** 39.5%

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

- **Generado el:** 2025-09-24 09:40:51
- **Fuente de datos:** season_data.json
