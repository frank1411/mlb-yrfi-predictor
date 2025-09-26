# Análisis YRFI: St. Louis Cardinals @ Chicago Cubs

**Fecha:** 2025-09-26  
**Lanzadores:** Miles Mikolas (V) vs Por anunciar (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 58.9%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 28.2% (22/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (St. Louis Cardinals - Miles Mikolas):** 33.3% (5/15 partidos)
- **Puntuación ajustada:** 31.8%

### St. Louis Cardinals (Visitante)
- **Estadística base YRFI:** 26.9% (21/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Por anunciar):** 50.0% (0/0 partidos)
- **Puntuación ajustada:** 39.7%

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

- **Generado el:** 2025-09-26 09:39:49
- **Fuente de datos:** season_data.json
