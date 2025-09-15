# Análisis YRFI: Cincinnati Reds @ St. Louis Cardinals

**Fecha:** 2025-09-15  
**Lanzadores:** Zack Littell (V) vs Matthew Liberatore (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 44.4%

## 🔍 Explicación de los Cálculos

### St. Louis Cardinals (Local)
- **Estadística base YRFI:** 20.0% (15/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Cincinnati Reds - Zack Littell):** 25.0% (4/16 partidos)
- **Puntuación ajustada:** 24.1%

### Cincinnati Reds (Visitante)
- **Estadística base YRFI:** 22.7% (17/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (St. Louis Cardinals - Matthew Liberatore):** 16.7% (2/12 partidos)
- **Puntuación ajustada:** 26.8%

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
