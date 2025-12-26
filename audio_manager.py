# audio_manager.py
import os
import sys
import subprocess
import threading
import time

class AudioManager:
    """Gestor de audio para reproducir el himno del Barça"""
    
    def __init__(self):
        self.process = None
        self.playing = False
        
    def play_himno(self):
        """Reproduce el himno en bucle usando Windows Media Player"""
        # Verificar que el archivo existe
        archivo = self._find_himno_file()
        if not archivo:
            print("⚠ himno_barca.mp3 no encontrado en el proyecto")
            return False
        
        print(f"🎵 Reproduciendo: {os.path.basename(archivo)}")
        
        try:
            # Crear un archivo .wpl (Windows Playlist) para bucle infinito
            wpl_content = f'''<?wpl version="1.0"?>
    <smil>
        <head>
            <meta name="Generator" content="Microsoft Windows Media Player"/>
            <author/>
            <title>Himno Barça</title>
        </head>
        <body>
            <seq repeatCount="indefinite">
                <media src="{os.path.abspath(archivo).replace('\\', '/')}"/>
            </seq>
        </body>
    </smil>'''
            
            # Guardar la playlist
            with open("himno_loop.wpl", "w", encoding="utf-8") as f:
                f.write(wpl_content)
            
            # Ejecutar Windows Media Player en modo oculto con la playlist
            # El parámetro /play hace que empiece a reproducir automáticamente
            # El parámetro /TaskNowPlaying oculta la interfaz
            self.process = subprocess.Popen(
                ['wmplayer.exe', '/play', '/TaskNowPlaying', 'himno_loop.wpl'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.playing = True
            print("✅ Himno del Barça iniciado (en bucle)")
            return True
            
        except Exception as e:
            print(f"❌ Error al reproducir: {e}")
            return False
    
    def _find_himno_file(self):
        """Busca el archivo del himno"""
        posibles_nombres = [
            "himno_barca.mp3",
            "HIMNO_BARCA.mp3",
            "himno.mp3",
            "barca_himno.mp3",
            "cant_del_barca.mp3"
        ]
        
        for nombre in posibles_nombres:
            if os.path.exists(nombre):
                return nombre
        return None
    
    def stop(self):
        """Detiene la reproducción"""
        if self.process:
            try:
                # Matar el proceso de Windows Media Player
                subprocess.run(['taskkill', '/F', '/IM', 'wmplayer.exe'], 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
                
                # Eliminar archivo de playlist temporal
                if os.path.exists("himno_loop.wpl"):
                    os.remove("himno_loop.wpl")
                
                self.process = None
                self.playing = False
                print("⏹️  Música detenida")
                
            except Exception as e:
                print(f"⚠ Error al detener música: {e}")
    
    def is_playing(self):
        """Verifica si la música está reproduciéndose"""
        return self.playing


# Instancia global del gestor de audio
audio_manager = AudioManager()

def iniciar_himno_automatico():
    """Función para iniciar el himno automáticamente"""
    # Pequeño retraso para que no interfiera con el inicio de la aplicación
    time.sleep(1)
    audio_manager.play_himno()

# Iniciar automáticamente al importar este módulo
threading.Thread(target=iniciar_himno_automatico, daemon=True).start()