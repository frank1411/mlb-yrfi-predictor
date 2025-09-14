# Análisis YRFI: Cincinnati Reds @ Athletics

**Fecha:** 2025-09-14  
**Lanzadores:** Nick Lodolo (V) vs Luis Morales (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.8%

## 🔍 Explicación de los Cálculos

### Athletics (Local)
- **Estadística base YRFI:** 36.5% (27/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Cincinnati Reds - Nick Lodolo):** 28.6% (4/14 partidos)
- **Puntuación ajustada:** 32.6%

### Cincinnati Reds (Visitante)
- **Estadística base YRFI:** 21.6% (16/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Athletics - Luis Morales):** 33.3% (1/3 partidos)
- **Puntuación ajustada:** 29.9%

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

- **Generado el:** 2025-09-14 09:36:39
- **Fuente de datos:** season_data.json
