# Análisis YRFI: San Diego Padres @ Chicago White Sox

**Fecha:** 2025-09-19  
**Lanzadores:** Dylan Cease (V) vs Davis Martin (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.8%

## 🔍 Explicación de los Cálculos

### Chicago White Sox (Local)
- **Estadística base YRFI:** 31.2% (24/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (San Diego Padres - Dylan Cease):** 33.3% (5/15 partidos)
- **Puntuación ajustada:** 37.5%

### San Diego Padres (Visitante)
- **Estadística base YRFI:** 26.9% (21/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Chicago White Sox - Davis Martin):** 27.3% (3/11 partidos)
- **Puntuación ajustada:** 29.3%

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
