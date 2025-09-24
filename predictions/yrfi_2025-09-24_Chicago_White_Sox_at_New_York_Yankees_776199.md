# Análisis YRFI: Chicago White Sox @ New York Yankees

**Fecha:** 2025-09-24  
**Lanzadores:** Fraser Ellard (V) vs Max Fried (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 59.2%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 34.2% (26/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador visitante (Chicago White Sox - Fraser Ellard):** 0.0% (0/2 partidos)
- **Puntuación ajustada:** 31.5%

### Chicago White Sox (Visitante)
- **Estadística base YRFI:** 30.3% (23/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (New York Yankees - Max Fried):** 35.7% (5/14 partidos)
- **Puntuación ajustada:** 40.4%

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

- **Generado el:** 2025-09-24 09:40:51
- **Fuente de datos:** season_data.json
