# Análisis YRFI: Athletics @ Pittsburgh Pirates

**Fecha:** 2025-09-21  
**Lanzadores:** Mitch Spence (V) vs Mike Burrows (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 44.4%

## 🔍 Explicación de los Cálculos

### Pittsburgh Pirates (Local)
- **Estadística base YRFI:** 31.2% (25/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Athletics - Mitch Spence):** 0.0% (0/3 partidos)
- **Puntuación ajustada:** 23.4%

### Athletics (Visitante)
- **Estadística base YRFI:** 28.7% (23/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Pittsburgh Pirates - Mike Burrows):** 20.0% (2/10 partidos)
- **Puntuación ajustada:** 27.3%

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

- **Generado el:** 2025-09-21 09:36:24
- **Fuente de datos:** season_data.json
