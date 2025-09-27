# Análisis YRFI: New York Mets @ Miami Marlins

**Fecha:** 2025-09-27  
**Lanzadores:** Clay Holmes (V) vs Eury Pérez (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 47.3%

## 🔍 Explicación de los Cálculos

### Miami Marlins (Local)
- **Estadística base YRFI:** 29.1% (23/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador visitante (New York Mets - Clay Holmes):** 20.0% (3/15 partidos)
- **Puntuación ajustada:** 22.7%

### New York Mets (Visitante)
- **Estadística base YRFI:** 26.6% (21/79 partidos)
- **Tendencia reciente (últimos 15 partidos):** 53.3% (8/15 partidos)
- **Impacto del lanzador local (Miami Marlins - Eury Pérez):** 14.3% (1/7 partidos)
- **Puntuación ajustada:** 31.8%

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
