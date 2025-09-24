# Análisis YRFI: St. Louis Cardinals @ San Francisco Giants

**Fecha:** 2025-09-25  
**Lanzadores:** Sonny Gray (V) vs JT Brubaker (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.5%

## 🔍 Explicación de los Cálculos

### San Francisco Giants (Local)
- **Estadística base YRFI:** 32.5% (25/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (St. Louis Cardinals - Sonny Gray):** 36.4% (4/11 partidos)
- **Puntuación ajustada:** 38.9%

### St. Louis Cardinals (Visitante)
- **Estadística base YRFI:** 27.3% (21/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (San Francisco Giants - JT Brubaker):** 0.0% (0/0 partidos)
- **Puntuación ajustada:** 22.3%

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

- **Generado el:** 2025-09-24 09:40:52
- **Fuente de datos:** season_data.json
