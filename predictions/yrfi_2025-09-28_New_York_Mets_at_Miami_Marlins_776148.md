# Análisis YRFI: New York Mets @ Miami Marlins

**Fecha:** 2025-09-28  
**Lanzadores:** Sean Manaea (V) vs Edward Cabrera (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 60.4%

## 🔍 Explicación de los Cálculos

### Miami Marlins (Local)
- **Estadística base YRFI:** 28.7% (23/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (New York Mets - Sean Manaea):** 60.0% (3/5 partidos)
- **Puntuación ajustada:** 36.6%

### New York Mets (Visitante)
- **Estadística base YRFI:** 27.5% (22/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador local (Miami Marlins - Edward Cabrera):** 23.1% (3/13 partidos)
- **Puntuación ajustada:** 37.6%

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

- **Generado el:** 2025-09-28 09:35:53
- **Fuente de datos:** season_data.json
