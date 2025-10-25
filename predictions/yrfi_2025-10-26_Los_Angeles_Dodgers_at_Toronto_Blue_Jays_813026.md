# Análisis YRFI: Los Angeles Dodgers @ Toronto Blue Jays

**Fecha:** 2025-10-26  
**Lanzadores:** Yoshinobu Yamamoto (V) vs Kevin Gausman (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 48.8%

## 🔍 Explicación de los Cálculos

### Toronto Blue Jays (Local)
- **Estadística base YRFI:** 29.6% (24/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Yoshinobu Yamamoto):** 27.8% (5/18 partidos)
- **Puntuación ajustada:** 27.9%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 29.6% (24/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Toronto Blue Jays - Kevin Gausman):** 37.5% (6/16 partidos)
- **Puntuación ajustada:** 28.9%

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

- **Generado el:** 2025-10-25 09:37:13
- **Fuente de datos:** season_data.json
