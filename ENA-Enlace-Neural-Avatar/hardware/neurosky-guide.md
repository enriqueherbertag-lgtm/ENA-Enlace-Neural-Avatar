# Guia de Uso: NeuroSky MindWave Mobile 2

Este documento explica como integrar el EEG NeuroSky MindWave Mobile 2 con ENA.

---

## 1. Especificaciones Tecnicas

| Parametro | Valor |
|:---|:---|
| Modelo | MindWave Mobile 2 |
| Electrodos | 1 (frontal, Fp1) + referencia (oreja) |
| Frecuencia muestreo | 512 Hz |
| Bandas de frecuencia | Delta, Theta, Alpha, Beta, Gamma |
| Conectividad | Bluetooth 4.0 |
| Bateria | 8 horas continuas |
| Certificaciones | FDA-cleared (510(k) K101870), CE, FCC |
| Precio | USD 99 |

---

## 2. Conexion con Raspberry Pi

### 2.1 Hardware necesario
- NeuroSky MindWave Mobile 2
- Raspberry Pi 4 (cualquier modelo)
- Adaptador Bluetooth USB (si no tiene Bluetooth integrado)

### 2.2 Instalacion de drivers

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas Bluetooth
sudo apt install bluetooth bluez bluez-tools rfkill -y

# Habilitar Bluetooth
sudo rfkill unblock bluetooth

# Verificar dispositivos Bluetooth
bluetoothctl scan on
```

### 2.3 Emparejar NeuroSky

```bash
# Iniciar consola Bluetooth
bluetoothctl

# Encender el NeuroSky (presionar boton 2 segundos)
# Buscar dispositivo
scan on

# Ver direccion MAC del NeuroSky (ej: 00:13:EF:XX:XX:XX)
# Emparejar
pair XX:XX:XX:XX:XX:XX

# Conectar
connect XX:XX:XX:XX:XX:XX

# Confiar (para conexion automatica)
trust XX:XX:XX:XX:XX:XX

# Salir
exit
```

## 3. Software de Lectura

### 3.1 Instalar BrainFlow

```bash
# Instalar dependencias
pip install numpy pandas

# Instalar BrainFlow
pip install brainflow
```

### 3.2 Codigo basico de lectura

```python
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

def test_neurosky():
    """Prueba de conexion con NeuroSky"""
    
    # Configurar parametros
    params = BrainFlowInputParams()
    params.serial_port = "XX:XX:XX:XX:XX:XX"  # MAC del NeuroSky
    
    # Inicializar board
    board_id = BoardIds.NEUROSKY_BOARD
    board = BoardShim(board_id, params)
    
    try:
        # Preparar sesion
        board.prepare_session()
        print("Conectado a NeuroSky")
        
        # Iniciar stream
        board.start_stream()
        time.sleep(5)  # Leer por 5 segundos
        
        # Obtener datos
        data = board.get_board_data()
        
        # Mostrar estadisticas basicas
        print(f"Canales: {BoardShim.get_eeg_names(board_id)}")
        print(f"Muestras: {data.shape[1]}")
        
        # Detener stream
        board.stop_stream()
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Liberar sesion
        board.release_session()

if __name__ == "__main__":
    test_neurosky()
```

## 4. Extraccion de Caracteristicas

```python
import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def extract_features_from_neurosky(eeg_data, sampling_rate=512):
    """Extrae caracteristicas de la senal EEG"""
    
    features = []
    
    # Bandas de frecuencia (Hz)
    bands = {
        'delta': (1, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30),
        'gamma': (30, 45)
    }
    
    # Potencia en cada banda
    for band_name, (low, high) in bands.items():
        power = DataFilter.get_band_power(eeg_data, low, high, sampling_rate)
        features.append(power)
    
    # Potencia total
    total_power = np.sum(eeg_data ** 2)
    features.append(total_power)
    
    # Estadisticas basicas
    features.append(np.mean(eeg_data))
    features.append(np.std(eeg_data))
    
    return np.array(features)
```

## 5. Problemas Comunes y Soluciones

| Problema | Causa posible | Solucion |
|:---|:---|:---|
| No se detecta dispositivo | Bluetooth no activado | sudo rfkill unblock bluetooth |
| Conexion intermitente | Interferencias | Acercar dispositivos, alejar WiFi |
| Senal ruidosa | Mal contacto del electrodo | Limpiar frente con alcohol, ajustar posicion |
| Latencia alta | Buffer lleno | Reducir tiempo de buffer en codigo |

## 6. Referencias

- Documentacion oficial NeuroSky: https://store.neurosky.com/pages/mindwave
- BrainFlow NeuroSky docs: https://brainflow.readthedocs.io/en/stable/UserAPI.html#neurosky-board
- Foro de desarrolladores NeuroSky: https://developer.neurosky.com/
```
