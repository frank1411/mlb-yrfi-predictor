# Análisis YRFI: Seattle Mariners @ Kansas City Royals

**Fecha:** 2025-09-18  
**Lanzadores:** Luis Castillo (V) vs Stephen Kolek (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.6%

## 🔍 Explicación de los Cálculos

### Kansas City Royals (Local)
- **Estadística base YRFI:** 32.5% (25/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Seattle Mariners - Luis Castillo):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 28.8%

### Seattle Mariners (Visitante)
- **Estadística base YRFI:** 36.4% (28/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Kansas City Royals - Stephen Kolek):** 50.0% (3/6 partidos)
- **Puntuación ajustada:** 37.7%

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

- **Generado el:** 2025-09-18 09:39:37
- **Fuente de datos:** season_data.json
