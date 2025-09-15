# Análisis YRFI: San Francisco Giants @ Arizona Diamondbacks

**Fecha:** 2025-09-16  
**Lanzadores:** Kai-Wei Teng (V) vs Zac Gallen (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 65.8%

## 🔍 Explicación de los Cálculos

### Arizona Diamondbacks (Local)
- **Estadística base YRFI:** 45.8% (33/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (San Francisco Giants - Kai-Wei Teng):** 50.0% (2/4 partidos)
- **Puntuación ajustada:** 42.8%

### San Francisco Giants (Visitante)
- **Estadística base YRFI:** 32.4% (24/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador local (Arizona Diamondbacks - Zac Gallen):** 26.7% (4/15 partidos)
- **Puntuación ajustada:** 40.3%

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

- **Generado el:** 2025-09-15 09:41:15
- **Fuente de datos:** season_data.json
