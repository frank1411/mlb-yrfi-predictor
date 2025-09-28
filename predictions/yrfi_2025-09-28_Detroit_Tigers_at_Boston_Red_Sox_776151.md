# Análisis YRFI: Detroit Tigers @ Boston Red Sox

**Fecha:** 2025-09-28  
**Lanzadores:** Chris Paddack (V) vs Por anunciar (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.7%

## 🔍 Explicación de los Cálculos

### Boston Red Sox (Local)
- **Estadística base YRFI:** 33.8% (27/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Detroit Tigers - Chris Paddack):** 46.7% (7/15 partidos)
- **Puntuación ajustada:** 38.1%

### Detroit Tigers (Visitante)
- **Estadística base YRFI:** 21.2% (17/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (Boston Red Sox - Por anunciar):** 50.0% (0/0 partidos)
- **Puntuación ajustada:** 28.5%

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

- **Generado el:** 2025-09-28 09:35:53
- **Fuente de datos:** season_data.json
