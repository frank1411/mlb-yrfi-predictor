# Análisis YRFI: Miami Marlins @ Colorado Rockies

**Fecha:** 2025-09-18  
**Lanzadores:** Sandy Alcantara (V) vs Tanner Gordon (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 45.8%

## 🔍 Explicación de los Cálculos

### Colorado Rockies (Local)
- **Estadística base YRFI:** 28.6% (22/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador visitante (Miami Marlins - Sandy Alcantara):** 33.3% (4/12 partidos)
- **Puntuación ajustada:** 22.4%

### Miami Marlins (Visitante)
- **Estadística base YRFI:** 25.7% (19/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Colorado Rockies - Tanner Gordon):** 37.5% (3/8 partidos)
- **Puntuación ajustada:** 30.2%

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

- **Generado el:** 2025-09-18 09:39:37
- **Fuente de datos:** season_data.json
