# main.py
import tkinter as tk
from ui import EventOrganizerUI

def main():
    # Crear ventana principal
    root = tk.Tk()
    
    # Crear instancia de la interfaz
    app = EventOrganizerUI(root)
    
    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()