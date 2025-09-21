# Análisis YRFI: Philadelphia Phillies @ Arizona Diamondbacks

**Fecha:** 2025-09-21  
**Lanzadores:** Ranger Suárez (V) vs Eduardo Rodriguez (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 59.9%

## 🔍 Explicación de los Cálculos

### Arizona Diamondbacks (Local)
- **Estadística base YRFI:** 46.8% (36/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Philadelphia Phillies - Ranger Suárez):** 9.1% (1/11 partidos)
- **Puntuación ajustada:** 31.2%

### Philadelphia Phillies (Visitante)
- **Estadística base YRFI:** 27.5% (22/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (Arizona Diamondbacks - Eduardo Rodriguez):** 41.7% (5/12 partidos)
- **Puntuación ajustada:** 41.7%

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
