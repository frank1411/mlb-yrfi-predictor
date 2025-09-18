# Análisis YRFI: Cleveland Guardians @ Detroit Tigers

**Fecha:** 2025-09-18  
**Lanzadores:** Tanner Bibee (V) vs Tarik Skubal (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 42.5%

## 🔍 Explicación de los Cálculos

### Detroit Tigers (Local)
- **Estadística base YRFI:** 31.2% (24/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Cleveland Guardians - Tanner Bibee):** 25.0% (4/16 partidos)
- **Puntuación ajustada:** 27.4%

### Cleveland Guardians (Visitante)
- **Estadística base YRFI:** 22.4% (17/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Detroit Tigers - Tarik Skubal):** 13.3% (2/15 partidos)
- **Puntuación ajustada:** 20.7%

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
