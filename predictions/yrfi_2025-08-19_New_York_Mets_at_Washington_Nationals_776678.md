# Análisis YRFI: New York Mets @ Washington Nationals

**Fecha:** 2025-08-19  
**Lanzadores:** David Peterson (V) vs Jake Irvin (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 59.7%

## 🔍 Explicación de los Cálculos

### Washington Nationals (Local)
- **Estadística base YRFI:** 30.6% (19/62 partidos)
- **Tendencia reciente (últimos 15 partidos):** 26.7% (4/15 partidos)
- **Impacto del lanzador visitante (New York Mets - David Peterson):** 20.0% (2/10 partidos)
- **Puntuación ajustada:** 25.5%

### New York Mets (Visitante)
- **Estadística base YRFI:** 23.7% (14/59 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador local (Washington Nationals - Jake Irvin):** 63.6% (7/11 partidos)
- **Puntuación ajustada:** 45.9%

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
