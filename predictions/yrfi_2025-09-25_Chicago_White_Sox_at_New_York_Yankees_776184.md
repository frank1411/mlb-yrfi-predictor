# Análisis YRFI: Chicago White Sox @ New York Yankees

**Fecha:** 2025-09-25  
**Lanzadores:** Davis Martin (V) vs Carlos Rodón (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 63.5%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 33.8% (26/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador visitante (Chicago White Sox - Davis Martin):** 41.7% (5/12 partidos)
- **Puntuación ajustada:** 43.5%

### Chicago White Sox (Visitante)
- **Estadística base YRFI:** 29.9% (23/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (New York Yankees - Carlos Rodón):** 21.4% (3/14 partidos)
- **Puntuación ajustada:** 35.3%

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

- **Generado el:** 2025-09-25 09:40:11
- **Fuente de datos:** season_data.json
