# Análisis YRFI: Milwaukee Brewers @ Los Angeles Dodgers

**Fecha:** 2025-10-18  
**Lanzadores:** Jose Quintana (V) vs Shohei Ohtani (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 41.6%

## 🔍 Explicación de los Cálculos

### Los Angeles Dodgers (Local)
- **Estadística base YRFI:** 35.8% (29/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Milwaukee Brewers - Jose Quintana):** 25.0% (3/12 partidos)
- **Puntuación ajustada:** 26.4%

### Milwaukee Brewers (Visitante)
- **Estadística base YRFI:** 28.4% (23/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador local (Los Angeles Dodgers - Shohei Ohtani):** 28.6% (2/7 partidos)
- **Puntuación ajustada:** 20.7%

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

- **Generado el:** 2025-10-17 18:44:27
- **Fuente de datos:** season_data.json
