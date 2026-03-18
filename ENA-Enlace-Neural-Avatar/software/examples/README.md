# Ejemplos de Uso - ENA

Esta carpeta contiene ejemplos practicos de uso de los diferentes modulos de ENA, desde pruebas basicas hasta integraciones completas.

---

## 1. Estructura de Ejemplos

```
software/examples/
├── README.md                    # Este archivo
├── 01_basic_connection.py        # Conexion basica con NeuroSky
├── 02_basic_connection_openbci.py # Conexion basica con OpenBCI
├── 03_simulated_eeg.py           # Uso de datos simulados
├── 04_feature_extraction.py       # Extraccion de caracteristicas
├── 05_motor_imagery_classifier.py # Clasificador de imaginacion motora
├── 06_p300_detection.py           # Detector P300
├── 07_ssvep_detection.py          # Detector SSVEP
├── 08_concentration_level.py       # Nivel de concentracion
├── 09_avatar_control_simple.py    # Control de avatar 2D
├── 10_avatar_control_three.py     # Control de avatar Three.js
├── 11_complete_pipeline.py        # Pipeline completo (lectura + clasif + avatar)
├── 12_realtime_visualization.py   # Visualizacion en tiempo real
├── 13_data_recording.py           # Grabacion de datos para entrenamiento
└── 14_train_from_recorded.py      # Entrenamiento con datos grabados
```

---

## 2. Requisitos Previos

Antes de ejecutar los ejemplos, asegurar:

```bash
# Instalar dependencias generales
pip install -r ../../requirements.txt

# Para ejemplos con NeuroSky, tener el dispositivo encendido
# Para ejemplos con OpenBCI, tener la placa conectada
# Para ejemplos con avatar 3D, tener navegador web
```

---

## 3. Ejemplos Basicos

### 3.1 Conexion con NeuroSky

```bash
python 01_basic_connection.py
```

```python
# Contenido simplificado
from eeg_reader.neurosky_reader import NeuroSkyReader

# Reemplazar con la MAC de tu dispositivo
reader = NeuroSkyReader(mac_address="00:13:EF:XX:XX:XX")
reader.connect()
data = reader.read(duration_seconds=5)
print(f"Leidas {data.shape[1]} muestras")
reader.disconnect()
```

### 3.2 Conexion con OpenBCI

```bash
python 02_basic_connection_openbci.py
```

```python
from eeg_reader.openbci_reader import OpenBCIReader

reader = OpenBCIReader(port="/dev/ttyUSB0")
reader.connect()
data = reader.read(duration_seconds=5)
print(f"Leidas {data.shape[1]} muestras de {data.shape[0]} canales")
reader.disconnect()
```

### 3.3 Simulacion de EEG

```bash
python 03_simulated_eeg.py
```

```python
from eeg_reader.simulated_reader import SimulatedReader
import matplotlib.pyplot as plt

reader = SimulatedReader(n_channels=4, sampling_rate=250)
reader.connect()
data = reader.read(duration_seconds=10)

plt.plot(data[:, 0])  # Canal 1
plt.title("EEG Simulado - Canal 1")
plt.xlabel("Muestras")
plt.ylabel("Amplitud (uV)")
plt.show()
```

---

## 4. Extraccion y Clasificacion

### 4.1 Extraccion de caracteristicas

```bash
python 04_feature_extraction.py
```

```python
from eeg_reader.simulated_reader import SimulatedReader
from eeg_reader.feature_extractor import FeatureExtractor

# Generar datos
reader = SimulatedReader()
reader.connect()
data = reader.read(duration_seconds=5)

# Extraer caracteristicas
extractor = FeatureExtractor()
features = extractor.extract(data)

print(f"Caracteristicas extraidas: {features.shape}")
print(f"Nombres: {extractor.get_feature_names()}")
```

### 4.2 Clasificador de imaginacion motora

```bash
python 05_motor_imagery_classifier.py
```

```python
from classifier.motor_imagery import MotorImageryClassifier
import numpy as np

# Cargar datos de ejemplo (simulados)
X_train = np.random.randn(100, 64)  # 100 muestras, 64 features
y_train = np.random.randint(0, 3, 100)  # 3 clases: left, right, rest

# Entrenar
clf = MotorImageryClassifier()
clf.train(X_train, y_train)

# Probar
X_test = np.random.randn(10, 64)
predictions = clf.predict(X_test)
print(f"Predicciones: {predictions}")
```

### 4.3 Detector P300

```bash
python 06_p300_detection.py
```

```python
from classifier.p300_detector import P300Detector
import numpy as np

detector = P300Detector(threshold=0.7)

# Simular segmentos con y sin P300
for i in range(10):
    # Generar segmento simulado
    segment = np.random.randn(250)  # 1 segundo a 250 Hz
    
    # Añadir pico P300 en algunos
    if i % 3 == 0:
        segment[100:150] += 5  # Simular P300
    
    is_p300 = detector.detect(segment)
    print(f"Segmento {i}: {'P300 detectado' if is_p300 else 'No P300'}")
```

### 4.4 Detector SSVEP

```bash
python 07_ssvep_detection.py
```

```python
from classifier.ssvep_detector import SSVEPDetector
import numpy as np

detector = SSVEPDetector(target_freqs=[12, 15, 20, 30])

# Simular 5 segundos a 15 Hz
t = np.linspace(0, 5, 5*250)
signal = np.sin(2*np.pi*15*t) + 0.5*np.random.randn(len(t))

freq = detector.detect_frequency(signal)
print(f"Frecuencia detectada: {freq} Hz")
```

### 4.5 Nivel de concentracion

```bash
python 08_concentration_level.py
```

```python
from classifier.concentration import ConcentrationLevel
import numpy as np

conc = ConcentrationLevel()

# Simular 10 ventanas
for i in range(10):
    # Datos simulados: mas concentracion al final
    data = np.random.randn(500) + i * 0.2
    level = conc.compute(data)
    print(f"Ventana {i}: Nivel {level:.1f}%")
```

---

## 5. Control de Avatar

### 5.1 Avatar simple (2D)

```bash
python 09_avatar_control_simple.py
```

```python
from avatar.simple_avatar import SimpleAvatar
import time
import random

avatar = SimpleAvatar()
avatar.init_window()

commands = ['left', 'right', 'up', 'down', 'stop']

for _ in range(50):
    cmd = random.choice(commands)
    print(f"Comando: {cmd}")
    
    if cmd == 'left':
        avatar.move_left()
    elif cmd == 'right':
        avatar.move_right()
    elif cmd == 'up':
        avatar.move_forward()
    elif cmd == 'down':
        avatar.move_backward()
    else:
        avatar.stop()
    
    avatar.update()
    time.sleep(0.5)
```

### 5.2 Avatar Three.js (navegador)

```bash
python 10_avatar_control_three.py
```

```python
from avatar.three_avatar import ThreeAvatar
import time
import random

avatar = ThreeAvatar(port=8000)
avatar.start()  # Abre navegador

commands = ['wave', 'smile', 'walk', 'idle']

for _ in range(20):
    cmd = random.choice(commands)
    print(f"Enviando: {cmd}")
    avatar.send_command(cmd)
    time.sleep(2)
```

---

## 6. Pipeline Completo

### 6.1 Pipeline con simulador y avatar simple

```bash
python 11_complete_pipeline.py
```

```python
import time
from eeg_reader.simulated_reader import SimulatedReader
from eeg_reader.feature_extractor import FeatureExtractor
from classifier.motor_imagery import MotorImageryClassifier
from avatar.simple_avatar import SimpleAvatar

# Inicializar componentes
reader = SimulatedReader(n_channels=4)
extractor = FeatureExtractor()
clf = MotorImageryClassifier()
avatar = SimpleAvatar()

# Simular entrenamiento (en realidad usariamos datos reales)
X_dummy = np.random.randn(100, 64)
y_dummy = np.random.randint(0, 3, 100)
clf.train(X_dummy, y_dummy)

# Conectar
reader.connect()
avatar.init_window()

# Bucle
try:
    for _ in range(30):
        data = reader.read(duration_seconds=2)
        features = extractor.extract(data)
        command = clf.predict(features.reshape(1, -1))[0]
        
        if command == 0:
            avatar.move_left()
        elif command == 1:
            avatar.move_right()
        elif command == 2:
            avatar.move_forward()
        else:
            avatar.stop()
        
        avatar.update()
        time.sleep(0.1)
        
finally:
    reader.disconnect()
```

---

## 7. Visualizacion y Grabacion

### 7.1 Visualizacion en tiempo real

```bash
python 12_realtime_visualization.py
```

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from eeg_reader.simulated_reader import SimulatedReader

reader = SimulatedReader()
reader.connect()

fig, axes = plt.subplots(4, 1, figsize=(10, 8))
lines = [ax.plot([], [])[0] for ax in axes]

def animate(i):
    data = reader.read(duration_seconds=0.5)
    for ch in range(min(4, data.shape[0])):
        lines[ch].set_data(range(len(data[ch])), data[ch])
        axes[ch].relim()
        axes[ch].autoscale_view()
    return lines

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
```

### 7.2 Grabacion de datos para entrenamiento

```bash
python 13_data_recording.py
```

```python
from eeg_reader.neurosky_reader import NeuroSkyReader
import numpy as np
import time

reader = NeuroSkyReader(mac_address="00:13:EF:XX:XX:XX")
reader.connect()

print("Grabando 30 segundos de datos...")
data = reader.read(duration_seconds=30)

# Guardar
np.save("recorded_data.npy", data)
print(f"Datos guardados en recorded_data.npy, forma: {data.shape}")

# Guardar con etiquetas (para entrenamiento supervisado)
labels = []  # Aqui pondriamos las etiquetas reales
for i in range(15):  # 15 ventanas de 2 segundos
    segment = data[:, i*500:(i+1)*500]
    # En una aplicacion real, aqui se pide al usuario que indique la tarea
    label = input(f"Ventana {i}: que tarea realizabas? (L=izq, R=der, N=nada): ")
    labels.append(label)
    
np.save("recorded_labels.npy", labels)
```

### 7.3 Entrenamiento con datos grabados

```bash
python 14_train_from_recorded.py
```

```python
import numpy as np
from eeg_reader.feature_extractor import FeatureExtractor
from classifier.motor_imagery import MotorImageryClassifier

# Cargar datos grabados
data = np.load("recorded_data.npy")
labels = np.load("recorded_labels.npy")

# Extraer caracteristicas por ventana
extractor = FeatureExtractor()
features = []
for i in range(data.shape[1] // 500):  # Ventanas de 2 segundos
    segment = data[:, i*500:(i+1)*500]
    feat = extractor.extract(segment)
    features.append(feat)

X = np.array(features)
y = np.array([0 if l=='L' else 1 if l=='R' else 2 for l in labels])

# Dividir en train/test
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Entrenar
clf = MotorImageryClassifier()
clf.train(X_train, y_train)

# Evaluar
accuracy = clf.evaluate(X_test, y_test)
print(f"Precision en test: {accuracy:.2f}")

# Guardar modelo
clf.save_model("models/mi_from_recorded.pkl")
```

---

## 8. Ejecucion de Todos los Ejemplos

Para ejecutar todos los ejemplos en secuencia:

```bash
# Desde la carpeta examples
for script in [f for f in sorted(os.listdir('.')) if f.endswith('.py')]:
    print(f"\n--- Ejecutando {script} ---")
    os.system(f"python {script}")
```

---

## 9. Notas Importantes

- Los ejemplos con hardware real requieren los dispositivos conectados y configurados
- Los ejemplos con simulador no requieren hardware
- Algunos ejemplos abren ventanas graficas (tkinter, matplotlib)
- Los ejemplos con Three.js abren el navegador web
- Para detener la ejecucion, usar Ctrl+C

---

*Documento version 1.0 - 2026*
```
