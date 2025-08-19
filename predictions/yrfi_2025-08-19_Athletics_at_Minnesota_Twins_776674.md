# Análisis YRFI: Athletics @ Minnesota Twins

**Fecha:** 2025-08-19  
**Lanzadores:** Jacob Lopez (V) vs Joe Ryan (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 44.9%

## 🔍 Explicación de los Cálculos

### Minnesota Twins (Local)
- **Estadística base YRFI:** 27.9% (17/61 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Athletics - Jacob Lopez):** 0.0% (0/8 partidos)
- **Puntuación ajustada:** 22.4%

### Athletics (Visitante)
- **Estadística base YRFI:** 30.2% (19/63 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Minnesota Twins - Joe Ryan):** 16.7% (2/12 partidos)
- **Puntuación ajustada:** 28.9%

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
