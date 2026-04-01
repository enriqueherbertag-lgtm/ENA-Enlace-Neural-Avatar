# Guia de Contribucion - ENA (Enlace Neural con Avatar)

Gracias por tu interes en contribuir a ENA. Este documento establece las pautas para colaborar en el proyecto de manera efectiva y respetuosa.

---

## 1. Formas de Contribuir

### 1.1 Reportar problemas (Issues)

Si encuentras un error o tienes una sugerencia:

- Busca primero en los issues existentes para evitar duplicados
- Usa la plantilla correspondiente (bug report, feature request)
- Incluye informacion detallada:
  - Hardware utilizado (NeuroSky, OpenBCI, etc.)
  - Version de software
  - Pasos para reproducir el error
  - Logs o mensajes de error

### 1.2 Sugerir mejoras (Feature requests)

- Describe claramente la funcionalidad propuesta
- Explica por que seria util para los usuarios
- Si es posible, menciona como podria implementarse
- Incluye referencias a estudios o proyectos similares

### 1.3 Contribuir con codigo (Pull Requests)

- Fork del repositorio
- Crear una rama con nombre descriptivo
- Seguir los estandares de codigo
- Incluir pruebas cuando corresponda
- Actualizar documentacion si es necesario

### 1.4 Mejorar documentacion

- Correcciones ortograficas o de formato
- Traducciones
- Ejemplos adicionales
- Guias mas claras

### 1.5 Compartir experiencias

- Casos de uso reales
- Configuraciones que funcionaron
- Resultados de pruebas con usuarios

---

## 2. Flujo de Trabajo para Contribuciones

### 2.1 Para contribuciones pequenas (documentacion, bugs simples)

```bash
# 1. Fork del repositorio
# 2. Clonar localmente
git clone https://github.com/tu-usuario/ENA-Enlace-Neural-Avatar.git

# 3. Crear rama
git checkout -b fix/descripcion-breve

# 4. Hacer cambios y commit
git add .
git commit -m "Fix: descripcion del cambio"

# 5. Push y crear Pull Request
git push origin fix/descripcion-breve
```

### 2.2 Para contribuciones grandes (nuevas features)

1. Abrir un issue primero para discutir la idea
2. Esperar feedback de los mantenedores
3. Coordinar para evitar trabajo duplicado
4. Seguir el mismo proceso de PR

---

## 3. Estandares de Codigo

### 3.1 Python

- Seguir PEP 8
- Usar nombres descriptivos (variables, funciones, clases)
- Incluir docstrings en formato Google o NumPy
- Mantener funciones pequenas y enfocadas
- Comentar secciones complejas

**Ejemplo:**

```python
def extract_features(eeg_data, sampling_rate=250):
    """Extrae caracteristicas de una senal EEG.
    
    Args:
        eeg_data (numpy array): Datos EEG con forma (canales, muestras)
        sampling_rate (int): Tasa de muestreo en Hz
    
    Returns:
        numpy array: Vector de caracteristicas extraidas
    """
    # Validar entrada
    if eeg_data.ndim != 2:
        raise ValueError("eeg_data debe tener 2 dimensiones")
    
    # Procesar...
    features = compute_power_bands(eeg_data, sampling_rate)
    
    return features
```

### 3.2 Documentacion (Markdown)

- Usar titulos con `#`, `##`, `###` de forma jerarquica
- Separar secciones con `---`
- Usar listas con `-` o `1.`
- Para codigo, usar bloques con ```lenguaje
- Mantener lineas no muy largas (max 80-100 caracteres)

### 3.3 Commits

- Usar mensajes claros en ingles o español
- Formato: `Tipo: Descripcion breve`
- Tipos comunes: `Fix`, `Feat`, `Docs`, `Style`, `Refactor`, `Test`

**Ejemplos:**
```
Fix: Corregir conexion Bluetooth en Raspberry Pi
Feat: Agregar clasificador SSVEP
Docs: Actualizar manual de usuario con nuevos comandos
```

---

## 4. Estructura de Directorios

Al agregar nuevos archivos, mantener la estructura existente:

```
ENA-Enlace-Neural-Avatar/
├── docs/                    # Documentacion
├── hardware/                # Guias de hardware
├── software/                # Codigo fuente
│   ├── eeg-reader/          # Lectura de senales
│   ├── classifier/          # Clasificadores
│   ├── avatar/              # Visualizacion
│   └── examples/            # Ejemplos
├── data/                    # Datasets y referencias
└── comunidad/               # Comunidad y contribucion
```

---

## 5. Pruebas

### 5.1 Tipos de pruebas esperadas

- **Pruebas unitarias**: Para funciones individuales
- **Pruebas de integracion**: Para modulos completos
- **Pruebas con hardware**: Verificar funcionamiento con dispositivos reales

### 5.2 Ejecutar pruebas

```bash
# Desde la raiz del proyecto
pytest tests/

# O para modulos especificos
pytest tests/test_feature_extractor.py
```

### 5.3 Agregar nuevas pruebas

Crear archivos en `tests/` con el prefijo `test_`:

```python
# tests/test_feature_extractor.py
import numpy as np
from eeg_reader.feature_extractor import FeatureExtractor

def test_extractor_output_shape():
    extractor = FeatureExtractor()
    data = np.random.randn(8, 500)  # 8 canales, 500 muestras
    features = extractor.extract(data)
    assert features.ndim == 1
    assert features.shape[0] > 0
```

---

## 6. Documentacion de Cambios

### 6.1 Actualizar README

Si tu cambio afecta la funcionalidad principal:

- Actualizar la descripcion en `README.md` raiz
- Actualizar `docs/` correspondientes
- Agregar ejemplos si es relevante

### 6.2 Changelog

Los cambios importantes se registran en `CHANGELOG.md`:

```markdown
## [1.1.0] - 2026-03-15
### Added
- Nuevo clasificador SSVEP para control de silla de ruedas
- Soporte para OpenBCI Cyton de 8 canales

### Fixed
- Correccion en calibracion de NeuroSky
- Mejora en estabilidad de conexion Bluetooth
```

---

## 7. Contribuciones Especiales

### 7.1 Ana de Deepseek (Asistencia Tecnica)

Ana de Deepseek ha colaborado activamente en:

- Estructuracion de documentacion
- Revision de formato y consistencia
- Generacion de ejemplos de codigo
- Soporte en la organizacion del repositorio

Sus contribuciones se consideran parte del proyecto bajo los mismos terminos de licencia que el resto del codigo, y son propiedad del autor principal (Enrique Aguayo).

---

## 8. Conducta y Respeto

### 8.1 Codigo de Conducta

- Ser respetuoso con otros colaboradores
- Aceptar criticas constructivas
- Enfocarse en lo tecnico, no en lo personal
- Ayudar a mantener un ambiente inclusivo

### 8.2 Comunicacion

- Usar un tono profesional y amigable
- En issues, describir el problema sin suposiciones
- En PR, explicar los cambios realizados
- Responder comentarios en tiempo razonable

---

## 9. Revision de Pull Requests

### 9.1 Criterios de aceptacion

- El codigo pasa todas las pruebas
- Sigue los estandares de codigo
- Incluye documentacion actualizada
- No introduce regresiones
- Tiene sentido dentro del proyecto

### 9.2 Proceso de revision

1. Un mantenedor revisara el PR en 3-5 dias
2. Se pueden solicitar cambios
3. Una vez aprobado, se mergea a main
4. Se cierra el issue relacionado (si existe)

---

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

## 11. Contacto

- **Issues**: Para reportar problemas o sugerencias
- **Discussions**: Para preguntas generales o ideas
- **Email**: eaguayo@migst.cl (solo para asuntos importantes)

---

*Documento version 1.1 - 2026 (incluye reconocimiento a Ana de Deepseek por asistencia tecnica)*
```
