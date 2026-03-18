# Guia de Instalacion - ENA (Enlace Neural con Avatar)

Instrucciones tecnicas para instalar y configurar el sistema ENA desde cero.

---

## 1. Requisitos de Hardware

### 1.1 Minimos recomendados

| Componente | Especificacion |
|:---|:---|
| Raspberry Pi | Modelo 4B (2GB RAM o superior) |
| MicroSD | 16GB Clase 10 |
| Fuente de poder | 5V/3A USB-C |
| Casco EEG | NeuroSky MindWave 2 |
| Monitor | HDMI, 720p o superior |

### 1.2 Opcionales

- Camara web (para videollamadas futuras)
- Altavoces o audifonos
- Adaptador Bluetooth USB (si la Pi no tiene)

---

## 2. Instalacion del Sistema Operativo

### 2.1 Descargar Raspberry Pi OS

```bash
# Desde otro computador, descargar la imagen
# Recomendado: Raspberry Pi OS Lite (32-bit) sin escritorio
# https://www.raspberrypi.com/software/operating-systems/
```

### 2.2 Grabar imagen en microSD

```bash
# Usar Raspberry Pi Imager o balenaEtcher
# Seleccionar:
# - SO: Raspberry Pi OS Lite
# - Tarjeta: (su microSD)
# - Opciones avanzadas: habilitar SSH, usuario: ena, password: ena123
```

### 2.3 Primer inicio

```bash
# Insertar microSD en Raspberry Pi
# Conectar Ethernet (o configurar WiFi en el primer arranque)
# Encender

# Desde otro computador, conectar por SSH:
ssh ena@(ip-de-la-pi)
# Password: ena123
```

---

## 3. Configuracion Base del Sistema

### 3.1 Actualizar sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Instalar dependencias basicas

```bash
sudo apt install -y python3-pip python3-dev git bluetooth bluez bluez-tools rfkill
```

### 3.3 Habilitar Bluetooth

```bash
sudo rfkill unblock bluetooth
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

---

## 4. Instalacion del Software ENA

### 4.1 Clonar repositorio

```bash
git clone https://github.com/enriqueherbertag-lgtm/ENA-Enlace-Neural-Avatar.git
cd ENA-Enlace-Neural-Avatar
```

### 4.2 Instalar dependencias Python

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### 4.3 Compilar modulos nativos (opcional, para mejor rendimiento)

```bash
cd software/eeg-reader
python3 setup.py build_ext --inplace
cd ../..
```

---

## 5. Configuracion del Casco EEG

### 5.1 Emparejar NeuroSky

```bash
# Iniciar consola Bluetooth
bluetoothctl

# Encender el NeuroSky (presionar boton 2 segundos)
# Buscar dispositivo
scan on

# Ver direccion MAC (ej: 00:13:EF:XX:XX:XX)
# Emparejar
pair XX:XX:XX:XX:XX:XX

# Conectar
connect XX:XX:XX:XX:XX:XX

# Confiar (conexion automatica)
trust XX:XX:XX:XX:XX:XX

# Salir
exit
```

### 5.2 Verificar conexion

```bash
cd software/eeg-reader
python3 test_connection.py --mac XX:XX:XX:XX:XX:XX
```

---

## 6. Configuracion del Avatar

### 6.1 Instalar dependencias graficas

```bash
sudo apt install -y python3-tk python3-pil python3-pil.imagetk
```

### 6.2 Probar avatar basico

```bash
cd software/avatar
python3 simple_avatar.py
```

### 6.3 Configurar resolucion (opcional)

```bash
# Editar archivo de configuracion
nano ~/.config/ena/config.yaml

# Ajustar:
# display:
#   width: 1280
#   height: 720
#   fullscreen: false
```

---

## 7. Configuracion de Arranque Automatico

### 7.1 Crear servicio systemd

```bash
sudo nano /etc/systemd/system/ena.service
```

### 7.2 Contenido del archivo

```ini
[Unit]
Description=ENA Neural Interface
After=bluetooth.target network.target

[Service]
Type=simple
User=ena
WorkingDirectory=/home/ena/ENA-Enlace-Neural-Avatar
ExecStart=/usr/bin/python3 /home/ena/ENA-Enlace-Neural-Avatar/software/avatar/simple_avatar.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 7.3 Habilitar servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable ena.service
sudo systemctl start ena.service
```

---

## 8. Configuracion de Red (Opcional)

### 8.1 WiFi

```bash
sudo raspi-config
# 1. System Options
# 2. Wireless LAN
# Ingresar SSID y password
```

### 8.2 IP fija (opcional)

```bash
sudo nano /etc/dhcpcd.conf

# Agregar al final:
# interface wlan0
# static ip_address=192.168.1.100/24
# static routers=192.168.1.1
# static domain_name_servers=8.8.8.8
```

---

## 9. Verificacion de Instalacion

### 9.1 Ejecutar pruebas automatizadas

```bash
cd /home/ena/ENA-Enlace-Neural-Avatar/software/examples
python3 run_all_tests.py
```

### 9.2 Verificar salida esperada

```
[TEST] Conexion Bluetooth: OK
[TEST] Lectura EEG: OK
[TEST] Procesamiento senal: OK
[TEST] Avatar 3D: OK
[TEST] Tasa refresco: 30 fps
```

---

## 10. Instalacion Avanzada (Opcional)

### 10.1 OpenBCI (para usuarios avanzados)

Si usa OpenBCI en lugar de NeuroSky:

```bash
cd hardware
python3 setup_openbci.py
```

### 10.2 Camara para videollamadas

```bash
sudo apt install -y fswebcam
# Probar camara
fswebcam test.jpg
```

### 10.3 Acceso remoto (VNC)

```bash
sudo raspi-config
# 3. Interface Options
# I3 VNC -> Enable
```

---

## 11. Solucion de Problemas de Instalacion

| Problema | Solucion |
|:---|:---|
| Bluetooth no funciona | `sudo rfkill unblock bluetooth` y reiniciar |
| Python no encuentra modulos | `pip3 install --upgrade -r requirements.txt` |
| Avatar no inicia | Verificar `DISPLAY=:0` y permisos de video |
| Conexion NeuroSky falla | Probar con otro dispositivo, verificar MAC |
| Sistema lento | Reducir resolucion, cerrar otras apps |

---

## 12. Referencias

- Documentacion oficial Raspberry Pi: https://www.raspberrypi.com/documentation/
- BrainFlow NeuroSky: https://brainflow.readthedocs.io/
- Repositorio ENA: https://github.com/enriqueherbertag-lgtm/ENA-Enlace-Neural-Avatar

---

*Documento version 1.0 - 2026*
```
