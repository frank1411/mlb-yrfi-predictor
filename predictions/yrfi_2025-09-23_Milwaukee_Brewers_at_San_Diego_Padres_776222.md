# Análisis YRFI: Milwaukee Brewers @ San Diego Padres

**Fecha:** 2025-09-23  
**Lanzadores:** Freddy Peralta (V) vs Nick Pivetta (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.8%

## 🔍 Explicación de los Cálculos

### San Diego Padres (Local)
- **Estadística base YRFI:** 25.3% (19/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (Milwaukee Brewers - Freddy Peralta):** 20.0% (3/15 partidos)
- **Puntuación ajustada:** 26.3%

### Milwaukee Brewers (Visitante)
- **Estadística base YRFI:** 29.5% (23/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (San Diego Padres - Nick Pivetta):** 31.2% (5/16 partidos)
- **Puntuación ajustada:** 29.1%

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

- **Generado el:** 2025-09-22 13:39:41
- **Fuente de datos:** season_data.json
