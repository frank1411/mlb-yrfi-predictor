# Análisis YRFI: Seattle Mariners @ Houston Astros

**Fecha:** 2025-09-20  
**Lanzadores:** Bryan Woo (V) vs Hunter Brown (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 53.8%

## 🔍 Explicación de los Cálculos

### Houston Astros (Local)
- **Estadística base YRFI:** 25.6% (20/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Seattle Mariners - Bryan Woo):** 53.3% (8/15 partidos)
- **Puntuación ajustada:** 38.1%

### Seattle Mariners (Visitante)
- **Estadística base YRFI:** 35.9% (28/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Houston Astros - Hunter Brown):** 15.4% (2/13 partidos)
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

- **Generado el:** 2025-09-19 09:39:43
- **Fuente de datos:** season_data.json
