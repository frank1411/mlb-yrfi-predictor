# Análisis YRFI: Los Angeles Dodgers @ Seattle Mariners

**Fecha:** 2025-09-28  
**Lanzadores:** Clayton Kershaw (V) vs Bryce Miller (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 46.2%

## 🔍 Explicación de los Cálculos

### Seattle Mariners (Local)
- **Estadística base YRFI:** 22.5% (18/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Clayton Kershaw):** 36.4% (4/11 partidos)
- **Puntuación ajustada:** 36.0%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 30.0% (24/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Seattle Mariners - Bryce Miller):** 0.0% (0/8 partidos)
- **Puntuación ajustada:** 15.9%

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

- **Generado el:** 2025-09-28 09:35:53
- **Fuente de datos:** season_data.json
