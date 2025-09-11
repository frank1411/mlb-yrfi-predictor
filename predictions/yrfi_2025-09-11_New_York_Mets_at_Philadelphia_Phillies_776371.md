# Análisis YRFI: New York Mets @ Philadelphia Phillies

**Fecha:** 2025-09-11  
**Lanzadores:** David Peterson (V) vs Jesús Luzardo (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 45.7%

## 🔍 Explicación de los Cálculos

### Philadelphia Phillies (Local)
- **Estadística base YRFI:** 39.4% (28/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (New York Mets - David Peterson):** 15.4% (2/13 partidos)
- **Puntuación ajustada:** 28.8%

### New York Mets (Visitante)
- **Estadística base YRFI:** 23.0% (17/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Philadelphia Phillies - Jesús Luzardo):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 23.6%

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

- **Generado el:** 2025-09-11 09:38:55
- **Fuente de datos:** season_data.json
