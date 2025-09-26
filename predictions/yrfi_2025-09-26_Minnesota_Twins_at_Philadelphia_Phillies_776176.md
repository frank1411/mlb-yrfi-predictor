# Análisis YRFI: Minnesota Twins @ Philadelphia Phillies

**Fecha:** 2025-09-26  
**Lanzadores:** Joe Ryan (V) vs Aaron Nola (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 61.7%

## 🔍 Explicación de los Cálculos

### Philadelphia Phillies (Local)
- **Estadística base YRFI:** 41.0% (32/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador visitante (Minnesota Twins - Joe Ryan):** 42.9% (6/14 partidos)
- **Puntuación ajustada:** 46.1%

### Minnesota Twins (Visitante)
- **Estadística base YRFI:** 29.5% (23/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Philadelphia Phillies - Aaron Nola):** 37.5% (3/8 partidos)
- **Puntuación ajustada:** 28.9%

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

- **Generado el:** 2025-09-26 09:39:49
- **Fuente de datos:** season_data.json
