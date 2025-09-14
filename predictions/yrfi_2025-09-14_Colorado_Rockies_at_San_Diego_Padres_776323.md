# Análisis YRFI: Colorado Rockies @ San Diego Padres

**Fecha:** 2025-09-14  
**Lanzadores:** Germán Márquez (V) vs Yu Darvish (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 42.9%

## 🔍 Explicación de los Cálculos

### San Diego Padres (Local)
- **Estadística base YRFI:** 24.3% (18/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Colorado Rockies - Germán Márquez):** 46.2% (6/13 partidos)
- **Puntuación ajustada:** 30.4%

### Colorado Rockies (Visitante)
- **Estadística base YRFI:** 13.5% (10/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador local (San Diego Padres - Yu Darvish):** 33.3% (2/6 partidos)
- **Puntuación ajustada:** 18.0%

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

- **Generado el:** 2025-09-14 09:36:39
- **Fuente de datos:** season_data.json
