# Análisis YRFI: Miami Marlins @ Philadelphia Phillies

**Fecha:** 2025-09-23  
**Lanzadores:** Edward Cabrera (V) vs Cristopher Sánchez (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 61.5%

## 🔍 Explicación de los Cálculos

### Philadelphia Phillies (Local)
- **Estadística base YRFI:** 40.0% (30/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Miami Marlins - Edward Cabrera):** 63.6% (7/11 partidos)
- **Puntuación ajustada:** 50.7%

### Miami Marlins (Visitante)
- **Estadística base YRFI:** 24.4% (19/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Philadelphia Phillies - Cristopher Sánchez):** 15.4% (2/13 partidos)
- **Puntuación ajustada:** 22.0%

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

- **Generado el:** 2025-09-23 09:40:26
- **Fuente de datos:** season_data.json
