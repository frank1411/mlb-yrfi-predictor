# Análisis YRFI: Los Angeles Dodgers @ Philadelphia Phillies

**Fecha:** 2025-10-06  
**Lanzadores:** Blake Snell (V) vs Jesús Luzardo (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 58.2%

## 🔍 Explicación de los Cálculos

### Philadelphia Phillies (Local)
- **Estadística base YRFI:** 40.7% (33/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Blake Snell):** 50.0% (2/4 partidos)
- **Puntuación ajustada:** 46.1%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 29.6% (24/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Philadelphia Phillies - Jesús Luzardo):** 18.8% (3/16 partidos)
- **Puntuación ajustada:** 22.4%

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

- **Generado el:** 2025-10-06 09:41:45
- **Fuente de datos:** season_data.json
