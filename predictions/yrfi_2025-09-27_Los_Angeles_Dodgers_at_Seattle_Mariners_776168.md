# Análisis YRFI: Los Angeles Dodgers @ Seattle Mariners

**Fecha:** 2025-09-27  
**Lanzadores:** Emmet Sheehan (V) vs Por anunciar (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 59.0%

## 🔍 Explicación de los Cálculos

### Seattle Mariners (Local)
- **Estadística base YRFI:** 21.8% (17/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Emmet Sheehan):** 50.0% (2/4 partidos)
- **Puntuación ajustada:** 38.2%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 30.8% (24/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Seattle Mariners - Por anunciar):** 50.0% (0/0 partidos)
- **Puntuación ajustada:** 33.6%

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
