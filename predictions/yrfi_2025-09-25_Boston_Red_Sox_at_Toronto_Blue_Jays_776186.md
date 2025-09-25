# Análisis YRFI: Boston Red Sox @ Toronto Blue Jays

**Fecha:** 2025-09-25  
**Lanzadores:** Brayan Bello (V) vs Louis Varland (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 42.8%

## 🔍 Explicación de los Cálculos

### Toronto Blue Jays (Local)
- **Estadística base YRFI:** 28.6% (22/77 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (Boston Red Sox - Brayan Bello):** 30.0% (3/10 partidos)
- **Puntuación ajustada:** 26.0%

### Boston Red Sox (Visitante)
- **Estadística base YRFI:** 28.7% (23/80 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Toronto Blue Jays - Louis Varland):** 0.0% (0/0 partidos)
- **Puntuación ajustada:** 22.7%

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

- **Generado el:** 2025-09-25 09:40:11
- **Fuente de datos:** season_data.json
