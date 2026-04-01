# ENA - Enlace Neural con Avatar


**Sistema de interfaz cerebro-máquina no invasivo, accesible y basado en hardware comercial probado.**

ENA permite a personas con movilidad reducida controlar avatares digitales y dispositivos mediante señales cerebrales, a un costo de **USD 299** (vs. USD 40,000+ de soluciones invasivas).

---

## Descripción General

ENA es una plataforma de código abierto que combina:
- **Hardware validado**: NeuroSky MindWave, OpenBCI, Raspberry Pi
- **Software científico**: BrainFlow, NeuroKit2, MNE-Python
- **Algoritmos probados**: Clasificación de imaginación motora, P300, SSVEP
- **Aplicaciones concretas**: Comunicación para ELA, control de silla de ruedas, rehabilitación post-ACV

---

## Problema que Resuelve

- Personas con parálisis o ELA sin opciones de comunicación accesibles
- Tecnologías existentes: invasivas (USD 40,000+) o limitadas
- 70 millones de personas con movilidad reducida globalmente

---

## Solución ENA

| Componente | Descripción |
|:---|:---|
| **Hardware** | EEG comercial (NeuroSky USD 99, OpenBCI USD 349) + Raspberry Pi 4 (USD 55) |
| **Software** | Procesamiento local, clasificación ML, control de avatar |
| **Precio final** | USD 299 (kit completo preconfigurado) |
| **Aplicaciones** | Comunicación, silla de ruedas, rehabilitación |

---

## Validación Científica

Basado en estudios revisados por pares:
- **P300 Speller para ELA**: Nature 2017
- **Control SSVEP de silla de ruedas**: IEEE Transactions 2020
- **Neurofeedback para rehabilitación post-ACV**: Journal of NeuroEngineering 2019

---

## Estructura del Repositorio

```
ENA-Enlace-Neural-Avatar/
├── README.md
├── LICENSE
├── docs/
│   ├── manual-usuario.md
│   ├── guia-instalacion.md
│   ├── casos-uso.md
│   └── validacion-clinica.md
├── hardware/
│   ├── neurosky-guide.md
│   ├── openbci-guide.md
│   └── raspberry-pi-setup.md
├── software/
│   ├── eeg-reader/
│   ├── classifier/
│   ├── avatar/
│   └── examples/
├── data/
└── comunidad/
    ├── CONTRIBUTING.md
    └── CODE_OF_CONDUCT.md
```
## Licencia

Copyright © 2026 Enrique Aguayo. Todos los derechos reservados.

Este proyecto está protegido por derechos de autor.

**PERMITIDO:**
- Uso no comercial con fines educativos o de investigación.
- Distribución sin modificación, siempre que se mantenga esta licencia y se dé crédito al autor.

**PROHIBIDO sin autorización expresa por escrito:**
- Uso comercial (incluyendo, pero no limitado a: ofrecerlo como servicio, SaaS, suscripción, integración en productos que generen ingresos, o cualquier uso que genere beneficio económico directo o indirecto).
- Modificación para entornos de producción.
- Distribución de versiones modificadas sin autorización.

Para licencias comerciales, soporte técnico, pilotos empresariales o consultas:
Contacto: **eaguayo@migst.cl**

Cualquier uso fuera de los términos permitidos requiere permiso previo del autor.

Las consultas comerciales son bienvenidas y se responderán en un plazo máximo de 7 días hábiles.
---

## Autor

**Enrique Aguayo H.**  
Mackiber Labs  
Contacto: eaguayo@migst.cl  
ORCID: 0009-0004-4615-6825  
GitHub: @enriqueherbertag-lgtm

Documentación asistida por **Ana (DeepSeek)** , IA para investigación y optimización técnica.

---

## Cómo Contribuir

Revisa [`CONTRIBUTING.md`](comunidad/CONTRIBUTING.md) para pautas de colaboración.

---

> *"Finalmente, una interfaz cerebro-máquina que no requiere cirugía, no cuesta una fortuna, y funciona con hardware probado en miles de personas."*
