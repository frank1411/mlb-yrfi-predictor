# Análisis YRFI: Chicago Cubs @ Cincinnati Reds

**Fecha:** 2025-09-19  
**Lanzadores:** Shota Imanaga (V) vs Nick Lodolo (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 59.7%

## 🔍 Explicación de los Cálculos

### Cincinnati Reds (Local)
- **Estadística base YRFI:** 40.0% (30/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Chicago Cubs - Shota Imanaga):** 41.7% (5/12 partidos)
- **Puntuación ajustada:** 35.8%

### Chicago Cubs (Visitante)
- **Estadística base YRFI:** 32.1% (25/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Cincinnati Reds - Nick Lodolo):** 45.5% (5/11 partidos)
- **Puntuación ajustada:** 37.2%

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
