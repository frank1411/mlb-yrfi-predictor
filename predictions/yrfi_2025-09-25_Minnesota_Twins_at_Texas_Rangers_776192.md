# Análisis YRFI: Minnesota Twins @ Texas Rangers

**Fecha:** 2025-09-25  
**Lanzadores:** Taj Bradley (V) vs Jacob deGrom (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 44.8%

## 🔍 Explicación de los Cálculos

### Texas Rangers (Local)
- **Estadística base YRFI:** 22.8% (18/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (Minnesota Twins - Taj Bradley):** 41.7% (5/12 partidos)
- **Puntuación ajustada:** 26.0%

### Minnesota Twins (Visitante)
- **Estadística base YRFI:** 27.6% (21/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (Texas Rangers - Jacob deGrom):** 35.7% (5/14 partidos)
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

- **Generado el:** 2025-09-24 09:40:51
- **Fuente de datos:** season_data.json
