# Análisis YRFI: San Francisco Giants @ Arizona Diamondbacks

**Fecha:** 2025-09-17  
**Lanzadores:** Justin Verlander (V) vs Brandon Pfaadt (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 61.1%

## 🔍 Explicación de los Cálculos

### Arizona Diamondbacks (Local)
- **Estadística base YRFI:** 45.9% (34/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (San Francisco Giants - Justin Verlander):** 27.3% (3/11 partidos)
- **Puntuación ajustada:** 37.3%

### San Francisco Giants (Visitante)
- **Estadística base YRFI:** 32.9% (25/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (Arizona Diamondbacks - Brandon Pfaadt):** 26.7% (4/15 partidos)
- **Puntuación ajustada:** 38.0%

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

- **Generado el:** 2025-09-17 09:39:33
- **Fuente de datos:** season_data.json
