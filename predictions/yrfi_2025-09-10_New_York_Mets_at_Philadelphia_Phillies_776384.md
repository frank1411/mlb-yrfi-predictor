# Análisis YRFI: New York Mets @ Philadelphia Phillies

**Fecha:** 2025-09-10  
**Lanzadores:** Clay Holmes (V) vs Cristopher Sánchez (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 45.8%

## 🔍 Explicación de los Cálculos

### Philadelphia Phillies (Local)
- **Estadística base YRFI:** 38.6% (27/70 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (New York Mets - Clay Holmes):** 14.3% (2/14 partidos)
- **Puntuación ajustada:** 28.2%

### New York Mets (Visitante)
- **Estadística base YRFI:** 23.3% (17/73 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (Philadelphia Phillies - Cristopher Sánchez):** 16.7% (2/12 partidos)
- **Puntuación ajustada:** 24.6%

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
