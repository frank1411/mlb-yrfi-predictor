# Análisis YRFI: Boston Red Sox @ New York Yankees

**Fecha:** 2025-10-03  
**Lanzadores:** Connelly Early (V) vs Cam Schlittler (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 66.5%

## 🔍 Explicación de los Cálculos

### New York Yankees (Local)
- **Estadística base YRFI:** 37.0% (30/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 60.0% (9/15 partidos)
- **Impacto del lanzador visitante (Boston Red Sox - Connelly Early):** 50.0% (1/2 partidos)
- **Puntuación ajustada:** 49.8%

### Boston Red Sox (Visitante)
- **Estadística base YRFI:** 28.4% (23/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (New York Yankees - Cam Schlittler):** 37.5% (3/8 partidos)
- **Puntuación ajustada:** 33.4%

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

- **Generado el:** 2025-10-02 09:38:48
- **Fuente de datos:** season_data.json
