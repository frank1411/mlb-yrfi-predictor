# Análisis YRFI: Detroit Tigers @ New York Yankees

**Fecha:** 2025-09-09  
**Lanzadores:** Casey Mize (V) vs Will Warren (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.1%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 33.3% (24/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Detroit Tigers - Casey Mize):** 25.0% (3/12 partidos)
- **Puntuación ajustada:** 32.8%

### Detroit Tigers (Visitante)
- **Estadística base YRFI:** 23.2% (16/69 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (New York Yankees - Will Warren):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 21.3%

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

- **Generado el:** 2025-09-09 20:25:51
- **Fuente de datos:** season_data.json
