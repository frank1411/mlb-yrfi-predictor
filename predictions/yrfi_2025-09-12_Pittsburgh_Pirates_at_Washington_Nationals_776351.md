# Análisis YRFI: Pittsburgh Pirates @ Washington Nationals

**Fecha:** 2025-09-12  
**Lanzadores:** Mitch Keller (V) vs Brad Lord (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 49.7%

## 🔍 Explicación de los Cálculos

### Washington Nationals (Local)
- **Estadística base YRFI:** 29.6% (21/71 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (Pittsburgh Pirates - Mitch Keller):** 30.8% (4/13 partidos)
- **Puntuación ajustada:** 28.9%

### Pittsburgh Pirates (Visitante)
- **Estadística base YRFI:** 27.8% (20/72 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Washington Nationals - Brad Lord):** 12.5% (1/8 partidos)
- **Puntuación ajustada:** 29.2%

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

- **Generado el:** 2025-09-12 09:38:12
- **Fuente de datos:** season_data.json
