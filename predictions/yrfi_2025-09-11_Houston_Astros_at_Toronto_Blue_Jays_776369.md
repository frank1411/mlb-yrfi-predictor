# Análisis YRFI: Houston Astros @ Toronto Blue Jays

**Fecha:** 2025-09-11  
**Lanzadores:** Cristian Javier (V) vs Kevin Gausman (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 68.4%

## 🔍 Explicación de los Cálculos

### Toronto Blue Jays (Local)
- **Estadística base YRFI:** 29.6% (21/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Houston Astros - Cristian Javier):** 100.0% (1/1 partidos)
- **Puntuación ajustada:** 55.6%

### Houston Astros (Visitante)
- **Estadística base YRFI:** 28.2% (20/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Toronto Blue Jays - Kevin Gausman):** 38.5% (5/13 partidos)
- **Puntuación ajustada:** 28.9%

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
