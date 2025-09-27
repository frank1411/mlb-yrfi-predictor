# Análisis YRFI: Chicago White Sox @ Washington Nationals

**Fecha:** 2025-09-27  
**Lanzadores:** Sean Burke (V) vs Jake Irvin (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 64.7%

## 🔍 Explicación de los Cálculos

### Washington Nationals (Local)
- **Estadística base YRFI:** 27.8% (22/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Chicago White Sox - Sean Burke):** 50.0% (4/8 partidos)
- **Puntuación ajustada:** 35.2%

### Chicago White Sox (Visitante)
- **Estadística base YRFI:** 30.4% (24/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Washington Nationals - Jake Irvin):** 57.1% (8/14 partidos)
- **Puntuación ajustada:** 45.6%

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

- **Generado el:** 2025-09-27 09:36:25
- **Fuente de datos:** season_data.json
