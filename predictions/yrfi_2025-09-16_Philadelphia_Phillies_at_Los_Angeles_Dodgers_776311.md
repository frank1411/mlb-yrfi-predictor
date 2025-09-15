# Análisis YRFI: Philadelphia Phillies @ Los Angeles Dodgers

**Fecha:** 2025-09-16  
**Lanzadores:** Ranger Suárez (V) vs Emmet Sheehan (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 39.0%

## 🔍 Explicación de los Cálculos

### Los Angeles Dodgers (Local)
- **Estadística base YRFI:** 37.8% (28/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Philadelphia Phillies - Ranger Suárez):** 10.0% (1/10 partidos)
- **Puntuación ajustada:** 21.7%

### Philadelphia Phillies (Visitante)
- **Estadística base YRFI:** 26.7% (20/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Los Angeles Dodgers - Emmet Sheehan):** 0.0% (0/6 partidos)
- **Puntuación ajustada:** 22.1%

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

- **Generado el:** 2025-09-15 09:41:15
- **Fuente de datos:** season_data.json
