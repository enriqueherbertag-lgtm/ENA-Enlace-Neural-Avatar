# Avatar - Modulo de Visualizacion y Control de Avatar 3D

Este modulo se encarga de la representacion grafica del avatar y la traduccion de los comandos del clasificador en movimientos visibles en pantalla.

---

## 1. Estructura del Modulo

```
software/avatar/
├── README.md                    # Este archivo
├── __init__.py                  # Inicializador del modulo
├── avatar_base.py                # Clase base para avatares
├── simple_avatar.py              # Avatar 2D simple (basico)
├── unity_avatar.py                # Integracion con Unity WebGL
├── three_avatar.py                # Avatar con Three.js (navegador)
├── animations.py                  # Definicion de animaciones
├── config.yaml                    # Configuracion de visualizacion
├── assets/                         # Recursos graficos
│   ├── models/                     # Modelos 3D
│   ├── textures/                   # Texturas
│   └── animations/                  # Archivos de animacion
└── examples/                        # Ejemplos de uso
    ├── demo_simple.py
    └── demo_three.html
```

---

## 2. Instalacion de Dependencias

### 2.1 Para avatar simple (2D)

```bash
# Ya instalado con dependencias base
# tkinter, PIL, numpy
```

### 2.2 Para avatar Three.js (navegador)

```bash
# No requiere instalacion Python adicional
# Solo un navegador web moderno
```

### 2.3 Para integracion Unity (avanzado)

```bash
# Requiere Unity instalado por separado
# Los archivos generados se sirven via HTTP
pip install flask  # Para servir archivos localmente
```

---

## 3. Uso Basico

### 3.1 Avatar simple (2D) - Para pruebas rapidas

```python
from avatar.simple_avatar import SimpleAvatar

# Crear avatar
avatar = SimpleAvatar(width=800, height=600)

# Inicializar ventana
avatar.init_window()

# Bucle de control
for command in commands:  # commands viene del clasificador
    if command == 'left':
        avatar.move_left()
    elif command == 'right':
        avatar.move_right()
    elif command == 'up':
        avatar.move_forward()
    else:
        avatar.stop()
    
    avatar.update()  # Actualizar pantalla
    time.sleep(0.1)
```

### 3.2 Avatar Three.js (navegador)

```python
from avatar.three_avatar import ThreeAvatar

# Crear servidor de avatar
avatar = ThreeAvatar(port=8000)

# Iniciar servidor (abre navegador automaticamente)
avatar.start()

# Enviar comandos mientras corre
avatar.send_command('wave')
avatar.send_command('smile')
avatar.send_command('walk')
```

### 3.3 Configuracion basica (config.yaml)

```yaml
# config.yaml
window:
  width: 1024
  height: 768
  fullscreen: false
  background_color: "#2c3e50"

avatar:
  type: "human"  # human, robot, animal
  skin_color: "#f5d0a9"
  model: "assets/models/default.glb"
  
animations:
  idle: "assets/animations/idle.fbx"
  walk: "assets/animations/walk.fbx"
  wave: "assets/animations/wave.fbx"
  smile: "assets/animations/smile.fbx"

feedback:
  show_eeg: false  # Mostrar grafica EEG
  show_commands: true  # Mostrar comandos detectados
  font_size: 14
```

---

## 4. Clases Principales

### 4.1 AvatarBase (clase base)

```python
class AvatarBase:
    """Clase base para todos los avatares"""
    
    def __init__(self, config_path="config.yaml"):
        self.load_config(config_path)
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.current_animation = "idle"
    
    def load_config(self, path):
        """Carga configuracion desde YAML"""
        pass
    
    def move_left(self):
        """Mover avatar a la izquierda"""
        self.position[0] -= 0.1
    
    def move_right(self):
        """Mover avatar a la derecha"""
        self.position[0] += 0.1
    
    def move_forward(self):
        """Mover avatar hacia adelante"""
        self.position[1] += 0.1
    
    def move_backward(self):
        """Mover avatar hacia atras"""
        self.position[1] -= 0.1
    
    def wave(self):
        """Hacer gesto de saludo"""
        self.current_animation = "wave"
    
    def smile(self):
        """Cambiar expresion a sonrisa"""
        self.current_animation = "smile"
    
    def update(self):
        """Actualizar visualizacion"""
        raise NotImplementedError
```

### 4.2 SimpleAvatar (tkinter)

```python
class SimpleAvatar(AvatarBase):
    """Implementacion simple con tkinter (2D)"""
    
    def __init__(self, width=800, height=600):
        super().__init__()
        self.width = width
        self.height = height
        self.canvas = None
    
    def init_window(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height,
            bg=self.config['window']['background_color']
        )
        self.canvas.pack()
        self.draw_avatar()
    
    def draw_avatar(self):
        """Dibujar avatar simple (circulos y lineas)"""
        x = self.width // 2 + self.position[0] * 100
        y = self.height // 2 - self.position[1] * 100
        
        # Cabeza
        self.canvas.create_oval(x-50, y-100, x+50, y, fill="white")
        
        # Ojos
        if self.current_animation == "smile":
            # Ojos felices (^_^)
            self.canvas.create_arc(x-30, y-70, x-10, y-50, start=0, extent=180, fill="black")
            self.canvas.create_arc(x+10, y-70, x+30, y-50, start=0, extent=180, fill="black")
        else:
            # Ojos normales
            self.canvas.create_oval(x-30, y-70, x-20, y-60, fill="black")
            self.canvas.create_oval(x+20, y-70, x+30, y-60, fill="black")
        
        # Boca segun animacion
        if self.current_animation == "smile":
            self.canvas.create_arc(x-20, y-40, x+20, y-20, start=0, extent=-180, fill="black")
        else:
            self.canvas.create_line(x-20, y-30, x+20, y-30, fill="black", width=2)
    
    def update(self):
        """Actualizar canvas"""
        self.canvas.delete("all")
        self.draw_avatar()
        self.root.update()
```

### 4.3 ThreeAvatar (navegador)

```python
class ThreeAvatar(AvatarBase):
    """Avatar con Three.js via navegador web"""
    
    def __init__(self, port=8000):
        super().__init__()
        self.port = port
        self.server = None
    
    def start(self):
        """Iniciar servidor web y abrir navegador"""
        import threading
        import webbrowser
        from http.server import HTTPServer, SimpleHTTPRequestHandler
        
        # Configurar servidor
        os.chdir(os.path.dirname(__file__))
        handler = SimpleHTTPRequestHandler
        self.server = HTTPServer(('localhost', self.port), handler)
        
        # Iniciar en thread separado
        thread = threading.Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()
        
        # Abrir navegador
        webbrowser.open(f'http://localhost:{self.port}/three_avatar.html')
    
    def send_command(self, command):
        """Enviar comando via WebSocket/HTTP"""
        import requests
        try:
            requests.post(
                f'http://localhost:{self.port}/command',
                json={'command': command}
            )
        except:
            pass
```

---

## 5. Archivos HTML para Three.js

### 5.1 three_avatar.html (simplificado)

```html
<!DOCTYPE html>
<html>
<head>
    <title>ENA Avatar</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #2c3e50; }
        #info {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <div id="info">Comando: <span id="command">idle</span></div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Escena basica
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        // Avatar simple (cubo con cara)
        const geometry = new THREE.BoxGeometry(2, 3, 1);
        const material = new THREE.MeshBasicMaterial({ color: 0xf5d0a9 });
        const avatar = new THREE.Mesh(geometry, material);
        scene.add(avatar);
        
        // Ojos
        const eyeGeo = new THREE.SphereGeometry(0.3);
        const eyeMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
        const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
        leftEye.position.set(-0.7, 0.5, 0.6);
        avatar.add(leftEye);
        
        const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
        rightEye.position.set(0.7, 0.5, 0.6);
        avatar.add(rightEye);
        
        // Boca
        const mouthGeo = new THREE.TorusGeometry(0.5, 0.1, 16, 32, Math.PI);
        const mouthMat = new THREE.MeshBasicMaterial({ color: 0x880000 });
        const mouth = new THREE.Mesh(mouthGeo, mouthMat);
        mouth.rotation.z = Math.PI;
        mouth.position.set(0, -0.3, 0.6);
        avatar.add(mouth);
        
        // Posicion camara
        camera.position.z = 10;
        
        // Comunicacion con servidor (simplificado - usar WebSocket real)
        function checkCommand() {
            fetch('/current_command')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('command').innerText = data.command;
                    
                    // Animar segun comando
                    if (data.command === 'left') {
                        avatar.rotation.y += 0.1;
                    } else if (data.command === 'right') {
                        avatar.rotation.y -= 0.1;
                    } else if (data.command === 'wave') {
                        avatar.rotation.z = Math.sin(Date.now() * 0.01) * 0.2;
                    } else {
                        avatar.rotation.y = 0;
                        avatar.rotation.z = 0;
                    }
                });
        }
        
        // Bucle de animacion
        function animate() {
            requestAnimationFrame(animate);
            checkCommand();
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Ajustar tamano de ventana
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
```

---

## 6. Integracion Completa

### 6.1 Ejemplo de uso en pipeline completo

```python
import time
from eeg_reader.neurosky_reader import NeuroSkyReader
from eeg_reader.feature_extractor import FeatureExtractor
from classifier.motor_imagery import MotorImageryClassifier
from avatar.simple_avatar import SimpleAvatar

# Inicializar componentes
reader = NeuroSkyReader(mac_address="00:13:EF:XX:XX:XX")
extractor = FeatureExtractor()
clf = MotorImageryClassifier.load_model("models/mi_model.pkl")
avatar = SimpleAvatar()

# Conectar
reader.connect()
avatar.init_window()

# Bucle principal
try:
    while True:
        # Leer EEG (2 segundos)
        data = reader.read(duration_seconds=2)
        
        # Extraer caracteristicas
        features = extractor.extract(data)
        
        # Clasificar
        command = clf.predict(features.reshape(1, -1))[0]
        
        # Mover avatar
        if command == 'left':
            avatar.move_left()
        elif command == 'right':
            avatar.move_right()
        elif command == 'up':
            avatar.move_forward()
        else:
            avatar.stop()
        
        # Actualizar pantalla
        avatar.update()
        
        # Pequena pausa
        time.sleep(0.1)
        
except KeyboardInterrupt:
    reader.disconnect()
    avatar.root.destroy()
```

### 6.2 Demo con Three.js y clasificador simulado

```python
from avatar.three_avatar import ThreeAvatar
import time
import random

# Iniciar avatar
avatar = ThreeAvatar(port=8000)
avatar.start()

# Simular comandos cada 3 segundos
commands = ['left', 'right', 'wave', 'smile', 'idle']

while True:
    cmd = random.choice(commands)
    print(f"Enviando comando: {cmd}")
    avatar.send_command(cmd)
    time.sleep(3)
```

---

## 7. Configuracion Avanzada

### 7.1 Animaciones personalizadas

```python
from avatar.animations import AnimationManager

# Cargar animaciones desde archivos
anim_manager = AnimationManager()
anim_manager.load_animation("dance", "assets/animations/dance.fbx")
anim_manager.load_animation("clap", "assets/animations/clap.fbx")

# Usar en avatar
avatar.set_animation("dance")
```

### 7.2 Feedback visual de EEG

```python
# En config.yaml
feedback:
  show_eeg: true
  eeg_channels: [1]  # Mostrar canal 1
  eeg_color: "#00ff00"
  update_rate: 10  # Hz
```

---

## 8. Troubleshooting

| Problema | Solucion |
|:---|:---|
| Ventana no aparece | Verificar `DISPLAY` en Linux, instalar tkinter |
| Three.js no carga | Verificar puerto 8000 libre, firewall |
| Animaciones lentas | Reducir calidad grafica en config |
| Avatar no responde | Verificar que comandos llegan (prints debug) |
| Error de dependencias | `pip install flask pillow` |

---

*Documento version 1.0 - 2026*
```
