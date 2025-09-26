# Análisis YRFI: Cincinnati Reds @ Milwaukee Brewers

**Fecha:** 2025-09-27  
**Lanzadores:** Zack Littell (V) vs Quinn Priester (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 32.5%

## 🔍 Explicación de los Cálculos

### Milwaukee Brewers (Local)
- **Estadística base YRFI:** 17.9% (14/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (Cincinnati Reds - Zack Littell):** 23.5% (4/17 partidos)
- **Puntuación ajustada:** 18.2%

### Cincinnati Reds (Visitante)
- **Estadística base YRFI:** 21.8% (17/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Milwaukee Brewers - Quinn Priester):** 11.1% (1/9 partidos)
- **Puntuación ajustada:** 17.4%

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
