# Análisis YRFI: Chicago Cubs @ Atlanta Braves

**Fecha:** 2025-09-10  
**Lanzadores:** Por anunciar (V) vs Chris Sale (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 57.9%

## 🔍 Explicación de los Cálculos

### Atlanta Braves (Local)
- **Estadística base YRFI:** 31.0% (22/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Chicago Cubs - Por anunciar):** 50.0% (0/0 partidos)
- **Puntuación ajustada:** 40.9%

### Chicago Cubs (Visitante)
- **Estadística base YRFI:** 31.5% (23/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Atlanta Braves - Chris Sale):** 28.6% (2/7 partidos)
- **Puntuación ajustada:** 28.8%

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
