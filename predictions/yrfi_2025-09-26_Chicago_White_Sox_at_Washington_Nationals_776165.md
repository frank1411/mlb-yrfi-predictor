# Análisis YRFI: Chicago White Sox @ Washington Nationals

**Fecha:** 2025-09-26  
**Lanzadores:** Yoendrys Gómez (V) vs Cade Cavalli (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 51.7%

## 🔍 Explicación de los Cálculos

### Washington Nationals (Local)
- **Estadística base YRFI:** 26.9% (21/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Chicago White Sox - Yoendrys Gómez):** 33.3% (1/3 partidos)
- **Puntuación ajustada:** 26.7%

### Chicago White Sox (Visitante)
- **Estadística base YRFI:** 29.5% (23/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Washington Nationals - Cade Cavalli):** 25.0% (1/4 partidos)
- **Puntuación ajustada:** 34.1%

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

- **Generado el:** 2025-09-26 09:39:49
- **Fuente de datos:** season_data.json
