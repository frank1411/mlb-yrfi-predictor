# Análisis YRFI: St. Louis Cardinals @ San Francisco Giants

**Fecha:** 2025-09-23  
**Lanzadores:** Michael McGreevy (V) vs Justin Verlander (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.9%

## 🔍 Explicación de los Cálculos

### San Francisco Giants (Local)
- **Estadística base YRFI:** 32.0% (24/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (St. Louis Cardinals - Michael McGreevy):** 33.3% (2/6 partidos)
- **Puntuación ajustada:** 37.7%

### St. Louis Cardinals (Visitante)
- **Estadística base YRFI:** 26.7% (20/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (San Francisco Giants - Justin Verlander):** 13.3% (2/15 partidos)
- **Puntuación ajustada:** 24.4%

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

- **Generado el:** 2025-09-22 13:39:41
- **Fuente de datos:** season_data.json
