# Análisis YRFI: Houston Astros @ Detroit Tigers

**Fecha:** 2025-08-19  
**Lanzadores:** Hunter Brown (V) vs Tarik Skubal (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.0%

## 🔍 Explicación de los Cálculos

### Detroit Tigers (Local)
- **Estadística base YRFI:** 29.7% (19/64 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Houston Astros - Hunter Brown):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 23.9%

### Houston Astros (Visitante)
- **Estadística base YRFI:** 28.3% (17/60 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Detroit Tigers - Tarik Skubal):** 15.4% (2/13 partidos)
- **Puntuación ajustada:** 30.4%

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
