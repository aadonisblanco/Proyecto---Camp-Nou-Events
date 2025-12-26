# test_audio.py
from audio_manager import audio_manager
import time

print("🔊 Probando sistema de audio...")
print("-" * 40)

# Iniciar música (ya se inicia automáticamente al importar, pero lo forzamos)
print("1. Iniciando himno...")
audio_manager.play_himno()

print("2. Esperando 5 segundos...")
time.sleep(5)

print("3. Deteniendo música...")
audio_manager.stop()

print("✅ Prueba completada")
input("Presiona Enter para salir...")