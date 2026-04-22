# Mejoras propuestas (no implementadas)

Este archivo contiene ideas y direcciones para futuras versiones de CORPUS y ENA, basadas en la experiencia práctica y en la evolución de la tecnología.

## ENA (interfaz cerebro-máquina)

### Protocolo de ambientación y control emocional

Los sistemas actuales de BCI (interfaz cerebro-computadora) ignoran el estado emocional y fisiológico del usuario. Proponemos una capa de preprocesamiento que:

1. **Ambientación:** Preparar el entorno (luz, sonido, temperatura) para inducir un estado emocional estable.
2. **Medición de estado:** Usar sensores de variabilidad cardíaca (HRV), conductancia de la piel y temperatura periférica para estimar el nivel de estrés o relajación.
3. **Calibración adaptativa:** El sistema ajusta sus parámetros según el estado del usuario. Si el usuario está estresado, la decodificación se vuelve más conservadora (o espera a que se relaje).
4. **Retroalimentación inmediata:** El usuario recibe información visual o háptica de la acción ejecutada, cerrando el bucle cerebro-máquina.

**Estado:** Propuesto, no implementado.

## CORPUS (cuerpo artificial)

### Inconsciente basado en tablas (no IA)

En lugar de ejecutar modelos de IA en el borde, el inconsciente de CORPUS puede funcionar como un **sistema experto basado en tablas**:

- **Motor:** SQLite con índices (búsqueda O(1)).
- **Generación de tablas:** Entrenamiento externo (simulación masiva, IA cuántica o red neuronal). El robot no aprende; ejecuta reglas precalculadas.
- **Actualización:** Se reemplaza el archivo `.db` (como un firmware).

**Ventajas:** Determinismo, bajo consumo, explicabilidad, fácil certificación.

**Estado:** Propuesto, no implementado.

### Reflejos de navegación avanzados

- **Detección de obstáculos con umbrales relativos:** No usar distancias fijas (ej. "30 cm"), sino recurrir a los sensores en tiempo real (`distancia < distancia_minima_operacional`).
- **Reposición de objetos:** Si el robot mueve una silla, ejecutar una rutina para devolverla a su lugar original.
- **Anticipación de eventos:** Usar visión y modelos precalculados para atrapar un objeto antes de que caiga.

**Estado:** Propuesto, no implementado.

### Seguridad vital (prioridad máxima)

El inconsciente debe monitorizar los signos vitales del paciente (a través de ENA) y, ante cualquier anomalía:

1. Detener todo movimiento.
2. Cortar la conexión neuronal (si estaba activa).
3. Transmitir alerta de emergencia por todos los canales disponibles.
4. Enviar posición y signos vitales a servicios de emergencia.

**Esta regla tiene prioridad sobre cualquier otra instrucción.**

**Estado:** Propuesto, no implementado.

---

## Nota

Estas mejoras no están implementadas en la versión actual de CORPUS o ENA. Se documentan como direcciones futuras y como registro de la evolución del pensamiento detrás del proyecto.
