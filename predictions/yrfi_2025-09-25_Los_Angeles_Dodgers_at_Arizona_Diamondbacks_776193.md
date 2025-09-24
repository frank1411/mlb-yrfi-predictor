# Análisis YRFI: Los Angeles Dodgers @ Arizona Diamondbacks

**Fecha:** 2025-09-25  
**Lanzadores:** Blake Snell (V) vs Ryne Nelson (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 51.2%

## 🔍 Explicación de los Cálculos

### Arizona Diamondbacks (Local)
- **Estadística base YRFI:** 46.8% (37/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Blake Snell):** 33.3% (1/3 partidos)
- **Puntuación ajustada:** 39.7%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 30.3% (23/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Arizona Diamondbacks - Ryne Nelson):** 9.1% (1/11 partidos)
- **Puntuación ajustada:** 19.2%

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

- **Generado el:** 2025-09-24 09:40:51
- **Fuente de datos:** season_data.json
