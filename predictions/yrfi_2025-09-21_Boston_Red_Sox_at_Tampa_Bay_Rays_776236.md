# Análisis YRFI: Boston Red Sox @ Tampa Bay Rays

**Fecha:** 2025-09-21  
**Lanzadores:** Connelly Early (V) vs Joe Boyle (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 39.8%

## 🔍 Explicación de los Cálculos

### Tampa Bay Rays (Local)
- **Estadística base YRFI:** 35.0% (28/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Boston Red Sox - Connelly Early):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 24.5%

### Boston Red Sox (Visitante)
- **Estadística base YRFI:** 28.6% (22/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Tampa Bay Rays - Joe Boyle):** 0.0% (0/4 partidos)
- **Puntuación ajustada:** 20.3%

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
