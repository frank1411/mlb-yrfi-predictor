# Análisis YRFI: San Francisco Giants @ Los Angeles Dodgers

**Fecha:** 2025-09-21  
**Lanzadores:** Kai-Wei Teng (V) vs Tyler Glasnow (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.9%

## 🔍 Explicación de los Cálculos

### Los Angeles Dodgers (Local)
- **Estadística base YRFI:** 35.4% (28/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (San Francisco Giants - Kai-Wei Teng):** 60.0% (3/5 partidos)
- **Puntuación ajustada:** 36.1%

### San Francisco Giants (Visitante)
- **Estadística base YRFI:** 32.9% (26/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Los Angeles Dodgers - Tyler Glasnow):** 20.0% (2/10 partidos)
- **Puntuación ajustada:** 30.9%

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
