# Análisis YRFI: San Diego Padres @ New York Mets

**Fecha:** 2025-09-17  
**Lanzadores:** Nick Pivetta (V) vs David Peterson (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 41.9%

## 🔍 Explicación de los Cálculos

### New York Mets (Local)
- **Estadística base YRFI:** 35.5% (27/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (San Diego Padres - Nick Pivetta):** 15.4% (2/13 partidos)
- **Puntuación ajustada:** 25.3%

### San Diego Padres (Visitante)
- **Estadística base YRFI:** 26.3% (20/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador local (New York Mets - David Peterson):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 22.2%

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
