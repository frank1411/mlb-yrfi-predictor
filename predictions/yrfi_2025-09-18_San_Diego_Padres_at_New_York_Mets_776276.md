# Análisis YRFI: San Diego Padres @ New York Mets

**Fecha:** 2025-09-18  
**Lanzadores:** Randy Vásquez (V) vs Jonah Tong (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 57.0%

## 🔍 Explicación de los Cálculos

### New York Mets (Local)
- **Estadística base YRFI:** 36.4% (28/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (San Diego Padres - Randy Vásquez):** 25.0% (3/12 partidos)
- **Puntuación ajustada:** 31.3%

### San Diego Padres (Visitante)
- **Estadística base YRFI:** 27.3% (21/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (New York Mets - Jonah Tong):** 50.0% (1/2 partidos)
- **Puntuación ajustada:** 37.4%

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

- **Generado el:** 2025-09-18 09:39:37
- **Fuente de datos:** season_data.json
