# Análisis YRFI: Detroit Tigers @ Boston Red Sox

**Fecha:** 2025-09-26  
**Lanzadores:** Casey Mize (V) vs Kyle Harrison (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 65.1%

## 🔍 Explicación de los Cálculos

### Boston Red Sox (Local)
- **Estadística base YRFI:** 34.6% (27/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Detroit Tigers - Casey Mize):** 30.8% (4/13 partidos)
- **Puntuación ajustada:** 35.2%

### Detroit Tigers (Visitante)
- **Estadística base YRFI:** 21.8% (17/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (Boston Red Sox - Kyle Harrison):** 100.0% (1/1 partidos)
- **Puntuación ajustada:** 46.1%

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

- **Generado el:** 2025-09-26 09:39:49
- **Fuente de datos:** season_data.json
