# Análisis YRFI: Los Angeles Dodgers @ San Francisco Giants

**Fecha:** 2025-09-14  
**Lanzadores:** Clayton Kershaw (V) vs Logan Webb (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 56.3%

## 🔍 Explicación de los Cálculos

### San Francisco Giants (Local)
- **Estadística base YRFI:** 31.5% (23/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 66.7% (10/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Clayton Kershaw):** 30.0% (3/10 partidos)
- **Puntuación ajustada:** 43.5%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 30.1% (22/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (San Francisco Giants - Logan Webb):** 18.8% (3/16 partidos)
- **Puntuación ajustada:** 22.5%

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

- **Generado el:** 2025-09-13 09:35:57
- **Fuente de datos:** season_data.json
