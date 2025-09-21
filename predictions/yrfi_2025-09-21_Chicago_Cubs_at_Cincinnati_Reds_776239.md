# Análisis YRFI: Chicago Cubs @ Cincinnati Reds

**Fecha:** 2025-09-21  
**Lanzadores:** Jameson Taillon (V) vs Andrew Abbott (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 44.2%

## 🔍 Explicación de los Cálculos

### Cincinnati Reds (Local)
- **Estadística base YRFI:** 40.3% (31/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Chicago Cubs - Jameson Taillon):** 16.7% (2/12 partidos)
- **Puntuación ajustada:** 27.1%

### Chicago Cubs (Visitante)
- **Estadística base YRFI:** 31.2% (25/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Cincinnati Reds - Andrew Abbott):** 6.7% (1/15 partidos)
- **Puntuación ajustada:** 23.4%

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
