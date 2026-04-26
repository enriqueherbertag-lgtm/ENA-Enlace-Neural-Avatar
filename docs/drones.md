# ENA para control de drones: caso de uso conceptual

## El problema

Los drones actuales requieren control remoto (joystick, tablet) o IA autónoma con supervisión humana. La latencia entre la intención del operador y la acción del drone puede ser crítica en aplicaciones de rescate, inspección o defensa. Además, un operador solo puede controlar un drone a la vez.

## La solución con ENA

ENA permite que un operador humano controle uno o múltiples drones mediante **señales cerebrales (EEG)**, sin necesidad de joystick ni pantallas táctiles. La interfaz es no invasiva (casco de superficie) y bidireccional (puede recibir sensaciones del drone, como proximidad o batería baja).

## Ventajas

| Aspecto | Control tradicional | Con ENA |
|:---|:---|:---|
| **Latencia** | 200-500 ms (respuesta manual) | < 50 ms (intención directa) |
| **Número de operadores por drone** | 1:1 | 1:N (un operador controla un enjambre) |
| **Fatiga del operador** | Alta (uso prolongado de manos) | Baja (solo actividad mental) |
| **Precisión en maniobras críticas** | Depende de la habilidad motora | Depende de la intención (entrenable) |

## Arquitectura simplificada

1. El operador usa el casco **ENA** (16 canales EEG, procesamiento en borde).
2. La señal cerebral se procesa en tiempo real (`NeuralBypass` opcional) y se clasifica en comandos (arriba, abajo, giro, etc.).
3. El comando se transmite al drone por Bluetooth, LoRa o 4G/5G.
4. El drone ejecuta la acción y envía retroalimentación (vibración, sonido, o estimulación táctil) al casco **ENA**, cerrando el bucle.

## Estado del proyecto

Este caso de uso es **conceptual**. El hardware de ENA está definido, y el procesamiento de señales está documentado en `NeuralBypass`. Se requiere un prototipo de integración con un drone comercial (ej. DJI, ZenaDrone, o un drone de código abierto).

## Próximos pasos (para quien quiera desarrollarlo)

1. Integrar `ENA` con un drone de bajo costo (ej. Crazyflie o un cuadricóptero Arduino).
2. Entrenar un clasificador simple (LDA) con comandos básicos: izquierda, derecha, subir, bajar.
3. Validar latencia y precisión en un entorno controlado.

## Colaboración

Si eres un fabricante de drones, un laboratorio de robótica o un investigador en interfaces cerebro-máquina, y te interesa explorar este caso de uso, contacta al autor.

**Contacto:** eaguayo@migst.cl
