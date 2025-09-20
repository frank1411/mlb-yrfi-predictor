# Análisis YRFI: Milwaukee Brewers @ St. Louis Cardinals

**Fecha:** 2025-09-20  
**Lanzadores:** Chad Patrick (V) vs Miles Mikolas (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.2%

## 🔍 Explicación de los Cálculos

### St. Louis Cardinals (Local)
- **Estadística base YRFI:** 22.8% (18/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Milwaukee Brewers - Chad Patrick):** 33.3% (3/9 partidos)
- **Puntuación ajustada:** 30.2%

### Milwaukee Brewers (Visitante)
- **Estadística base YRFI:** 30.3% (23/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (St. Louis Cardinals - Miles Mikolas):** 42.9% (6/14 partidos)
- **Puntuación ajustada:** 35.8%

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
