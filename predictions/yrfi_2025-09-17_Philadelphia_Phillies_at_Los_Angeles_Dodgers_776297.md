# Análisis YRFI: Philadelphia Phillies @ Los Angeles Dodgers

**Fecha:** 2025-09-17  
**Lanzadores:** Cristopher Sánchez (V) vs Shohei Ohtani (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.1%

## 🔍 Explicación de los Cálculos

### Los Angeles Dodgers (Local)
- **Estadística base YRFI:** 37.3% (28/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Philadelphia Phillies - Cristopher Sánchez):** 18.8% (3/16 partidos)
- **Puntuación ajustada:** 24.6%

### Philadelphia Phillies (Visitante)
- **Estadística base YRFI:** 27.6% (21/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Los Angeles Dodgers - Shohei Ohtani):** 33.3% (2/6 partidos)
- **Puntuación ajustada:** 36.4%

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

- **Generado el:** 2025-09-16 23:14:58
- **Fuente de datos:** season_data.json
