# Análisis YRFI: New York Yankees @ Minnesota Twins

**Fecha:** 2025-09-16  
**Lanzadores:** Cam Schlittler (V) vs Zebby Matthews (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 54.0%

## 🔍 Explicación de los Cálculos

### Minnesota Twins (Local)
- **Estadística base YRFI:** 25.3% (19/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (New York Yankees - Cam Schlittler):** 50.0% (2/4 partidos)
- **Puntuación ajustada:** 32.1%

### New York Yankees (Visitante)
- **Estadística base YRFI:** 41.3% (31/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Minnesota Twins - Zebby Matthews):** 16.7% (1/6 partidos)
- **Puntuación ajustada:** 32.2%

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

- **Generado el:** 2025-09-16 09:40:57
- **Fuente de datos:** season_data.json
