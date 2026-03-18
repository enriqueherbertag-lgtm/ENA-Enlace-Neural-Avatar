# Datos para ENA - Enlace Neural con Avatar

Esta carpeta contiene referencias a datasets publicos, datos de ejemplo y scripts para descargar y preparar datos para entrenamiento y validacion.

---

## 1. Estructura de la Carpeta

```
data/
├── README.md                    # Este archivo
├── download_scripts/             # Scripts para descargar datasets
│   ├── download_bci_iv_2a.py
│   ├── download_physionet_mmi.py
│   ├── download_openbmi.py
│   └── download_all.py
├── sample_data/                   # Datos de ejemplo (pequenos)
│   ├── sample_eeg.npy
│   ├── sample_labels.npy
│   └── sample_features.npy
├── processed/                      # Datos procesados (gitignored)
│   └── README.md
└── references/                     # Referencias a papers
    └── README.md
```

**Nota:** Los archivos de datos grandes no se incluyen en el repositorio. Se deben descargar por separado usando los scripts proporcionados.

---

## 2. Datasets Publicos Recomendados

### 2.1 BCI Competition IV - Dataset 2a

| Detalle | Descripcion |
|:---|:---|
| **Descripcion** | Imaginacion motora de 4 clases (mano izquierda, derecha, pies, lengua) |
| **Sujetos** | 9 |
| **Canales** | 22 EEG + 3 EOG |
| **Frecuencia** | 250 Hz |
| **Enlace** | http://www.bbci.de/competition/iv/ |
| **Uso en ENA** | Entrenamiento de clasificadores de imaginacion motora |

### 2.2 BCI Competition III - Dataset II (P300 Speller)

| Detalle | Descripcion |
|:---|:---|
| **Descripcion** | Potenciales P300 para deletreo |
| **Sujetos** | 2 |
| **Canales** | 64 |
| **Frecuencia** | 240 Hz |
| **Enlace** | http://www.bbci.de/competition/iii/ |
| **Uso en ENA** | Desarrollo del modo comunicacion (teclado virtual) |

### 2.3 BCI Competition IV - Dataset 1 (SSVEP)

| Detalle | Descripcion |
|:---|:---|
| **Descripcion** | Potenciales SSVEP a diferentes frecuencias |
| **Sujetos** | 10 |
| **Canales** | 8 |
| **Frecuencia** | 1000 Hz |
| **Enlace** | http://www.bbci.de/competition/iv/ |
| **Uso en ENA** | Control de silla de ruedas por frecuencias |

### 2.4 PhysioNet EEG Motor Movement/Imagery

| Detalle | Descripcion |
|:---|:---|
| **Descripcion** | Movimientos reales e imaginados |
| **Sujetos** | 109 |
| **Canales** | 64 |
| **Frecuencia** | 160 Hz |
| **Enlace** | https://physionet.org/content/eegmmidb/ |
| **Uso en ENA** | Entrenamiento con gran cantidad de sujetos |

### 2.5 OpenBMI Dataset

| Detalle | Descripcion |
|:---|:---|
| **Descripcion** | 54 sujetos, multiples tareas |
| **Sujetos** | 54 |
| **Canales** | 62 |
| **Frecuencia** | 1000 Hz |
| **Enlace** | http://openbmi.org/ |
| **Uso en ENA** | Validacion cruzada, generalizacion |

---

## 3. Scripts de Descarga

### 3.1 Descargar BCI Competition IV

```bash
cd data/download_scripts
python download_bci_iv_2a.py
```

Contenido del script (simplificado):

```python
import os
import urllib.request
import zipfile

def download_bci_iv_2a():
    """Descarga dataset BCI Competition IV 2a"""
    
    urls = [
        "http://www.bbci.de/competition/download/competition_iv/BCICIV_2a_gdf.zip",
        "http://www.bbci.de/competition/download/competition_iv/true_labels.zip"
    ]
    
    os.makedirs("../raw/bci_iv_2a", exist_ok=True)
    
    for url in urls:
        filename = os.path.join("../raw/bci_iv_2a", os.path.basename(url))
        print(f"Descargando {url}...")
        urllib.request.urlretrieve(url, filename)
        
        # Descomprimir
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall("../raw/bci_iv_2a/")
        
        os.remove(filename)  # Eliminar zip
    
    print("Descarga completada")

if __name__ == "__main__":
    download_bci_iv_2a()
```

### 3.2 Descargar PhysioNet

```bash
python download_physionet_mmi.py
```

### 3.3 Descargar todo

```bash
python download_all.py
```

---

## 4. Datos de Ejemplo (Sample Data)

Para pruebas rapidas sin descargar datasets completos, se incluyen datos de ejemplo pequenos.

### 4.1 Cargar datos de ejemplo

```python
import numpy as np

# Cargar EEG de ejemplo
eeg_sample = np.load("data/sample_data/sample_eeg.npy")
print(f"Forma: {eeg_sample.shape}")  # (canales, muestras)

# Cargar etiquetas
labels = np.load("data/sample_data/sample_labels.npy")
print(f"Etiquetas: {labels}")

# Cargar caracteristicas pre-extraidas
features = np.load("data/sample_data/sample_features.npy")
print(f"Caracteristicas: {features.shape}")
```

### 4.2 Generar tus propios datos de ejemplo

```python
import numpy as np

# Generar datos simulados
n_channels = 8
n_samples = 2500  # 10 segundos a 250 Hz
eeg_data = np.random.randn(n_channels, n_samples) * 10  # Escala microvolts

# Guardar
np.save("data/sample_data/my_sample.npy", eeg_data)
```

---

## 5. Procesamiento de Datos

### 5.1 Convertir GDF a numpy

```python
import mne
import numpy as np

# Cargar archivo GDF (formato de BCI Competition)
raw = mne.io.read_raw_gdf("data/raw/bci_iv_2a/A01T.gdf", preload=True)

# Obtener datos y eventos
data = raw.get_data()
events = mne.find_events(raw)

# Guardar en formato numpy
np.save("data/processed/A01T_data.npy", data)
np.save("data/processed/A01T_events.npy", events)
```

### 5.2 Extraer ventanas etiquetadas

```python
import numpy as np

def extract_epochs(data, events, event_id, tmin=0, tmax=4, fs=250):
    """Extrae ventanas de tiempo alrededor de eventos"""
    
    n_samples = int((tmax - tmin) * fs)
    epochs = []
    
    for event in events:
        if event[2] == event_id:
            start = event[0] + int(tmin * fs)
            if start + n_samples < data.shape[1]:
                epoch = data[:, start:start+n_samples]
                epochs.append(epoch)
    
    return np.array(epochs)
```

---

## 6. Estructura de Datos Procesados (Recomendada)

Para mantener consistencia en el entrenamiento, se recomienda esta estructura:

```
data/processed/
├── subject_01/
│   ├── train_data.npy      # (n_trials, n_channels, n_samples)
│   ├── train_labels.npy     # (n_trials,)
│   ├── test_data.npy
│   └── test_labels.npy
├── subject_02/
│   └── ...
└── all_subjects/
    ├── X_train.npy
    ├── y_train.npy
    ├── X_test.npy
    └── y_test.npy
```

---

## 7. Scripts de Utilidad

### 7.1 Ver informacion de dataset

```python
def dataset_info(data, labels):
    print(f"Forma datos: {data.shape}")
    print(f"Rango valores: [{data.min():.2f}, {data.max():.2f}]")
    print(f"Clases: {np.unique(labels)}")
    print(f"Distribucion: {np.bincount(labels)}")
```

### 7.2 Balancear clases

```python
from sklearn.utils import resample

def balance_classes(X, y):
    """Balancea clases usando oversampling"""
    
    classes = np.unique(y)
    max_size = max(np.bincount(y))
    
    X_balanced = []
    y_balanced = []
    
    for c in classes:
        X_c = X[y == c]
        if len(X_c) < max_size:
            # Oversampling
            X_resampled = resample(X_c, replace=True, n_samples=max_size, random_state=42)
            X_balanced.append(X_resampled)
            y_balanced.append([c] * max_size)
        else:
            X_balanced.append(X_c)
            y_balanced.append([c] * len(X_c))
    
    X_balanced = np.vstack(X_balanced)
    y_balanced = np.concatenate(y_balanced)
    
    return X_balanced, y_balanced
```

---

## 8. Referencias Bibliograficas

```bibtex
@article{bci_iv_2008,
  title={The BCI competition IV: Dataset 2a},
  author={Tangermann, Michael and others},
  journal={Journal of Neural Engineering},
  year={2012}
}

@article{physionet_2000,
  title={PhysioBank, PhysioToolkit, and PhysioNet},
  author={Goldberger, Ary L. and others},
  journal={Circulation},
  year={2000}
}
```

---

## 9. Notas de Uso

- Los datasets publicos son para uso academico/investigacion
- Verificar licencias antes de uso comercial
- Los datos de ejemplo son simulados y no representan senales reales
- Para reproducibilidad, anotar version de los datasets usados

---

*Documento version 1.0 - 2026*
```
