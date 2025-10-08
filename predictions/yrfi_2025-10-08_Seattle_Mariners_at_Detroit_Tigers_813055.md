# Análisis YRFI: Seattle Mariners @ Detroit Tigers

**Fecha:** 2025-10-08  
**Lanzadores:** Bryce Miller (V) vs Casey Mize (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.3%

## 🔍 Explicación de los Cálculos

### Detroit Tigers (Local)
- **Estadística base YRFI:** 30.9% (25/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (Seattle Mariners - Bryce Miller):** 44.4% (4/9 partidos)
- **Puntuación ajustada:** 29.4%

### Seattle Mariners (Visitante)
- **Estadística base YRFI:** 37.0% (30/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Detroit Tigers - Casey Mize):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 32.5%

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

- **Generado el:** 2025-10-08 09:40:28
- **Fuente de datos:** season_data.json
