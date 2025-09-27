# Análisis YRFI: Colorado Rockies @ San Francisco Giants

**Fecha:** 2025-09-27  
**Lanzadores:** Kyle Freeland (V) vs Justin Verlander (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.1%

## 🔍 Explicación de los Cálculos

### San Francisco Giants (Local)
- **Estadística base YRFI:** 32.9% (26/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador visitante (Colorado Rockies - Kyle Freeland):** 46.7% (7/15 partidos)
- **Puntuación ajustada:** 45.0%

### Colorado Rockies (Visitante)
- **Estadística base YRFI:** 12.7% (10/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (San Francisco Giants - Justin Verlander):** 12.5% (2/16 partidos)
- **Puntuación ajustada:** 12.8%

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

- **Generado el:** 2025-09-27 09:36:25
- **Fuente de datos:** season_data.json
