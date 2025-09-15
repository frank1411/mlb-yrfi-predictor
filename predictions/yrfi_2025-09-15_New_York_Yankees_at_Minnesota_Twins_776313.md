# Análisis YRFI: New York Yankees @ Minnesota Twins

**Fecha:** 2025-09-15  
**Lanzadores:** Carlos Rodón (V) vs Simeon Woods Richardson (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 46.8%

## 🔍 Explicación de los Cálculos

### Minnesota Twins (Local)
- **Estadística base YRFI:** 25.7% (19/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (New York Yankees - Carlos Rodón):** 18.8% (3/16 partidos)
- **Puntuación ajustada:** 21.2%

### New York Yankees (Visitante)
- **Estadística base YRFI:** 41.9% (31/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Minnesota Twins - Simeon Woods Richardson):** 10.0% (1/10 partidos)
- **Puntuación ajustada:** 32.4%

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

- **Generado el:** 2025-09-15 09:41:15
- **Fuente de datos:** season_data.json
