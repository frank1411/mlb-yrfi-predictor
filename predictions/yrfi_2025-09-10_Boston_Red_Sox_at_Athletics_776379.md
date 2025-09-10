# Análisis YRFI: Boston Red Sox @ Athletics

**Fecha:** 2025-09-10  
**Lanzadores:** Payton Tolle (V) vs Mason Barnett (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 65.2%

## 🔍 Explicación de los Cálculos

### Athletics (Local)
- **Estadística base YRFI:** 35.2% (25/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Boston Red Sox - Payton Tolle):** 100.0% (1/1 partidos)
- **Puntuación ajustada:** 54.8%

### Boston Red Sox (Visitante)
- **Estadística base YRFI:** 29.7% (22/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Athletics - Mason Barnett):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 23.0%

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

- **Generado el:** 2025-09-10 09:39:09
- **Fuente de datos:** season_data.json
