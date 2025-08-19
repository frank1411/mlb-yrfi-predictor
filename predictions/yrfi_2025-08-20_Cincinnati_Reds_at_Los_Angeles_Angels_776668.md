# Análisis YRFI: Cincinnati Reds @ Los Angeles Angels

**Fecha:** 2025-08-20  
**Lanzadores:** Hunter Greene (V) vs Kyle Hendricks (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 49.9%

## 🔍 Explicación de los Cálculos

### Los Angeles Angels (Local)
- **Estadística base YRFI:** 31.2% (20/64 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Cincinnati Reds - Hunter Greene):** 20.0% (1/5 partidos)
- **Puntuación ajustada:** 28.1%

### Cincinnati Reds (Visitante)
- **Estadística base YRFI:** 21.3% (13/61 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Los Angeles Angels - Kyle Hendricks):** 41.7% (5/12 partidos)
- **Puntuación ajustada:** 30.4%

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

- **Generado el:** 2025-08-19 12:49:11
- **Fuente de datos:** season_data.json
