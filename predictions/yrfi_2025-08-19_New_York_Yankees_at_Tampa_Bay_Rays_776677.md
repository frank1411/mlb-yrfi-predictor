# Análisis YRFI: New York Yankees @ Tampa Bay Rays

**Fecha:** 2025-08-19  
**Lanzadores:** Carlos Rodón (V) vs Shane Baz (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 54.9%

## 🔍 Explicación de los Cálculos

### Tampa Bay Rays (Local)
- **Estadística base YRFI:** 32.3% (20/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (New York Yankees - Carlos Rodón):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 31.8%

### New York Yankees (Visitante)
- **Estadística base YRFI:** 38.7% (24/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Tampa Bay Rays - Shane Baz):** 16.7% (2/12 partidos)
- **Puntuación ajustada:** 33.8%

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

- **Generado el:** 2025-08-19 12:49:11
- **Fuente de datos:** season_data.json
