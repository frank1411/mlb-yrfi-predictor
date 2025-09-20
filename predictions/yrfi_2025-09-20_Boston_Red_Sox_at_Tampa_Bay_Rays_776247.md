# Análisis YRFI: Boston Red Sox @ Tampa Bay Rays

**Fecha:** 2025-09-20  
**Lanzadores:** Kyle Harrison (V) vs Adrian Houser (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 51.2%

## 🔍 Explicación de los Cálculos

### Tampa Bay Rays (Local)
- **Estadística base YRFI:** 35.4% (28/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Boston Red Sox - Kyle Harrison):** 33.3% (1/3 partidos)
- **Puntuación ajustada:** 38.7%

### Boston Red Sox (Visitante)
- **Estadística base YRFI:** 28.9% (22/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Tampa Bay Rays - Adrian Houser):** 0.0% (0/7 partidos)
- **Puntuación ajustada:** 20.4%

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

- **Generado el:** 2025-09-20 09:36:49
- **Fuente de datos:** season_data.json
