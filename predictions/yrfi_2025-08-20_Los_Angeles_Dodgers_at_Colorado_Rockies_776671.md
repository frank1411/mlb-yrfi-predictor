# Análisis YRFI: Los Angeles Dodgers @ Colorado Rockies

**Fecha:** 2025-08-20  
**Lanzadores:** Emmet Sheehan (V) vs Austin Gomber (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 63.3%

## 🔍 Explicación de los Cálculos

### Colorado Rockies (Local)
- **Estadística base YRFI:** 33.3% (21/63 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Emmet Sheehan):** 50.0% (1/2 partidos)
- **Puntuación ajustada:** 34.4%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 30.0% (18/60 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Colorado Rockies - Austin Gomber):** 60.0% (3/5 partidos)
- **Puntuación ajustada:** 44.1%

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
