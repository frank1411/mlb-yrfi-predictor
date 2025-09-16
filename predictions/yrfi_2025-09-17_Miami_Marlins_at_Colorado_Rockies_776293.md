# Análisis YRFI: Miami Marlins @ Colorado Rockies

**Fecha:** 2025-09-17  
**Lanzadores:** Eury Pérez (V) vs Kyle Freeland (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 57.9%

## 🔍 Explicación de los Cálculos

### Colorado Rockies (Local)
- **Estadística base YRFI:** 29.3% (22/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador visitante (Miami Marlins - Eury Pérez):** 60.0% (6/10 partidos)
- **Puntuación ajustada:** 32.0%

### Miami Marlins (Visitante)
- **Estadística base YRFI:** 26.4% (19/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Colorado Rockies - Kyle Freeland):** 46.2% (6/13 partidos)
- **Puntuación ajustada:** 38.2%

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

- **Generado el:** 2025-09-16 23:14:58
- **Fuente de datos:** season_data.json
