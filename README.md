# ENA: Interfaz cerebro-máquina sin cirugía

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19372267.svg)](https://doi.org/10.5281/zenodo.19372267)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![EN](https://img.shields.io/badge/English-version-blue.svg)](./README.en.md)

Las interfaces cerebro-máquina más famosas requieren cirugía. Implantes, electrodos en el cerebro, riesgos de infección, rechazo y procedimientos costosos. Eso las limita a laboratorios o casos extremos.

**ENA nace para cambiar eso.**

## Que es

ENA (Electro Neural Adapter) es una interfaz cerebro-máquina no invasiva, modular y de código abierto. Se coloca detrás de la oreja (región retroauricular) y opera sin cirugía, mediante electrodos secos que leen señales EEG y estimulación tACS para enviar sensaciones.

## Que hace

- **Lee señales del cerebro**: 8–16 canales EEG capturan la actividad neuronal desde la superficie del cuero cabelludo.
- **Escribe sensaciones**: estimulación tACS (0–250 Hz, hasta 2 mA) permite enviar tacto, presión o temperatura al usuario.
- **Detecta movimiento**: IMU (acelerómetro + giroscopio) para interpretar intención motora.
- **Conecta sin cables**: Bluetooth 5.2, Wi-Fi y USB-C para comunicarse con prótesis, CORPUS u otros dispositivos.
- **Funciona todo el día**: batería recargable con 8–12 horas de uso continuo.

Todo en un dispositivo de menos de 50 gramos.

## Para quién es

- **Personas con prótesis**: pueden sentir lo que tocan y controlar la mano robótica con el pensamiento.
- **Usuarios de CORPUS**: pueden operar el cuerpo artificial a distancia y recibir retroalimentación sensorial.
- **Rehabilitación neurológica**: estimulación para pacientes con daño motor.
- **Investigación en interfaces cerebro-máquina**: plataforma abierta para desarrollar nuevas aplicaciones.

## Ventajas principales

- **Sin cirugía**: se coloca como un audífono, sin riesgos ni procedimientos invasivos.
- **Bidireccional**: no solo lee el cerebro, también escribe sensaciones.
- **Ligero y portátil**: menos de 50 gramos, 8–12 horas de batería.
- **Integrado con CORPUS**: permite que un humano controle el cuerpo artificial y sienta lo que él siente.

## Estado actual

- Concepto definido
- Arquitectura documentada
- 8–16 canales EEG, estimulación tACS, IMU
- Comunicación Bluetooth 5.2, Wi-Fi, USB-C
- Batería recargable (8–12 horas)
- Peso menor a 50 gramos
- Prototipo (pendiente)
- Validación clínica (pendiente)

  ## Documentación adicional

- **[Control de drones con ENA](docs/drones.md)**: caso de uso conceptual para operar drones (o enjambres) mediante señales cerebrales, sin joystick.

## Proyectos relacionados

- CORPUS — sistema corporal artificial
- Quantum-Flux — comunicaciones resilientes
- ShieldAir — torres de producción de oxígeno
- Motor de Oxígeno — propulsión limpia

## Licencia

Copyright © 2026 Enrique Aguayo. Todos los derechos reservados.

Este proyecto está protegido por derechos de autor.

PERMITIDO:
- Uso no comercial con fines educativos o de investigación.
- Distribución sin modificación, siempre que se mantenga esta licencia y se dé crédito al autor.

PROHIBIDO sin autorización expresa por escrito:
- Uso comercial (incluyendo, pero no limitado a: ofrecerlo como servicio, SaaS, suscripción, integración en productos que generen ingresos, o cualquier uso que genere beneficio económico directo o indirecto).
- Modificación para entornos de producción.
- Distribución de versiones modificadas sin autorización.

Para licencias comerciales, soporte técnico, pilotos empresariales o consultas:
Contacto: eaguayo@migst.cl

Cualquier uso fuera de los términos permitidos requiere permiso previo del autor.

Las consultas comerciales son bienvenidas y se responderán en un plazo máximo de 7 días hábiles.

## Autor

Enrique Aguayo H.
Mackiber Labs
Contacto: eaguayo@migst.cl
ORCID: 0009-0004-4615-6825
GitHub: @enriqueherbertag-lgtm

Documentación asistida por Ana (DeepSeek), IA para investigación y optimización técnica.
