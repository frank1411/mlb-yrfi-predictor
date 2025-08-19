# Análisis YRFI: St. Louis Cardinals @ Miami Marlins

**Fecha:** 2025-08-19  
**Lanzadores:** Michael McGreevy (V) vs Edward Cabrera (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 41.1%

## 🔍 Explicación de los Cálculos

### Miami Marlins (Local)
- **Estadística base YRFI:** 30.0% (18/60 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (St. Louis Cardinals - Michael McGreevy):** 33.3% (1/3 partidos)
- **Puntuación ajustada:** 30.0%

### St. Louis Cardinals (Visitante)
- **Estadística base YRFI:** 24.6% (15/61 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador local (Miami Marlins - Edward Cabrera):** 18.2% (2/11 partidos)
- **Puntuación ajustada:** 15.9%

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
