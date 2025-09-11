# Análisis YRFI: Tampa Bay Rays @ Chicago White Sox

**Fecha:** 2025-09-11  
**Lanzadores:** Ian Seymour (V) vs Shane Smith (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 40.9%

## 🔍 Explicación de los Cálculos

### Chicago White Sox (Local)
- **Estadística base YRFI:** 28.8% (21/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Tampa Bay Rays - Ian Seymour):** 0.0% (0/2 partidos)
- **Puntuación ajustada:** 15.6%

### Tampa Bay Rays (Visitante)
- **Estadística base YRFI:** 23.9% (17/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Chicago White Sox - Shane Smith):** 25.0% (3/12 partidos)
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

- **Generado el:** 2025-09-11 09:38:55
- **Fuente de datos:** season_data.json
