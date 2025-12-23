# main.py
# main.py
import tkinter as tk
import sys
import os

# Asegurar que Python encuentre los módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui import EventOrganizerUI
from Controller import ControladorEventos

class AplicacionPrincipal:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Crear la interfaz de usuario
        self.ui = EventOrganizerUI(self.root)
        
        # Crear el controlador
        self.controlador = ControladorEventos(self.ui)
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("Organizador de Eventos - Camp Nou")
        self.root.geometry("1000x750")
        
        # Icono de la ventana (opcional)
        try:
            self.root.iconbitmap("camp_nou.ico")
        except:
            pass
        
        # Centrar ventana en pantalla
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def cerrar_aplicacion(self):
        """Maneja el cierre de la aplicación"""
        # Aquí podrías agregar confirmación o guardado automático
        self.root.destroy()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = AplicacionPrincipal()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()