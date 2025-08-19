# Análisis YRFI: San Francisco Giants @ San Diego Padres

**Fecha:** 2025-08-20  
**Lanzadores:** Kai-Wei Teng (V) vs Nick Pivetta (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 62.1%

## 🔍 Explicación de los Cálculos

### San Diego Padres (Local)
- **Estadística base YRFI:** 23.7% (14/59 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (San Francisco Giants - Kai-Wei Teng):** 100.0% (1/1 partidos)
- **Puntuación ajustada:** 46.7%

### San Francisco Giants (Visitante)
- **Estadística base YRFI:** 30.6% (19/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (San Diego Padres - Nick Pivetta):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 29.0%

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
