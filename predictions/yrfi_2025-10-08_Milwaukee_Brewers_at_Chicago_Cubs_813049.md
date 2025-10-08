# Análisis YRFI: Milwaukee Brewers @ Chicago Cubs

**Fecha:** 2025-10-08  
**Lanzadores:** Quinn Priester (V) vs Jameson Taillon (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 48.9%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 29.6% (24/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Milwaukee Brewers - Quinn Priester):** 42.9% (6/14 partidos)
- **Puntuación ajustada:** 38.0%

### Milwaukee Brewers (Visitante)
- **Estadística base YRFI:** 28.4% (23/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Jameson Taillon):** 20.0% (2/10 partidos)
- **Puntuación ajustada:** 17.7%

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
