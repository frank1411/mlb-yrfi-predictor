# Análisis YRFI: Cincinnati Reds @ San Diego Padres

**Fecha:** 2025-09-10  
**Lanzadores:** Zack Littell (V) vs Michael King (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 42.2%

## 🔍 Explicación de los Cálculos

### San Diego Padres (Local)
- **Estadística base YRFI:** 23.2% (16/69 partidos)
- **Tendencia reciente (últimos 15 partidos):** 13.3% (2/15 partidos)
- **Impacto del lanzador visitante (Cincinnati Reds - Zack Littell):** 26.7% (4/15 partidos)
- **Puntuación ajustada:** 20.9%

### Cincinnati Reds (Visitante)
- **Estadística base YRFI:** 21.4% (15/70 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador local (San Diego Padres - Michael King):** 25.0% (2/8 partidos)
- **Puntuación ajustada:** 26.9%

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

- **Generado el:** 2025-09-09 20:25:51
- **Fuente de datos:** season_data.json
