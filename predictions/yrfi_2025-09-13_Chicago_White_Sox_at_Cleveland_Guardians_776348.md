# Análisis YRFI: Chicago White Sox @ Cleveland Guardians

**Fecha:** 2025-09-13  
**Lanzadores:** Davis Martin (V) vs Parker Messick (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.0%

## 🔍 Explicación de los Cálculos

### Cleveland Guardians (Local)
- **Estadística base YRFI:** 32.9% (24/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Chicago White Sox - Davis Martin):** 45.5% (5/11 partidos)
- **Puntuación ajustada:** 35.1%

### Chicago White Sox (Visitante)
- **Estadística base YRFI:** 30.1% (22/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Cleveland Guardians - Parker Messick):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 18.4%

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

- **Generado el:** 2025-09-13 09:35:57
- **Fuente de datos:** season_data.json
