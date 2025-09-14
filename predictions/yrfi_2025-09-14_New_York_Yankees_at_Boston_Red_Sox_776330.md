# Análisis YRFI: New York Yankees @ Boston Red Sox

**Fecha:** 2025-09-14  
**Lanzadores:** Will Warren (V) vs Garrett Crochet (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.3%

## 🔍 Explicación de los Cálculos

### Boston Red Sox (Local)
- **Estadística base YRFI:** 32.4% (24/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (New York Yankees - Will Warren):** 20.0% (3/15 partidos)
- **Puntuación ajustada:** 26.0%

### New York Yankees (Visitante)
- **Estadística base YRFI:** 42.5% (31/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (Boston Red Sox - Garrett Crochet):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 39.6%

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
