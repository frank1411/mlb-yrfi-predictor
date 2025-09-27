# Análisis YRFI: St. Louis Cardinals @ Chicago Cubs

**Fecha:** 2025-09-27  
**Lanzadores:** Michael McGreevy (V) vs Jameson Taillon (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 54.7%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 29.1% (23/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (St. Louis Cardinals - Michael McGreevy):** 42.9% (3/7 partidos)
- **Puntuación ajustada:** 35.4%

### St. Louis Cardinals (Visitante)
- **Estadística base YRFI:** 26.6% (21/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Jameson Taillon):** 22.2% (2/9 partidos)
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

- **Generado el:** 2025-09-27 09:36:25
- **Fuente de datos:** season_data.json
