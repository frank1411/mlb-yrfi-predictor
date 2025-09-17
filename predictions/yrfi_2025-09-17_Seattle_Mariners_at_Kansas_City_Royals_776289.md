# Análisis YRFI: Seattle Mariners @ Kansas City Royals

**Fecha:** 2025-09-17  
**Lanzadores:** Bryce Miller (V) vs Cole Ragans (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 51.5%

## 🔍 Explicación de los Cálculos

### Kansas City Royals (Local)
- **Estadística base YRFI:** 31.6% (24/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Seattle Mariners - Bryce Miller):** 37.5% (3/8 partidos)
- **Puntuación ajustada:** 34.3%

### Seattle Mariners (Visitante)
- **Estadística base YRFI:** 36.8% (28/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Kansas City Royals - Cole Ragans):** 16.7% (1/6 partidos)
- **Puntuación ajustada:** 26.1%

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

- **Generado el:** 2025-09-17 09:39:33
- **Fuente de datos:** season_data.json
