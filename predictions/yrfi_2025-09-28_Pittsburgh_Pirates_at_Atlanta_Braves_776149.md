# Análisis YRFI: Pittsburgh Pirates @ Atlanta Braves

**Fecha:** 2025-09-28  
**Lanzadores:** Johan Oviedo (V) vs Charlie Morton (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 50.6%

## 🔍 Explicación de los Cálculos

### Atlanta Braves (Local)
- **Estadística base YRFI:** 31.2% (25/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Pittsburgh Pirates - Johan Oviedo):** 25.0% (1/4 partidos)
- **Puntuación ajustada:** 27.4%

### Pittsburgh Pirates (Visitante)
- **Estadística base YRFI:** 26.2% (21/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Atlanta Braves - Charlie Morton):** 28.6% (4/14 partidos)
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

- **Generado el:** 2025-09-28 09:35:53
- **Fuente de datos:** season_data.json
