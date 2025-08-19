# Análisis YRFI: Baltimore Orioles @ Boston Red Sox

**Fecha:** 2025-08-19  
**Lanzadores:** Tomoyuki Sugano (V) vs Walker Buehler (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 53.9%

## 🔍 Explicación de los Cálculos

### Boston Red Sox (Local)
- **Estadística base YRFI:** 35.4% (23/65 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Baltimore Orioles - Tomoyuki Sugano):** 45.5% (5/11 partidos)
- **Puntuación ajustada:** 40.6%

### Baltimore Orioles (Visitante)
- **Estadística base YRFI:** 24.6% (16/65 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador local (Boston Red Sox - Walker Buehler):** 30.0% (3/10 partidos)
- **Puntuación ajustada:** 22.5%

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

- **Generado el:** 2025-08-19 12:49:11
- **Fuente de datos:** season_data.json
