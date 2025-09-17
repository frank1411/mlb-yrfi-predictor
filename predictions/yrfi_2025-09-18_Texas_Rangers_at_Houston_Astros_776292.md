# Análisis YRFI: Texas Rangers @ Houston Astros

**Fecha:** 2025-09-18  
**Lanzadores:** Jacob deGrom (V) vs Cristian Javier (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 41.3%

## 🔍 Explicación de los Cálculos

### Houston Astros (Local)
- **Estadística base YRFI:** 24.7% (19/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Texas Rangers - Jacob deGrom):** 28.6% (4/14 partidos)
- **Puntuación ajustada:** 26.8%

### Texas Rangers (Visitante)
- **Estadística base YRFI:** 29.9% (23/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador local (Houston Astros - Cristian Javier):** 25.0% (1/4 partidos)
- **Puntuación ajustada:** 19.9%

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

- **Generado el:** 2025-09-17 09:39:33
- **Fuente de datos:** season_data.json
