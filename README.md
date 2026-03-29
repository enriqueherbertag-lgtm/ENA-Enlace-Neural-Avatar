# ENA - Enlace Neural con Avatar

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

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

---

## Autor

**Enrique Aguayo H.**  
Investigador independiente, Mackiber Labs  
GitHub: [@enriqueherbertag-lgtm](https://github.com/enriqueherbertag-lgtm)  
Contacto: eaguayo@migst.cl  
ORCID: 0009-0004-4615-6825

---

## Cómo Contribuir

Revisa [`CONTRIBUTING.md`](comunidad/CONTRIBUTING.md) para pautas de colaboración.

---

> *"Finalmente, una interfaz cerebro-máquina que no requiere cirugía, no cuesta una fortuna, y funciona con hardware probado en miles de personas."*
