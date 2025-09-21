# Análisis YRFI: San Diego Padres @ Chicago White Sox

**Fecha:** 2025-09-21  
**Lanzadores:** Michael King (V) vs Sean Burke (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 63.0%

## 🔍 Explicación de los Cálculos

### Chicago White Sox (Local)
- **Estadística base YRFI:** 32.9% (26/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador visitante (San Diego Padres - Michael King):** 25.0% (1/4 partidos)
- **Puntuación ajustada:** 39.8%

### San Diego Padres (Visitante)
- **Estadística base YRFI:** 26.2% (21/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Chicago White Sox - Sean Burke):** 53.8% (7/13 partidos)
- **Puntuación ajustada:** 38.4%

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

- **Generado el:** 2025-09-21 09:36:24
- **Fuente de datos:** season_data.json
