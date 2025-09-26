# Análisis YRFI: Arizona Diamondbacks @ San Diego Padres

**Fecha:** 2025-09-27  
**Lanzadores:** Zac Gallen (V) vs Yu Darvish (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 58.2%

## 🔍 Explicación de los Cálculos

### San Diego Padres (Local)
- **Estadística base YRFI:** 26.9% (21/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Arizona Diamondbacks - Zac Gallen):** 40.0% (6/15 partidos)
- **Puntuación ajustada:** 36.2%

### Arizona Diamondbacks (Visitante)
- **Estadística base YRFI:** 26.9% (21/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (San Diego Padres - Yu Darvish):** 28.6% (2/7 partidos)
- **Puntuación ajustada:** 34.6%

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
