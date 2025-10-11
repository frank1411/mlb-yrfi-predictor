# Análisis YRFI: Chicago Cubs @ Milwaukee Brewers

**Fecha:** 2025-10-12  
**Lanzadores:** Drew Pomeranz (V) vs Trevor Megill (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 29.0%

## 🔍 Explicación de los Cálculos

### Milwaukee Brewers (Local)
- **Estadística base YRFI:** 17.3% (14/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador visitante (Chicago Cubs - Drew Pomeranz):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 7.4%

### Chicago Cubs (Visitante)
- **Estadística base YRFI:** 30.9% (25/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Milwaukee Brewers - Trevor Megill):** 0.0% (0/0 partidos)
- **Puntuación ajustada:** 23.3%

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

- **Generado el:** 2025-10-11 20:13:41
- **Fuente de datos:** season_data.json
