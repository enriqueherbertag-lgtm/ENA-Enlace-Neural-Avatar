# Configuracion de Raspberry Pi para ENA

Guia completa para preparar una Raspberry Pi como unidad central del sistema ENA.

---

## 1. Modelos Compatibles

| Modelo | RAM minima | Recomendado para |
|:---|:---|:---|
| Raspberry Pi 4B | 2GB | Todos los modos de ENA |
| Raspberry Pi 4B | 4GB | Modo investigacion + analisis avanzado |
| Raspberry Pi 3B+ | 1GB | Modo basico (solo comunicacion) |
| Raspberry Pi 5 | 4GB | Desarrollo futuro (no testeado aun) |

**Recomendacion principal:** Raspberry Pi 4B con 2GB o 4GB RAM.

---

## 2. Material Necesario

### 2.1 Incluido en el kit ENA

- Raspberry Pi 4B (2GB)
- Fuente de poder 5V/3A USB-C
- Cable HDMI
- Tarjeta microSD 16GB (con sistema preinstalado)

### 2.2 Necesario por separado (no incluido)

- Monitor HDMI
- Teclado USB
- Mouse USB
- Cable Ethernet (opcional, para red cableada)
- Carcasa protectora (recomendada)

---

## 3. Instalacion del Sistema Operativo desde Cero

### 3.1 Descargar Raspberry Pi OS

```bash
# Desde un computador, descargar Raspberry Pi Imager
# https://www.raspberrypi.com/software/

# O descargar imagen directamente (recomendado para ENA)
# Raspberry Pi OS Lite (32-bit) sin escritorio
# https://www.raspberrypi.com/software/operating-systems/
```

### 3.2 Grabar imagen en microSD con Raspberry Pi Imager

```bash
# Pasos:
# 1. Abrir Raspberry Pi Imager
# 2. Seleccionar SO: Raspberry Pi OS Lite (32-bit)
# 3. Seleccionar almacenamiento: (tu microSD)
# 4. Click en engranaje para opciones avanzadas:
#    - Habilitar SSH
#    - Usuario: ena
#    - Password: ena123
#    - Configurar WiFi (opcional)
# 5. Click en Grabar
```

### 3.3 Grabar imagen manualmente (alternativa)

```bash
# Si prefieres linea de comandos:
# Identificar la microSD (ej: /dev/sdb)
lsblk

# Descargar imagen
wget https://downloads.raspberrypi.org/raspios_lite_armhf/images/.../2024-XX-XX-raspios-bullseye-armhf-lite.img.xz

# Descomprimir
unxz 2024-XX-XX-raspios-bullseye-armhf-lite.img.xz

# Grabar (CUIDADO: reemplazar /dev/sdX con tu dispositivo)
sudo dd if=raspios-lite.img of=/dev/sdX bs=4M status=progress

# Habilitar SSH (crear archivo vacio en particion boot)
touch /media/boot/ssh
```

---

## 4. Primer Arranque y Configuracion

### 4.1 Conexion inicial

```bash
# Insertar microSD en Raspberry Pi
# Conectar HDMI, teclado, mouse, Ethernet
# Conectar fuente de poder

# El sistema arrancara automaticamente
# Usuario: ena
# Password: ena123

# Si usaste WiFi en configuracion, puedes conectar por SSH:
ssh ena@(ip-de-la-pi)
# Encontrar IP: mirar router o usar `arp -a`
```

### 4.2 Configuracion basica

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Cambiar password (opcional pero recomendado)
passwd

# Expandir sistema de archivos (si no se expandio automaticamente)
sudo raspi-config
# 6 Advanced Options -> A1 Expand Filesystem
```

### 4.3 Configurar nombre de equipo (opcional)

```bash
sudo raspi-config
# 1 System Options -> S4 Hostname -> ena-001
```

---

## 5. Instalacion de Dependencias para ENA

### 5.1 Dependencias base

```bash
# Instalar herramientas basicas
sudo apt install -y python3-pip python3-dev git bluetooth bluez bluez-tools rfkill

# Instalar librerias graficas (para modo avatar)
sudo apt install -y python3-tk python3-pil python3-pil.imagetk
```

### 5.2 Instalar dependencias Python

```bash
# Actualizar pip
pip3 install --upgrade pip

# Instalar librerias cientificas
pip3 install numpy pandas scipy scikit-learn matplotlib

# Instalar BrainFlow (para lectura EEG)
pip3 install brainflow

# Instalar OpenBCI (opcional, si usas OpenBCI)
pip3 install openbci-ganglion

# Instalar herramientas para procesamiento de senales
pip3 install mne neurokit2
```

### 5.3 Verificar instalaciones

```bash
# Probar BrainFlow
python3 -c "import brainflow; print('BrainFlow OK')"

# Probar MNE
python3 -c "import mne; print('MNE OK')"

# Probar sklearn
python3 -c "from sklearn.ensemble import RandomForestClassifier; print('Scikit-learn OK')"
```

---

## 6. Configuracion de Bluetooth

### 6.1 Activar Bluetooth

```bash
# Habilitar Bluetooth
sudo rfkill unblock bluetooth
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# Verificar estado
systemctl status bluetooth
```

### 6.2 Probar escaneo

```bash
# Iniciar consola Bluetooth
bluetoothctl

# Escanear dispositivos
scan on

# Ver dispositivos detectados (aparecera NeuroSky si esta encendido)
# Salir con Ctrl+D o escribiendo 'exit'
```

---

## 7. Configuracion de Red

### 7.1 WiFi

```bash
sudo raspi-config
# 1 System Options -> S1 Wireless LAN
# Ingresar SSID y password
```

### 7.2 IP fija (opcional)

```bash
sudo nano /etc/dhcpcd.conf

# Agregar al final (ajustar segun tu red):
# interface wlan0
# static ip_address=192.168.1.100/24
# static routers=192.168.1.1
# static domain_name_servers=8.8.8.8 8.8.4.4

# Guardar y reiniciar
sudo reboot
```

---

## 8. Instalacion del Software ENA

### 8.1 Clonar repositorio

```bash
git clone https://github.com/enriqueherbertag-lgtm/ENA-Enlace-Neural-Avatar.git
cd ENA-Enlace-Neural-Avatar
```

### 8.2 Instalar requirements

```bash
pip3 install -r requirements.txt
```

### 8.3 Probar instalacion

```bash
# Probar lectura de EEG con simulador (sin hardware)
cd software/eeg-reader
python3 test_simulated.py

# Probar avatar basico
cd ../avatar
python3 simple_avatar.py
```

---

## 9. Optimizaciones para Rendimiento

### 9.1 Overclock (opcional)

```bash
sudo nano /boot/config.txt

# Agregar al final:
# over_voltage=2
# arm_freq=1750
# gpu_freq=500

# Requiere buen enfriamiento (ventilador)
```

### 9.2 Deshabilitar servicios innecesarios

```bash
# Deshabilitar Bluetooth (si no se usa)
sudo systemctl disable bluetooth

# Deshabilitar WiFi (si se usa Ethernet)
sudo systemctl disable wpa_supplicant
```

### 9.3 Reducir latencia

```bash
# Ajustar prioridad de proceso para ENA
sudo renice -20 -p $(pgrep -f python3)
```

---

## 10. Creacion de Imagen de Backup

### 10.1 Desde Raspberry Pi

```bash
# Crear imagen comprimida de la microSD
sudo dd if=/dev/mmcblk0 bs=4M status=progress | gzip > ena-backup-$(date +%Y%m%d).img.gz
```

### 10.2 Desde computador externo

```bash
# Con microSD conectada a PC
sudo dd if=/dev/sdX bs=4M status=progress | gzip > ena-backup.img.gz
```

---

## 11. Problemas Comunes y Soluciones

| Problema | Causa | Solucion |
|:---|:---|:---|
| No arranca | MicroSD mal grabada | Re-grabar imagen |
| | Fuente insuficiente | Usar fuente oficial 5V/3A |
| Sobrecalentamiento | Sin ventilador | Agregar disipador/ventilador |
| Bluetooth no funciona | Hardware bloqueado | `sudo rfkill unblock bluetooth` |
| Wifi no conecta | SSID/password incorrectos | Reconfigurar en raspi-config |
| Python no encuentra modulos | Instalacion incompleta | Reinstalar requirements.txt |

---

## 12. Referencias

- Documentacion oficial Raspberry Pi: https://www.raspberrypi.com/documentation/
- Foro Raspberry Pi: https://forums.raspberrypi.com/
- Repositorio ENA: https://github.com/enriqueherbertag-lgtm/ENA-Enlace-Neural-Avatar

---

*Documento version 1.0 - 2026*
```
