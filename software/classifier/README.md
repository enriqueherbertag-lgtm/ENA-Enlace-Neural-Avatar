# Classifier - Modulo de Clasificacion de Senales EEG

Este modulo contiene los algoritmos de machine learning para traducir las senales EEG en comandos accionables (movimientos de avatar, seleccion de letras, etc.).

---

## 1. Tipos de Clasificadores Incluidos

| Clasificador | Aplicacion | Entrada | Salida |
|:---|:---|:---|:---|
| Motor Imagery | Imaginacion de movimiento | Potencia alpha/beta (C3, C4) | Izquierda / Derecha / Nada |
| P300 Detector | Seleccion de letras | Potenciales evocados (Fz, Cz, Pz) | Letra seleccionada |
| SSVEP Detector | Control por frecuencias | Frecuencia dominante (O1, O2) | Comando (Adelante, Atras, etc.) |
| Concentration Level | Neurofeedback basico | Potencia theta/alpha | Nivel de concentracion (0-100) |

---

## 2. Estructura del Modulo

```
software/classifier/
├── README.md                    # Este archivo
├── __init__.py                  # Inicializador del modulo
├── base_classifier.py           # Clase base abstracta
├── motor_imagery.py              # Clasificador para imaginacion motora
├── p300_detector.py              # Detector de potenciales P300
├── ssvep_detector.py             # Detector de frecuencias SSVEP
├── concentration.py              # Nivel de concentracion
├── train.py                      # Script para entrenar modelos
├── evaluate.py                    # Script para evaluar modelos
├── models/                        # Modelos entrenados (gitignored)
│   ├── mi_model.pkl
│   ├── p300_model.pkl
│   └── ssvep_model.pkl
└── data/                          # Datos de ejemplo (gitignored)
```

---

## 3. Instalacion de Dependencias

```bash
# Desde la raiz del proyecto
pip install -r requirements.txt

# O manualmente:
pip install numpy pandas scipy scikit-learn joblib
```

---

## 4. Uso Basico

### 4.1 Cargar un clasificador pre-entrenado

```python
from classifier.motor_imagery import MotorImageryClassifier

# Cargar modelo guardado
clf = MotorImageryClassifier.load_model("models/mi_model.pkl")

# Predecir a partir de caracteristicas extraidas
features = extractor.extract(eeg_segment)  # array de (n_features,)
prediction = clf.predict(features.reshape(1, -1))

print(f"Comando: {prediction[0]}")  # 'left', 'right', 'rest'
```

### 4.2 Entrenar un nuevo clasificador

```python
from classifier.motor_imagery import MotorImageryClassifier
import numpy as np

# Datos de ejemplo (caracteristicas, etiquetas)
X_train = np.load("data/X_train.npy")  # (n_samples, n_features)
y_train = np.load("data/y_train.npy")  # (n_samples,)

# Inicializar y entrenar
clf = MotorImageryClassifier()
clf.train(X_train, y_train)

# Guardar modelo
clf.save_model("models/mi_model_v2.pkl")

# Evaluar
accuracy = clf.evaluate(X_test, y_test)
print(f"Precision: {accuracy:.2f}")
```

---

## 5. Clasificadores Especificos

### 5.1 Motor Imagery (Imaginacion Motora)

**Descripcion:** Detecta si el usuario esta imaginando movimiento de mano izquierda o derecha.

**Caracteristicas utilizadas:**
- Potencia en banda mu (8-12 Hz) en C3 y C4
- Potencia en banda beta (13-30 Hz) en C3 y C4
- Relacion de potencia C3/C4
- Hjorth parameters

```python
from classifier.motor_imagery import MotorImageryClassifier

# Configuracion
clf = MotorImageryClassifier(
    classifier_type='random_forest',  # 'svm', 'lda', 'cnn'
    n_estimators=100,
    bands=['mu', 'beta'],
    channels=['C3', 'C4']
)

# Entrenar
clf.train(X_train, y_train)

# Prediccion en tiempo real
command = clf.predict(features)
if command == 'left':
    avatar.move_left()
elif command == 'right':
    avatar.move_right()
else:
    avatar.stop()
```

**Dataset recomendado:** BCI Competition IV, dataset 2a.

### 5.2 P300 Detector

**Descripcion:** Detecta potenciales P300 en respuesta a estimulos visuales (para teclado virtual).

**Caracteristicas utilizadas:**
- Amplitud promedio en ventana 250-450ms post-estimulo
- Pendiente de la senal
- Area bajo la curva
- Coherencia entre canales frontales

```python
from classifier.p300_detector import P300Detector

# Inicializar detector
detector = P300Detector(
    channels=['Fz', 'Cz', 'Pz'],
    window_ms=[250, 450],
    threshold=0.7
)

# En cada estimulo:
# Recibir segmento de EEG post-estimulo
is_p300 = detector.detect(eeg_segment)

if is_p300:
    # Seleccionar letra actual
    selected_letter = current_letter
```

**Dataset recomendado:** BCI Competition III, dataset II (P300 speller).

### 5.3 SSVEP Detector

**Descripcion:** Detecta la frecuencia de parpadeo que esta mirando el usuario (para control de silla de ruedas).

**Frecuencias tipicas:** 12, 15, 20, 30 Hz

```python
from classifier.ssvep_detector import SSVEPDetector

# Inicializar detector
detector = SSVEPDetector(
    channels=['O1', 'O2'],
    target_freqs=[12, 15, 20, 30],
    sampling_rate=250
)

# En cada ventana de analisis
dominant_freq = detector.detect_frequency(eeg_segment)

if dominant_freq == 12:
    wheelchair.forward()
elif dominant_freq == 15:
    wheelchair.backward()
elif dominant_freq == 20:
    wheelchair.left()
elif dominant_freq == 30:
    wheelchair.right()
```

**Dataset recomendado:** BCI Competition IV, dataset 1 (SSVEP).

### 5.4 Concentration Level (Neurofeedback)

**Descripcion:** Calcula un indice de concentracion basado en relacion theta/alpha.

```python
from classifier.concentration import ConcentrationLevel

# Inicializar
conc = ConcentrationLevel(
    channels=['Fp1', 'Fp2'],
    alpha_band=(8, 13),
    theta_band=(4, 8)
)

# Calcular nivel cada 2 segundos
level = conc.compute(eeg_segment)  # 0-100
print(f"Nivel de concentracion: {level}%")

# Usar para juego de neurofeedback
if level > 70:
    game.advance()
```

---

## 6. Entrenamiento de Modelos

### 6.1 Usando datasets publicos

```python
from classifier.train import train_motor_imagery

# Descargar dataset (BCI Competition IV)
# Estructura esperada: data/BCICIV_2a/

# Entrenar modelo
model = train_motor_imagery(
    data_path="data/BCICIV_2a/",
    subject=1,  # Usar sujeto 1
    save_path="models/mi_subject1.pkl"
)
```

### 6.2 Entrenamiento con datos propios

```python
from classifier.train import train_from_files

# Archivos con caracteristicas extraidas
X_train = np.load("my_data/X_train.npy")
y_train = np.load("my_data/y_train.npy")

# Entrenar
model = train_from_files(
    X_train, y_train,
    classifier_type='svm',
    save_path="models/my_model.pkl"
)
```

### 6.3 Script de entrenamiento desde linea de comandos

```bash
# Entrenar imaginacion motora con dataset publico
python software/classifier/train.py --type motor_imagery --dataset bci_iv_2a --subject 1

# Entrenar P300
python software/classifier/train.py --type p300 --dataset bci_iii_ii

# Entrenar SSVEP
python software/classifier/train.py --type ssvep --dataset bci_iv_1
```

---

## 7. Evaluacion de Modelos

```python
from classifier.evaluate import evaluate_model

# Evaluar modelo guardado en test set
metrics = evaluate_model(
    model_path="models/mi_model.pkl",
    test_data="data/X_test.npy",
    test_labels="data/y_test.npy"
)

print(f"Accuracy: {metrics['accuracy']:.2f}")
print(f"F1-score: {metrics['f1_score']:.2f}")
print(metrics['confusion_matrix'])
```

---

## 8. Integracion en Tiempo Real

```python
import time
from eeg_reader.neurosky_reader import NeuroSkyReader
from eeg_reader.feature_extractor import FeatureExtractor
from classifier.motor_imagery import MotorImageryClassifier

# Inicializar componentes
reader = NeuroSkyReader(mac_address="00:13:EF:XX:XX:XX")
extractor = FeatureExtractor()
clf = MotorImageryClassifier.load_model("models/mi_model.pkl")

# Conectar
reader.connect()

# Bucle de tiempo real
window_seconds = 2
overlap = 1.5  # Ventanas deslizantes

try:
    while True:
        # Leer ventana
        data = reader.read(duration_seconds=window_seconds)
        
        # Extraer caracteristicas
        features = extractor.extract(data)
        
        # Clasificar
        command = clf.predict(features.reshape(1, -1))[0]
        
        # Accion
        if command == 'left':
            print("← Moviendo a izquierda")
        elif command == 'right':
            print("→ Moviendo a derecha")
        else:
            print("▪ Reposo")
        
        # Esperar para siguiente ventana
        time.sleep(window_seconds - overlap)
        
except KeyboardInterrupt:
    reader.disconnect()
```

---

## 9. Referencias API

### 9.1 Clase BaseClassifier

| Metodo | Descripcion |
|:---|:---|
| `train(X, y)` | Entrena el modelo con datos |
| `predict(X)` | Predice etiquetas para nuevas muestras |
| `predict_proba(X)` | Probabilidades de cada clase |
| `save_model(path)` | Guarda modelo a archivo |
| `load_model(path)` | Carga modelo desde archivo |
| `evaluate(X, y)` | Evaluacion en test set |

### 9.2 Clases derivadas

| Clase | Metodos adicionales |
|:---|:---|
| MotorImageryClassifier | `get_dominant_channel()` |
| P300Detector | `set_threshold(t)`, `get_response_latency()` |
| SSVEPDetector | `get_frequency_spectrum()` |
| ConcentrationLevel | `get_history()`, `reset()` |

---

## 10. Troubleshooting

| Problema | Solucion |
|:---|:---|
| Baja precision | Aumentar datos de entrenamiento, probar otro clasificador |
| Overfitting | Reducir features, aumentar regularizacion |
| Latencia en prediccion | Reducir ventana de analisis, simplificar modelo |
| Modelo no carga | Verificar version de sklearn (`joblib` incompatibilidad) |
| Clases desbalanceadas | Usar `class_weight='balanced'` |

---

*Documento version 1.0 - 2026*
```
