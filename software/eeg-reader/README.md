# EEG Reader - Modulo de Adquisicion de Senales

Este modulo se encarga de la lectura, filtrado y procesamiento inicial de las senales EEG provenientes de dispositivos compatibles.

---

## 1. Dispositivos Soportados

| Dispositivo | Canales | Modo | Libreria |
|:---|:---|:---|:---|
| NeuroSky MindWave 2 | 1 | Bajo costo | BrainFlow |
| OpenBCI Cyton | 8 | Investigacion | BrainFlow / OpenBCI |
| OpenBCI Ganglion | 4 | Portatil | BrainFlow / OpenBCI |
| Simulador | Variable | Desarrollo | numpy (senal simulada) |

---

## 2. Estructura del Modulo

```
software/eeg-reader/
├── README.md                    # Este archivo
├── __init__.py                  # Inicializador del modulo
├── reader_base.py                # Clase base para todos los readers
├── neurosky_reader.py            # Implementacion para NeuroSky
├── openbci_reader.py             # Implementacion para OpenBCI
├── simulated_reader.py           # Generador de senales simuladas (pruebas)
├── filters.py                    # Filtros digitales (Butterworth, etc.)
├── feature_extractor.py          # Extraccion de caracteristicas
├── test_connection.py            # Script para probar conexion
└── test_simulated.py             # Script para probar con datos simulados
```

---

## 3. Instalacion de Dependencias

```bash
# Desde la raiz del proyecto
pip install -r requirements.txt

# O manualmente:
pip install numpy pandas scipy brainflow openbci-ganglion
```

---

## 4. Uso Basico

### 4.1 Con NeuroSky

```python
from eeg_reader.neurosky_reader import NeuroSkyReader

# Inicializar reader con direccion MAC del NeuroSky
reader = NeuroSkyReader(mac_address="00:13:EF:XX:XX:XX")

# Conectar
reader.connect()

# Leer datos (5 segundos)
data = reader.read(duration_seconds=5)

# Desconectar
reader.disconnect()

# Los datos incluyen timestamps y valores EEG
print(f"Forma de los datos: {data.shape}")
print(f"Tasa de muestreo: {reader.sampling_rate} Hz")
```

### 4.2 Con OpenBCI

```python
from eeg_reader.openbci_reader import OpenBCIReader

# Inicializar reader con puerto serie
reader = OpenBCIReader(port="/dev/ttyUSB0")

# Conectar
reader.connect()

# Leer datos (5 segundos)
data = reader.read(duration_seconds=5)

# Desconectar
reader.disconnect()
```

### 4.3 Con Simulador (para pruebas)

```python
from eeg_reader.simulated_reader import SimulatedReader

# Inicializar reader con 8 canales simulados
reader = SimulatedReader(n_channels=8, sampling_rate=250)

# Conectar (siempre funciona)
reader.connect()

# Leer datos (10 segundos)
data = reader.read(duration_seconds=10)

# Desconectar
reader.disconnect()

# Visualizar
import matplotlib.pyplot as plt
plt.plot(data[:, 0])  # Canal 1
plt.show()
```

---

## 5. Clases Principales

### 5.1 ReaderBase (clase abstracta)

```python
class ReaderBase:
    """Clase base para todos los lectores EEG"""
    
    def __init__(self, sampling_rate=None):
        self.sampling_rate = sampling_rate
        self.connected = False
    
    def connect(self):
        """Conectar al dispositivo"""
        raise NotImplementedError
    
    def read(self, duration_seconds):
        """Leer datos por un tiempo especifico"""
        raise NotImplementedError
    
    def read_stream(self, callback, duration_seconds=None):
        """Leer en modo streaming con callback por cada muestra"""
        raise NotImplementedError
    
    def disconnect(self):
        """Desconectar dispositivo"""
        raise NotImplementedError
```

### 5.2 NeuroSkyReader

```python
class NeuroSkyReader(ReaderBase):
    """Lector para NeuroSky MindWave 2"""
    
    def __init__(self, mac_address):
        super().__init__(sampling_rate=512)
        self.mac_address = mac_address
        self.board = None
    
    def connect(self):
        # Implementacion usando BrainFlow
        pass
    
    def read(self, duration_seconds):
        # Retorna array numpy con canales x muestras
        pass
```

### 5.3 OpenBCIReader

```python
class OpenBCIReader(ReaderBase):
    """Lector para OpenBCI Cyton"""
    
    def __init__(self, port, n_channels=8):
        super().__init__(sampling_rate=250)
        self.port = port
        self.n_channels = n_channels
        self.board = None
    
    def connect(self):
        # Implementacion usando BrainFlow u openbci-ganglion
        pass
```

---

## 6. Procesamiento de Senales

### 6.1 Filtros (filters.py)

```python
from eeg_reader.filters import butter_bandpass, notch_filter

# Aplicar filtro pasa banda (1-45 Hz)
filtered = butter_bandpass(data, lowcut=1, highcut=45, fs=250)

# Aplicar filtro notch para eliminar 50/60 Hz
filtered = notch_filter(data, freq=50, fs=250)
```

### 6.2 Extraccion de Caracteristicas (feature_extractor.py)

```python
from eeg_reader.feature_extractor import FeatureExtractor

# Inicializar extractor con configuracion por defecto
extractor = FeatureExtractor()

# Extraer caracteristicas de una ventana de datos
features = extractor.extract(data_segment)

# Caracteristicas incluyen:
# - Potencia en bandas (delta, theta, alpha, beta, gamma)
# - Potencia total
# - Media, desviacion estandar
# - Cruces por cero
# - Hjorth parameters (movilidad, complejidad)
```

---

## 7. Scripts de Prueba

### 7.1 test_connection.py

```bash
python software/eeg-reader/test_connection.py --device neurosky --mac 00:13:EF:XX:XX:XX
```

Salida esperada:
```
Conectando a NeuroSky...
Conexion exitosa.
Tasa de muestreo: 512 Hz
Leyendo 5 segundos de datos...
Muestras obtenidas: 2560
Forma de datos: (1, 2560)
Media canal 1: 12.34 uV
Desconectado.
```

### 7.2 test_simulated.py

```bash
python software/eeg-reader/test_simulated.py --channels 8 --duration 10
```

Salida esperada:
```
Simulando 8 canales EEG por 10 segundos a 250 Hz...
Forma de datos: (8, 2500)
Graficando canales 0-3...
(Se abre ventana con graficos)
```

---

## 8. Integracion con Clasificador

```python
from eeg_reader.neurosky_reader import NeuroSkyReader
from eeg_reader.feature_extractor import FeatureExtractor
from software.classifier.motor_imagery import MotorImageryClassifier

# Inicializar componentes
reader = NeuroSkyReader(mac_address="00:13:EF:XX:XX:XX")
extractor = FeatureExtractor()
classifier = MotorImageryClassifier.load_model("models/mi_model.pkl")

# Conectar
reader.connect()

# Bucle de clasificacion en tiempo real
while True:
    # Leer ventana de 2 segundos
    data = reader.read(duration_seconds=2)
    
    # Extraer caracteristicas
    features = extractor.extract(data)
    
    # Clasificar
    prediction = classifier.predict(features.reshape(1, -1))
    
    # Mostrar resultado
    print(f"Comando detectado: {prediction}")
    
    # Pausa para siguiente ventana
    time.sleep(0.5)
```

---

## 9. Referencias API

### 9.1 Metodos principales de ReaderBase

| Metodo | Descripcion | Retorna |
|:---|:---|:---|
| `connect()` | Conecta al dispositivo | bool |
| `read(duration)` | Lee datos por duracion (seg) | numpy array |
| `read_stream(callback, duration)` | Streaming con callback | None |
| `get_sampling_rate()` | Tasa de muestreo actual | int |
| `get_channel_names()` | Nombres de canales | list |
| `disconnect()` | Desconecta | None |

### 9.2 Metodos de FeatureExtractor

| Metodo | Descripcion | Retorna |
|:---|:---|:---|
| `extract(data)` | Extrae caracteristicas | numpy array |
| `get_feature_names()` | Nombres de caracteristicas | list |
| `set_bands(bands_dict)` | Configura bandas de frecuencia | None |

---

## 10. Troubleshooting

| Problema | Solucion |
|:---|:---|
| BrainFlow no encuentra dispositivo | Verificar direccion MAC y Bluetooth activado |
| OpenBCI no conecta | Verificar puerto `/dev/ttyUSB0` y permisos |
| Datos muy ruidosos | Aplicar filtros pasa banda y notch |
| Latencia alta en streaming | Reducir tamano de buffer |
| Simulador no grafica | Instalar matplotlib: `pip install matplotlib` |

---

*Documento version 1.0 - 2026*
```
