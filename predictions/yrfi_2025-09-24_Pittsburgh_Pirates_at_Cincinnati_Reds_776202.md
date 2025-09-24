# Análisis YRFI: Pittsburgh Pirates @ Cincinnati Reds

**Fecha:** 2025-09-24  
**Lanzadores:** Paul Skenes (V) vs Hunter Greene (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 44.9%

## 🔍 Explicación de los Cálculos

### Cincinnati Reds (Local)
- **Estadística base YRFI:** 39.2% (31/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Pittsburgh Pirates - Paul Skenes):** 6.2% (1/16 partidos)
- **Puntuación ajustada:** 23.2%

### Pittsburgh Pirates (Visitante)
- **Estadística base YRFI:** 27.6% (21/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Cincinnati Reds - Hunter Greene):** 10.0% (1/10 partidos)
- **Puntuación ajustada:** 28.3%

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
