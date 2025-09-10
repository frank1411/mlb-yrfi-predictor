# Análisis YRFI: Minnesota Twins @ Los Angeles Angels

**Fecha:** 2025-09-10  
**Lanzadores:** Taj Bradley (V) vs José Soriano (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 55.0%

## 🔍 Explicación de los Cálculos

### Los Angeles Angels (Local)
- **Estadística base YRFI:** 33.8% (25/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (Minnesota Twins - Taj Bradley):** 45.5% (5/11 partidos)
- **Puntuación ajustada:** 40.1%

### Minnesota Twins (Visitante)
- **Estadística base YRFI:** 28.4% (21/74 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Los Angeles Angels - José Soriano):** 20.0% (3/15 partidos)
- **Puntuación ajustada:** 24.8%

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

- **Generado el:** 2025-09-10 09:39:09
- **Fuente de datos:** season_data.json
