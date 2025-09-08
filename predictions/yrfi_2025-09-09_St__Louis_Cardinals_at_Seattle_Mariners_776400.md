# Análisis YRFI: St. Louis Cardinals @ Seattle Mariners

**Fecha:** 2025-09-09  
**Lanzadores:** Miles Mikolas (V) vs Bryan Woo (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 44.0%

## 🔍 Explicación de los Cálculos

### Seattle Mariners (Local)
- **Estadística base YRFI:** 20.6% (14/68 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (St. Louis Cardinals - Miles Mikolas):** 38.5% (5/13 partidos)
- **Puntuación ajustada:** 29.0%

### St. Louis Cardinals (Visitante)
- **Estadística base YRFI:** 26.1% (18/69 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (Seattle Mariners - Bryan Woo):** 25.0% (3/12 partidos)
- **Puntuación ajustada:** 21.1%

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

- **Generado el:** 2025-09-08 22:45:00
- **Fuente de datos:** season_data.json
