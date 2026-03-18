# Guia de Uso: OpenBCI Cyton Board

Este documento explica como integrar el EEG OpenBCI Cyton Board con ENA.

---

## 1. Especificaciones Tecnicas

| Parametro | Valor |
|:---|:---|
| Modelo | Cyton Board (8 canales) |
| Canales | 8 (mas 3 acelerometros) |
| Frecuencia muestreo | 250 Hz (max 16 kHz con firmware modificado) |
| Resolucion | 24 bits |
| Conectividad | Bluetooth (USB dongle incluido) |
| Electrodos | Secos o humedos (incluye 10) |
| Bateria | 1000 mAh LiPo (8-10 horas) |
| Certificaciones | CE, RoHS, usado en 500+ laboratorios |
| Precio | USD 349 (kit basico) |

---

## 2. Componentes del Kit

- Placa Cyton principal
- Dongle USB Bluetooth
- Cable USB para carga
- 10 electrodos (secos y humedos)
- Bateria LiPo 1000 mAh
- Cinta/casco para sujetar electrodos

---

## 3. Conexion con Raspberry Pi

### 3.1 Hardware necesario

- OpenBCI Cyton Board (cargado)
- Dongle USB Bluetooth incluido
- Raspberry Pi 4
- Electrodos y cinta/casco

### 3.2 Instalacion de drivers en Raspberry Pi

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3-pip python3-dev git

# Instalar pySerial para comunicacion serie
pip3 install pyserial

# Instalar OpenBCI Python
pip3 install openbci-ganglion
```

### 3.3 Emparejar el dongle Bluetooth

```bash
# Conectar el dongle USB a la Raspberry Pi
lsusb  # Verificar que se detecta (debe aparecer Silicon Labs)

# El dongle ya viene emparejado de fabrica con la placa Cyton
# Solo asegurar que la placa este encendida (switch en ON)
```

---

## 4. Software de Lectura Basico

### 4.1 Script de prueba simple

Crea un archivo `test_openbci.py`:

```python
import time
from openbci_ganglion import OpenBCIGanglion

def test_openbci():
    """Prueba de conexion con OpenBCI Cyton"""
    
    # Inicializar placa (puerto depende del sistema)
    # En Linux, el dongle crea un puerto /dev/ttyUSB0
    board = OpenBCIGanglion(port='/dev/ttyUSB0')
    
    try:
        # Conectar
        board.connect()
        print("Conectado a OpenBCI Cyton")
        
        # Iniciar stream
        board.start_streaming()
        
        # Leer 100 muestras
        for i in range(100):
            sample = board.read_sample()
            if sample:
                print(f"Muestra {i}: canal 1 = {sample.channels[0]:.2f} uV")
            time.sleep(0.01)
        
        # Detener
        board.stop_streaming()
        board.disconnect()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_openbci()
```

### 4.2 Usando BrainFlow (recomendado para ENA)

```python
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

def test_openbci_brainflow():
    """Prueba OpenBCI con BrainFlow (mas compatible con ENA)"""
    
    # Configurar parametros
    params = BrainFlowInputParams()
    params.serial_port = "/dev/ttyUSB0"  # Ajustar segun sistema
    
    # Inicializar board (OpenBCI Cyton = BoardIds.CYTON_BOARD)
    board_id = BoardIds.CYTON_BOARD.value
    board = BoardShim(board_id, params)
    
    try:
        # Preparar sesion
        board.prepare_session()
        print("Conectado a OpenBCI Cyton via BrainFlow")
        
        # Iniciar stream
        board.start_stream()
        time.sleep(5)  # Leer por 5 segundos
        
        # Obtener datos
        data = board.get_board_data()
        
        # Mostrar informacion
        print(f"Canales EEG: {BoardShim.get_eeg_channels(board_id)}")
        print(f"Muestras totales: {data.shape[1]}")
        print(f"Duracion: {data.shape[1] / BoardShim.get_sampling_rate(board_id):.2f} segundos")
        
        # Detener stream
        board.stop_stream()
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Liberar sesion
        board.release_session()

if __name__ == "__main__":
    test_openbci_brainflow()
```

---

## 5. Colocacion de Electrodos

### 5.1 Sistema 10-20 para 8 canales

Para ENA, se recomienda esta configuracion:

| Canal | Posicion | Area cerebral | Funcion |
|:---|:---|:---|:---|
| 1 | Fp1 | Prefrontal izquierdo | Concentracion, planificacion |
| 2 | Fp2 | Prefrontal derecho | Concentracion, emocion |
| 3 | C3 | Motor izquierdo | Imaginacion motora (derecha) |
| 4 | C4 | Motor derecho | Imaginacion motora (izquierda) |
| 5 | P3 | Parietal izquierdo | Procesamiento espacial |
| 6 | P4 | Parietal derecho | Procesamiento espacial |
| 7 | O1 | Visual izquierdo | Estimulos visuales (SSVEP) |
| 8 | O2 | Visual derecho | Estimulos visuales (SSVEP) |

### 5.2 Colocacion practica

```
      Fp1   Fp2
       |     |
       C3     C4
       |     |
       P3     P4
       |     |
       O1     O2
```

Referencia: electrodo en mastoides detras de oreja
Tierra: en el centro (Cz) o en la frente

---

## 6. Extraccion de Caracteristicas para 8 Canales

```python
import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def extract_features_openbci(eeg_data, sampling_rate=250):
    """Extrae caracteristicas de senales OpenBCI (8 canales)"""
    
    n_channels = eeg_data.shape[0]
    all_features = []
    
    # Bandas de frecuencia (Hz)
    bands = {
        'delta': (1, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30),
        'gamma': (30, 45)
    }
    
    # Para cada canal
    for channel in range(n_channels):
        channel_data = eeg_data[channel, :]
        channel_features = []
        
        # Potencia en cada banda
        for band_name, (low, high) in bands.items():
            power = DataFilter.get_band_power(channel_data, low, high, sampling_rate)
            channel_features.append(power)
        
        # Potencia total
        total_power = np.sum(channel_data ** 2)
        channel_features.append(total_power)
        
        # Estadisticas basicas
        channel_features.append(np.mean(channel_data))
        channel_features.append(np.std(channel_data))
        
        all_features.extend(channel_features)
    
    return np.array(all_features)
```

---

## 7. Modos Especificos con OpenBCI

### 7.1 Imaginacion Motora (C3, C4)

```python
# Usar canales 3 y 4 (C3, C4)
# Entrenar clasificador para izquierda/derecha
from sklearn.ensemble import RandomForestClassifier

# Caracteristicas: potencia alpha/beta en ambos canales
# Dataset: BCI Competition IV
```

### 7.2 SSVEP (O1, O2)

```python
# Usar canales 7 y 8 (O1, O2)
# Detectar frecuencia dominante mediante FFT
freqs = np.fft.rfftfreq(len(segment), 1/250)
fft_vals = np.abs(np.fft.rfft(segment))
dominant_freq = freqs[np.argmax(fft_vals[5:]) + 5]  # Ignorar frecuencias bajas
```

### 7.3 P300 (Fz, Cz, Pz)

```python
# Usar canales frontales y parietales
# Promediar ventanas post-estimulo
# Detectar pico positivo alrededor de 300ms
```

---

## 8. Problemas Comunes y Soluciones

| Problema | Causa posible | Solucion |
|:---|:---|:---|
| No se detecta placa | Dongle no conectado | Verificar USB, `lsusb` |
| | Placa apagada | Encender (switch en ON) |
| Conexion intermitente | Bateria baja | Cargar bateria |
| | Interferencias | Alejarse de WiFi, microondas |
| Ruido en senales | Mala conexion de electrodos | Limpiar piel, verificar contacto |
| | Electrodo suelto | Ajustar cinta/casco |
| Latencia alta | Buffer lleno | Aumentar tiempo de espera |
| | Sampling rate alto | Reducir a 250 Hz |

---

## 9. Referencias

- Documentacion oficial OpenBCI: https://docs.openbci.com/
- BrainFlow OpenBCI docs: https://brainflow.readthedocs.io/
- Foro OpenBCI: https://openbci.com/forum
- Repositorio ENA: https://github.com/enriqueherbertag-lgtm/ENA-Enlace-Neural-Avatar

---

*Documento version 1.0 - 2026*
```
