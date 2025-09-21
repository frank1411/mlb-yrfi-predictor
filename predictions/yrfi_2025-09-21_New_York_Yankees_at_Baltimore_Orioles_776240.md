# Análisis YRFI: New York Yankees @ Baltimore Orioles

**Fecha:** 2025-09-21  
**Lanzadores:** Cam Schlittler (V) vs Kyle Bradish (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 70.2%

## 🔍 Explicación de los Cálculos

### Baltimore Orioles (Local)
- **Estadística base YRFI:** 26.0% (20/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (New York Yankees - Cam Schlittler):** 60.0% (3/5 partidos)
- **Puntuación ajustada:** 38.1%

### New York Yankees (Visitante)
- **Estadística base YRFI:** 43.8% (35/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador local (Baltimore Orioles - Kyle Bradish):** 50.0% (1/2 partidos)
- **Puntuación ajustada:** 51.8%

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

- **Generado el:** 2025-09-21 09:36:24
- **Fuente de datos:** season_data.json
