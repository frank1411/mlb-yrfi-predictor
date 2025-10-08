# Análisis YRFI: Philadelphia Phillies @ Los Angeles Dodgers

**Fecha:** 2025-10-09  
**Lanzadores:** Aaron Nola (V) vs Yoshinobu Yamamoto (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 53.9%

## 🔍 Explicación de los Cálculos

### Los Angeles Dodgers (Local)
- **Estadística base YRFI:** 35.8% (29/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Philadelphia Phillies - Aaron Nola):** 37.5% (3/8 partidos)
- **Puntuación ajustada:** 30.8%

### Philadelphia Phillies (Visitante)
- **Estadística base YRFI:** 27.2% (22/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Los Angeles Dodgers - Yoshinobu Yamamoto):** 25.0% (3/12 partidos)
- **Puntuación ajustada:** 33.4%

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

- **Generado el:** 2025-10-08 09:40:28
- **Fuente de datos:** season_data.json
