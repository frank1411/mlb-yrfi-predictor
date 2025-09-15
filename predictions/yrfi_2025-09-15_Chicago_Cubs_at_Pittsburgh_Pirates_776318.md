# Análisis YRFI: Chicago Cubs @ Pittsburgh Pirates

**Fecha:** 2025-09-15  
**Lanzadores:** Jameson Taillon (V) vs Braxton Ashcraft (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 42.4%

## 🔍 Explicación de los Cálculos

### Pittsburgh Pirates (Local)
- **Estadística base YRFI:** 29.3% (22/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Chicago Cubs - Jameson Taillon):** 18.2% (2/11 partidos)
- **Puntuación ajustada:** 29.2%

### Chicago Cubs (Visitante)
- **Estadística base YRFI:** 31.1% (23/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Pittsburgh Pirates - Braxton Ashcraft):** 0.0% (0/3 partidos)
- **Puntuación ajustada:** 18.6%

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

- **Generado el:** 2025-09-15 09:41:15
- **Fuente de datos:** season_data.json
