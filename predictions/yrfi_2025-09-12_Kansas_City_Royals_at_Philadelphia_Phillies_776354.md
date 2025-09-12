# Análisis YRFI: Kansas City Royals @ Philadelphia Phillies

**Fecha:** 2025-09-12  
**Lanzadores:** Michael Lorenzen (V) vs Walker Buehler (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 46.4%

## 🔍 Explicación de los Cálculos

### Philadelphia Phillies (Local)
- **Estadística base YRFI:** 38.9% (28/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Kansas City Royals - Michael Lorenzen):** 7.7% (1/13 partidos)
- **Puntuación ajustada:** 26.0%

### Kansas City Royals (Visitante)
- **Estadística base YRFI:** 29.2% (21/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Philadelphia Phillies - Walker Buehler):** 27.3% (3/11 partidos)
- **Puntuación ajustada:** 27.6%

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

- **Generado el:** 2025-09-12 09:38:12
- **Fuente de datos:** season_data.json
