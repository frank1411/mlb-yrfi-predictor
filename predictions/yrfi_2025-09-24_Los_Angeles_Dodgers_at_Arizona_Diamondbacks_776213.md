# Análisis YRFI: Los Angeles Dodgers @ Arizona Diamondbacks

**Fecha:** 2025-09-24  
**Lanzadores:** Shohei Ohtani (V) vs Brandon Pfaadt (L)

## 📊 Probabilidad YRFI del Partido

**Probabilidad de que anoten en la primera entrada:** 52.2%

## 🔍 Explicación de los Cálculos

### Arizona Diamondbacks (Local)
- **Estadística base YRFI:** 47.4% (37/78 partidos)
- **Tendencia reciente (últimos 15 partidos):** 46.7% (7/15 partidos)
- **Impacto del lanzador visitante (Los Angeles Dodgers - Shohei Ohtani):** 16.7% (1/6 partidos)
- **Puntuación ajustada:** 36.4%

### Los Angeles Dodgers (Visitante)
- **Estadística base YRFI:** 30.7% (23/75 partidos)
- **Tendencia reciente (últimos 15 partidos):** 20.0% (3/15 partidos)
- **Impacto del lanzador local (Arizona Diamondbacks - Brandon Pfaadt):** 25.0% (4/16 partidos)
- **Puntuación ajustada:** 24.9%

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

- **Generado el:** 2025-09-23 09:40:26
- **Fuente de datos:** season_data.json
