# Análisis YRFI: Tampa Bay Rays @ Chicago Cubs

**Fecha:** 2025-09-13  
**Lanzadores:** Drew Rasmussen (V) vs Colin Rea (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 53.0%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 27.4% (20/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Tampa Bay Rays - Drew Rasmussen):** 27.3% (3/11 partidos)
- **Puntuación ajustada:** 27.1%

### Tampa Bay Rays (Visitante)
- **Estadística base YRFI:** 24.7% (18/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Colin Rea):** 33.3% (5/15 partidos)
- **Puntuación ajustada:** 35.6%

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
