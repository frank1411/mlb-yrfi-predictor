# Análisis YRFI: Cincinnati Reds @ St. Louis Cardinals

**Fecha:** 2025-09-16  
**Lanzadores:** Andrew Abbott (V) vs Michael McGreevy (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 46.3%

## 🔍 Explicación de los Cálculos

### St. Louis Cardinals (Local)
- **Estadística base YRFI:** 19.7% (15/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Cincinnati Reds - Andrew Abbott):** 18.2% (2/11 partidos)
- **Puntuación ajustada:** 19.3%

### Cincinnati Reds (Visitante)
- **Estadística base YRFI:** 22.4% (17/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (St. Louis Cardinals - Michael McGreevy):** 42.9% (3/7 partidos)
- **Puntuación ajustada:** 33.5%

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

- **Generado el:** 2025-09-16 09:40:57
- **Fuente de datos:** season_data.json
