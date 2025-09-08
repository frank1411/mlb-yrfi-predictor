# Análisis YRFI: New York Mets @ Philadelphia Phillies

**Fecha:** 2025-09-08  
**Lanzadores:** Nolan McLean (V) vs Aaron Nola (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 60.7%

## 🔍 Explicación de los Cálculos

### Philadelphia Phillies (Local)
- **Estadística base YRFI:** 38.2% (26/68 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (New York Mets - Nolan McLean):** 50.0% (1/2 partidos)
- **Puntuación ajustada:** 38.2%

### New York Mets (Visitante)
- **Estadística base YRFI:** 23.9% (17/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Philadelphia Phillies - Aaron Nola):** 50.0% (3/6 partidos)
- **Puntuación ajustada:** 36.4%

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

- **Generado el:** 2025-09-08 22:45:00
- **Fuente de datos:** season_data.json
