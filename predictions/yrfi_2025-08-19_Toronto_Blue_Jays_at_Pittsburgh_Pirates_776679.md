# Análisis YRFI: Toronto Blue Jays @ Pittsburgh Pirates

**Fecha:** 2025-08-19  
**Lanzadores:** Max Scherzer (V) vs Mitch Keller (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 40.3%

## 🔍 Explicación de los Cálculos

### Pittsburgh Pirates (Local)
- **Estadística base YRFI:** 28.1% (18/64 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Toronto Blue Jays - Max Scherzer):** 25.0% (1/4 partidos)
- **Puntuación ajustada:** 26.5%

### Toronto Blue Jays (Visitante)
- **Estadística base YRFI:** 22.6% (14/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Pittsburgh Pirates - Mitch Keller):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 18.8%

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
