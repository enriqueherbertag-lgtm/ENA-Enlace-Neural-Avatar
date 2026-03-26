# Hardware de ENA

## Componentes Recomendados

### Opción Económica (USD 99–150)

| Componente | Modelo | Costo USD | Enlace / Notas |
|------------|--------|-----------|----------------|
| **EEG Headset** | NeuroSky MindWave Mobile 2 | 99 | Electrodos secos, 1 canal EEG (AF7), batería 8h |
| **Procesador** | Raspberry Pi 4 (4 GB) | 55 | Modelo recomendado: Raspberry Pi 4 Model B |
| **Total** | | **154** | |

### Opción Avanzada (USD 400–500)

| Componente | Modelo | Costo USD | Enlace / Notas |
|------------|--------|-----------|----------------|
| **EEG Board** | OpenBCI Ganglion | 349 | 4 canales EEG, electrodos húmedos, Bluetooth |
| **Electrodos** | OpenBCI Gold Cup Electrodes | 50 | 8 electrodos con pasta conductora |
| **Procesador** | Raspberry Pi 5 (8 GB) | 80 | Mayor capacidad de procesamiento |
| **Total** | | **479** | |

---

## Especificaciones Técnicas

### NeuroSky MindWave Mobile 2

| Parámetro | Valor |
|-----------|-------|
| Canales EEG | 1 (AF7) |
| Frecuencia de muestreo | 512 Hz |
| Resolución | 12 bits |
| Electrodos | Secos, sin pasta |
| Conexión | Bluetooth Class 2 |
| Batería | 8 horas continuas |
| Peso | 90 g |

### OpenBCI Ganglion

| Parámetro | Valor |
|-----------|-------|
| Canales EEG | 4 (configurables) |
| Frecuencia de muestreo | 250 Hz / canal |
| Resolución | 24 bits |
| Electrodos | Húmedos (con pasta conductora) |
| Conexión | Bluetooth 4.0 / USB |
| Batería | 24 horas |
| Peso | 120 g |

### Raspberry Pi 4 (Model B)

| Parámetro | Valor |
|-----------|-------|
| Procesador | ARM Cortex-A72, 1.5 GHz (4 núcleos) |
| RAM | 4 GB |
| Almacenamiento | MicroSD 32 GB (recomendado) |
| Puertos | 2× USB 3.0, 2× USB 2.0, Ethernet, HDMI |
| Consumo | 3–5 W |

---

## Configuración de Conexión

### NeuroSky + Raspberry Pi

```bash
# Instalar librería
pip install neurosky2
# Conectar por Bluetooth
bluetoothctl
scan on
pair [MAC_ADDRESS]
trust [MAC_ADDRESS]
connect [MAC_ADDRESS]
