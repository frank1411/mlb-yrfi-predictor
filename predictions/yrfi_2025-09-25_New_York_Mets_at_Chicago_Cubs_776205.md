# Análisis YRFI: New York Mets @ Chicago Cubs

**Fecha:** 2025-09-25  
**Lanzadores:** Jonah Tong (V) vs Matthew Boyd (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.5%

## 🔍 Explicación de los Cálculos

### Chicago Cubs (Local)
- **Estadística base YRFI:** 28.9% (22/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 33.3% (5/15 partidos)
- **Impacto del lanzador visitante (New York Mets - Jonah Tong):** 0.0% (0/1 partidos)
- **Puntuación ajustada:** 20.4%

### New York Mets (Visitante)
- **Estadística base YRFI:** 25.0% (19/76 partidos)
- **Tendencia reciente (últimos 15 partidos):** 40.0% (6/15 partidos)
- **Impacto del lanzador local (Chicago Cubs - Matthew Boyd):** 35.7% (5/14 partidos)
- **Puntuación ajustada:** 34.1%

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

- **Generado el:** 2025-09-24 09:40:51
- **Fuente de datos:** season_data.json
