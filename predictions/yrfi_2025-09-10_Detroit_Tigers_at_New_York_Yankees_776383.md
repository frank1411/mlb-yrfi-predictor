# Análisis YRFI: Detroit Tigers @ New York Yankees

**Fecha:** 2025-09-10  
**Lanzadores:** Jack Flaherty (V) vs Carlos Rodón (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 48.9%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 34.2% (25/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Detroit Tigers - Jack Flaherty):** 16.7% (2/12 partidos)
- **Puntuación ajustada:** 32.5%

### Detroit Tigers (Visitante)
- **Estadística base YRFI:** 22.9% (16/70 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (New York Yankees - Carlos Rodón):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 24.3%

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

- **Generado el:** 2025-09-10 09:39:09
- **Fuente de datos:** season_data.json
