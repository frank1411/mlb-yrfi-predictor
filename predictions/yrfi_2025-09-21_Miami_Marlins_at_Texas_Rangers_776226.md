# Análisis YRFI: Miami Marlins @ Texas Rangers

**Fecha:** 2025-09-21  
**Lanzadores:** Eury Pérez (V) vs Merrill Kelly (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 49.5%

## 🔍 Explicación de los Cálculos

### Texas Rangers (Local)
- **Estadística base YRFI:** 22.1% (17/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 6.7% (1/15 partidos)
- **Impacto del lanzador visitante (Miami Marlins - Eury Pérez):** 54.5% (6/11 partidos)
- **Puntuación ajustada:** 27.9%

### Miami Marlins (Visitante)
- **Estadística base YRFI:** 24.7% (19/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Texas Rangers - Merrill Kelly):** 37.5% (6/16 partidos)
- **Puntuación ajustada:** 29.9%

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
