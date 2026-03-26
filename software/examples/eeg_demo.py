#!/usr/bin/env python3
"""
ENA - Demo básico de adquisición de EEG
Ejemplo para NeuroSky MindWave Mobile 2
"""

import time
import sys

try:
    import neurosky2
except ImportError:
    print("Instala neurosky2: pip install neurosky2")
    sys.exit(1)

def main():
    print("ENA - Demo de EEG")
    print("Conectando a NeuroSky MindWave...")
    print("Asegúrate de que el headset esté encendido y emparejado por Bluetooth")
    print("Presiona Ctrl+C para salir\n")
    
    try:
        # Conectar al dispositivo
        headset = neurosky2.Headset()
        
        # Esperar conexión
        time.sleep(2)
        
        print("✅ Conectado. Leyendo señales EEG...")
        print("Formato: | Atención | Meditación | Calidad Señal |\n")
        
        while True:
            # Leer datos
            attention = headset.attention
            meditation = headset.meditation
            signal_quality = headset.signal_quality
            
            # Mostrar en consola
            print(f"| {attention:>8} | {meditation:>9} | {signal_quality:>12} |", end='\r')
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\nDemo finalizada.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Verifica que el headset esté encendido y emparejado.")

if __name__ == "__main__":
    main()
