# Análisis YRFI: Chicago White Sox @ New York Yankees

**Fecha:** 2025-09-23  
**Lanzadores:** Shane Smith (V) vs Luis Gil (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 63.3%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 34.7% (26/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador visitante (Chicago White Sox - Shane Smith):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 39.7%

### Chicago White Sox (Visitante)
- **Estadística base YRFI:** 30.7% (23/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador local (New York Yankees - Luis Gil):** 25.0% (1/4 partidos)
- **Puntuación ajustada:** 39.2%

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

- **Generado el:** 2025-09-23 09:40:26
- **Fuente de datos:** season_data.json
