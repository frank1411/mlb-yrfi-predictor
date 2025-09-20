# Análisis YRFI: San Diego Padres @ Chicago White Sox

**Fecha:** 2025-09-20  
**Lanzadores:** Yu Darvish (V) vs Yoendrys Gómez (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 61.3%

## 🔍 Explicación de los Cálculos

### Chicago White Sox (Local)
- **Estadística base YRFI:** 32.1% (25/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador visitante (San Diego Padres - Yu Darvish):** 50.0% (3/6 partidos)
- **Puntuación ajustada:** 45.9%

### San Diego Padres (Visitante)
- **Estadística base YRFI:** 26.6% (21/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Chicago White Sox - Yoendrys Gómez):** 25.0% (1/4 partidos)
- **Puntuación ajustada:** 28.4%

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

- **Generado el:** 2025-09-20 09:36:49
- **Fuente de datos:** season_data.json
