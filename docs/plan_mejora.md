# 📋 Plan de Mejora - MLB YRFI Predictor

*Última actualización: 26 de Junio 2025*

## 📌 Visión General

Este documento describe el plan estratégico para mejorar el proyecto MLB YRFI Predictor, un sistema de predicción de carreras en la primera entrada (YRFI - Yes Run First Inning) para partidos de béisbol de las Grandes Ligas.

## 🛣️ Ruta Óptima de Implementación

### Fase 1: Cimientos Sólidos (Semanas 1-2)
**Objetivo:** Establecer una base sólida para el desarrollo continuo

1. **Automatización Básica** (Alto Impacto/Bajo Esfuerzo)
   - [x] Configurar GitHub Actions para ejecución diaria
   - [x] Implementar sistema de logs básico
   - [x] Automatizar actualización de datos

2. **Dashboard Mínimo Viable (MVP)**
   - [x] Crear dashboard simple con Streamlit
   - [x] Mostrar predicciones del día
   - [ ] Incluir métricas básicas de precisión

### Fase 2: Mejora del Modelo (Semanas 3-5)
**Objetivo:** Incrementar la precisión de las predicciones

3. **Variables Clave**
   - [ ] Añadir datos meteorológicos básicos
   - [ ] Implementar ponderación ajustable de factores
   - [ ] Mejorar estadísticas de lanzadores

4. **Sistema de Retroalimentación**
   - [ ] Registrar resultados reales vs predicciones
   - [ ] Crear métricas de rendimiento
   - [ ] Implementar validación cruzada básica

### Fase 3: Escalabilidad (Semanas 6-9)
**Objetivo:** Preparar el sistema para crecimiento

5. **Infraestructura**
   - [ ] Migrar a base de datos SQL
   - [ ] Implementar sistema de caché
   - [ ] Optimizar consultas frecuentes

6. **API Básica**
   - [ ] Desarrollar endpoints esenciales
   - [ ] Documentación básica
   - [ ] Autenticación simple

### Fase 4: Refinamiento (Semanas 10+)
**Objetivo:** Mejora continua y optimización

7. **Mejoras Incrementales**
   - [ ] Modelos avanzados de ML
   - [ ] Dashboard avanzado
   - [ ] Sistema de notificaciones

## 🎯 Objetivos

1. Mejorar la precisión de las predicciones YRFI
2. Automatizar el flujo de trabajo
3. Mejorar la experiencia del usuario
4. Asegurar la escalabilidad del sistema
5. Mantener documentación actualizada

## 📊 1. Mejoras en el Modelo Predictivo

### 1.1 Variables Adicionales

- [ ] **Factores Meteorológicos**
  - Temperatura, humedad, dirección del viento
  - Condiciones del campo (cúpula/aire libre)
  - Presión atmosférica

- [ ] **Estadísticas Avanzadas de Lanzadores**
  - Rendimiento por entrada
  - Efectividad contra bateadores zurdos/diestros
  - Rendimiento en días de descanso específicos
  - Velocidad promedio de lanzamiento

- [ ] **Rendimiento Histórico del Equipo**
  - Rendimiento contra lanzadores similares
  - Rendimiento en días específicos de la semana
  - Efecto del jet lag en equipos viajeros

### 1.2 Mejoras en el Algoritmo

- [ ] Implementar modelos de machine learning (XGBoost, Random Forest)
- [ ] Añadir validación cruzada para evaluar el rendimiento
- [ ] Implementar un sistema de ponderación de factores ajustable
- [ ] Sistema de retroalimentación para mejorar predicciones

## 🏗️ 2. Mejoras en la Infraestructura

### 2.1 Automatización

- [ ] Configurar GitHub Actions para:
  - Ejecución diaria de predicciones
  - Notificaciones automáticas
  - Actualización de dashboard
  - Pruebas automáticas

### 2.2 Base de Datos

- [ ] Migrar a PostgreSQL/MySQL
- [ ] Implementar sistema de caché con Redis
- [ ] Programar respaldos automáticos
- [ ] Optimizar consultas frecuentes

## 🖥️ 3. Interfaz de Usuario

### 3.1 Dashboard Web

- [ ] Panel de control con:
  - Gráficos de tendencias YRFI
  - Historial de predicciones vs. resultados
  - Comparativas de rendimiento
  - Alertas personalizables

### 3.2 API REST

- [ ] Endpoints para:
  - Consulta de predicciones
  - Estadísticas históricas
  - Integración con otras aplicaciones
  - Autenticación segura

## 📈 4. Calidad de Datos

### 4.1 Limpieza y Validación

- [ ] Validación de datos de entrada
- [ ] Manejo de datos faltantes
- [ ] Sistema de logs detallado
- [ ] Monitoreo de calidad de datos

### 4.2 Fuentes Adicionales

- [ ] Múltiples fuentes para validación cruzada
- [ ] Datos de apuestas deportivas
- [ ] Estadísticas avanzadas de Fangraphs/Baseball-Reference

## 📚 5. Documentación

### 5.1 Técnica

- [ ] Arquitectura del sistema
- [ ] Guía de contribución
- [ ] Proceso de despliegue
- [ ] Estándares de código

### 5.2 Usuario

- [ ] Manual de usuario
- [ ] Guía de interpretación de métricas
- [ ] Preguntas frecuentes
- [ ] Tutoriales en video

## 🚀 6. Próximos Pasos

### Prioridad Alta (Sprint 1)

1. Implementar sistema de ponderación ajustable
2. Configurar GitHub Actions
3. Dashboard básico con Streamlit
4. Documentación inicial

### Prioridad Media (Sprint 2)

1. Añadir variables meteorológicas
2. Mejorar sistema de caché
3. Documentar código existente
4. Sistema de logs mejorado

### Prioridad Baja (Sprint 3+)

1. Desarrollar API REST
2. Implementar modelos de ML avanzados
3. Sistema de notificaciones
4. Documentación detallada

## 📊 7. Métricas de Éxito

| Métrica | Objetivo | Actual |
|---------|----------|---------|
| Precisión predicciones | > 60% | Por definir |
| Tiempo generación | < 5 min | Por medir |
| Disponibilidad | > 99.5% | Por medir |
| Reducción llamadas API | 30% | Por medir |
| Satisfacción usuario | > 4.5/5 | Por medir |

## 👥 Responsables

- **Equipo de Desarrollo**: Implementación técnica
- **Ciencia de Datos**: Mejora de modelos
- **DevOps**: Infraestructura y despliegue
- **UX/UI**: Experiencia de usuario

## 📅 Cronograma Tentativo

- **Sprint 1 (2 semanas)**: Prioridades altas
- **Sprint 2 (3 semanas)**: Prioridades medias
- **Sprint 3+ (4 semanas)**: Prioridades bajas y refinamiento

## 🔄 Revisión y Ajustes

Este documento se revisará y actualizará al final de cada sprint para reflejar:
- Progreso realizado
- Cambios en prioridades
- Nuevas oportunidades identificadas
- Lecciones aprendidas

---

*Documento creado el 26 de Junio 2025*
*Próxima revisión programada: 10 de Julio 2025*
