# Análisis YRFI: Arizona Diamondbacks @ Minnesota Twins

**Fecha:** 2025-09-14  
**Lanzadores:** Nabil Crismatt (V) vs Bailey Ober (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.5%

## 🔍 Explicación de los Cálculos

### Minnesota Twins (Local)
- **Estadística base YRFI:** 26.0% (19/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Arizona Diamondbacks - Nabil Crismatt):** 33.3% (1/3 partidos)
- **Puntuación ajustada:** 26.4%

### Arizona Diamondbacks (Visitante)
- **Estadística base YRFI:** 27.3% (21/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Minnesota Twins - Bailey Ober):** 25.0% (3/12 partidos)
- **Puntuación ajustada:** 28.6%

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

- **Generado el:** 2025-09-14 09:36:39
- **Fuente de datos:** season_data.json
