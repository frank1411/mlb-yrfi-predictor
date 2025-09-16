# Análisis YRFI: Baltimore Orioles @ Chicago White Sox

**Fecha:** 2025-09-16  
**Lanzadores:** Dean Kremer (V) vs Shane Smith (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 57.0%

## 🔍 Explicación de los Cálculos

### Chicago White Sox (Local)
- **Estadística base YRFI:** 30.7% (23/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Baltimore Orioles - Dean Kremer):** 43.8% (7/16 partidos)
- **Puntuación ajustada:** 38.6%

### Baltimore Orioles (Visitante)
- **Estadística base YRFI:** 26.3% (20/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Chicago White Sox - Shane Smith):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 30.1%

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

- **Generado el:** 2025-09-16 09:40:57
- **Fuente de datos:** season_data.json
