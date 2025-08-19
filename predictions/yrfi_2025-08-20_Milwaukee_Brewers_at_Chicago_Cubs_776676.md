# Análisis YRFI: Milwaukee Brewers @ Chicago Cubs

**Fecha:** 2025-08-20  
**Lanzadores:** Brandon Woodruff (V) vs Jameson Taillon (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 32.7%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 29.0% (18/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (Milwaukee Brewers - Brandon Woodruff):** 0.0% (0/3 partidos)
- **Puntuación ajustada:** 13.3%

### Milwaukee Brewers (Visitante)
- **Estadística base YRFI:** 29.0% (18/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Jameson Taillon):** 12.5% (1/8 partidos)
- **Puntuación ajustada:** 22.4%

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

- **Generado el:** 2025-08-19 12:49:11
- **Fuente de datos:** season_data.json
