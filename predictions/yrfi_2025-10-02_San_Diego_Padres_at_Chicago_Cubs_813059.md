# Análisis YRFI: San Diego Padres @ Chicago Cubs

**Fecha:** 2025-10-02  
**Lanzadores:** Yu Darvish (V) vs Jameson Taillon (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 62.2%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 29.6% (24/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador visitante (San Diego Padres - Yu Darvish):** 57.1% (4/7 partidos)
- **Puntuación ajustada:** 43.0%

### San Diego Padres (Visitante)
- **Estadística base YRFI:** 25.9% (21/81 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Jameson Taillon):** 20.0% (2/10 partidos)
- **Puntuación ajustada:** 33.6%

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
