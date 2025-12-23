
# controller.py
from Events import GestorEventos, Evento, TIPOS_EVENTO, UBICACIONES_CAMP_NOU
from datetime import datetime
import tkinter.messagebox as messagebox

class ControladorEventos:
    """Controlador que maneja la lógica entre la UI y los eventos"""
    
    def __init__(self, ui):
        self.ui = ui
        self.gestor = GestorEventos()
        
        # Conectar eventos de la UI
        self.conectar_eventos()
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
    
    def conectar_eventos(self):
        """Conecta los botones de la UI con los métodos del controlador"""
        # Botones del formulario
        self.ui.save_button.config(command=self.guardar_evento)
        self.ui.clear_button.config(command=self.limpiar_formulario)
        
        # Botones de la pestaña de visualización
        self.ui.search_button.config(command=self.buscar_eventos)
        self.ui.show_all_button.config(command=self.mostrar_todos_eventos)
        self.ui.view_details_button.config(command=self.ver_detalles_evento)
        self.ui.delete_event_button.config(command=self.eliminar_evento)
        
        # Botón de estadísticas
        self.ui.update_stats_button.config(command=self.actualizar_estadisticas)
    
    def cargar_datos_iniciales(self):
        """Carga datos iniciales en la UI"""
        self.mostrar_todos_eventos()
        self.actualizar_estadisticas()
    
    def guardar_evento(self):
        """Procesa y guarda un nuevo evento desde el formulario"""
        try:
            # Obtener datos del formulario
            datos = self.ui.get_form_data()
            
            # Validar datos requeridos
            if not self.validar_datos_evento(datos):
                return
            
            # Crear el evento
            evento = self.gestor.crear_evento(**datos)
            
            if evento:
                messagebox.showinfo("Éxito", f"Evento '{evento.nombre}' creado exitosamente!")
                self.limpiar_formulario()
                self.mostrar_todos_eventos()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", "No se pudo crear el evento. Verifique los datos.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear evento: {str(e)}")
    
    def validar_datos_evento(self, datos: dict) -> bool:
        """Valida los datos del evento antes de guardar"""
        errores = []
        
        # Validar nombre
        nombre = datos.get('nombre', '')
        if not nombre:
            errores.append("El nombre del evento es obligatorio")
        
        # Validar fecha
        fecha = datos.get('fecha', '')
        if not fecha:
            errores.append("La fecha es obligatoria")
        elif fecha:  # Solo validar formato si hay fecha
            try:
                datetime.strptime(fecha, "%d/%m/%Y")
            except ValueError:
                errores.append("La fecha debe tener el formato DD/MM/AAAA")
        
        # Validar hora
        hora = datos.get('hora', '')
        if not hora:
            errores.append("La hora es obligatoria")
        elif hora:  # Solo validar formato si hay hora
            try:
                datetime.strptime(hora, "%H:%M")
            except ValueError:
                errores.append("La hora debe tener el formato HH:MM")
        
        # Validar duración
        duracion_str = datos.get('duracion', '0')
        try:
            duracion = float(duracion_str)
            if duracion <= 0:
                errores.append("La duración debe ser mayor a 0")
        except ValueError:
            # Si no se puede convertir a float, ver si es vacío
            if duracion_str:
                errores.append("La duración debe ser un número válido (ej: 2, 2.5, 1.75)")
            else:
                errores.append("La duración es obligatoria")
        
        # Validar tipo
        tipo = datos.get('tipo', '')
        if not tipo:
            errores.append("El tipo de evento es obligatorio")
        
        # Validar ubicación
        ubicacion = datos.get('ubicacion', '')
        if not ubicacion:
            errores.append("La ubicación es obligatoria")
        
        # Validar capacidad
        capacidad_str = datos.get('capacity', '0')  # Nota: 'capacity' vs 'capacidad'
        try:
            capacidad = int(capacidad_str)
            if capacidad < 0:
                errores.append("La capacidad no puede ser negativa")
            if capacidad > 99354:  # Capacidad máxima del Camp Nou
                errores.append(f"La capacidad no puede exceder 99,354 (capacidad del Camp Nou)")
        except ValueError:
            if capacidad_str:
                errores.append("La capacidad debe ser un número entero válido")
            else:
                errores.append("La capacidad es obligatoria")
        
        # Mostrar errores si hay
        if errores:
            messagebox.showerror("Errores de validación", "\n".join(errores))
            return False
        
        return True
    
    def limpiar_formulario(self):
        """Limpia el formulario de creación de eventos"""
        self.ui.clear_form_fields()
    
    def mostrar_todos_eventos(self):
        """Muestra todos los eventos en la tabla"""
        eventos = self.gestor.obtener_todos_para_ui()
        self.ui.display_events(eventos)
    
    def buscar_eventos(self):
        """Busca eventos según el criterio en la barra de búsqueda"""
        criterio = self.ui.search_var.get().strip()
        
        if not criterio:
            self.mostrar_todos_eventos()
            return
        
        # Buscar por nombre, tipo o ubicación
        eventos_encontrados = []
        eventos_encontrados.extend(self.gestor.buscar_por_nombre(criterio))
        eventos_encontrados.extend(self.gestor.buscar_por_tipo(criterio))
        
        # Convertir a formato para UI
        eventos_ui = [e.to_dict() for e in eventos_encontrados]
        
        if eventos_ui:
            self.ui.display_events(eventos_ui)
        else:
            messagebox.showinfo("Búsqueda", "No se encontraron eventos con ese criterio")
            self.mostrar_todos_eventos()
    
    def ver_detalles_evento(self):
        """Muestra los detalles del evento seleccionado"""
        seleccion = self.ui.events_tree.selection()
        
        if not seleccion:
            messagebox.showwarning("Selección requerida", 
                                  "Por favor, seleccione un evento de la lista")
            return
        
        # Obtener el evento seleccionado
        item = self.ui.events_tree.item(seleccion[0])
        nombre_evento = item['values'][0]
        
        # Buscar el evento
        eventos = self.gestor.buscar_por_nombre(nombre_evento)
        if eventos:
            evento = eventos[0]  # Tomar el primero encontrado
            
            # Crear ventana de detalles
            from tkinter import Toplevel, Label, Frame, Text, Button
            import tkinter.font as tkFont
            
            detalles_ventana = Toplevel(self.ui.root)
            detalles_ventana.title(f"Detalles: {evento.nombre}")
            detalles_ventana.geometry("600x500")
            detalles_ventana.configure(bg="white")
            
            # Título
            titulo_font = tkFont.Font(family="Arial", size=16, weight="bold")
            Label(detalles_ventana, text=evento.nombre, 
                  font=titulo_font, bg="white", fg="#004D98").pack(pady=20)
            
            # Frame para detalles
            frame_detalles = Frame(detalles_ventana, bg="white")
            frame_detalles.pack(fill="both", expand=True, padx=30)
            
            # Información del evento
            info = [
                ("📅 Fecha:", evento.fecha),
                ("⏰ Hora:", f"{evento.hora} - {evento.hora_fin}"),
                ("⏱️ Duración:", f"{evento.duracion} horas"),
                ("🏷️ Tipo:", evento.tipo),
                ("📍 Ubicación:", evento.ubicacion),
                ("👥 Capacidad:", f"{evento.capacidad:,} personas"),
                ("📊 Estado:", evento.estado.upper()),
                ("💰 Precio Base:", f"€{evento.precio_base:.2f}"),
                ("👤 Organizador:", evento.organizador)
            ]
            
            for etiqueta, valor in info:
                frame_info = Frame(frame_detalles, bg="white")
                frame_info.pack(fill="x", pady=5)
                
                Label(frame_info, text=etiqueta, font=("Arial", 11, "bold"),
                      bg="white", width=15, anchor="w").pack(side="left")
                Label(frame_info, text=valor, font=("Arial", 11),
                      bg="white").pack(side="left", padx=(10, 0))
            
            # Descripción
            Label(frame_detalles, text="📝 Descripción:", font=("Arial", 11, "bold"),
                  bg="white", anchor="w").pack(anchor="w", pady=(20, 5))
            
            texto_desc = Text(frame_detalles, height=6, width=60, 
                             font=("Arial", 11), wrap="word")
            texto_desc.pack(fill="x", pady=(0, 10))
            texto_desc.insert("1.0", evento.descripcion or "Sin descripción")
            texto_desc.config(state="disabled")
            
            # Botón cerrar
            Button(detalles_ventana, text="Cerrar", 
                   command=detalles_ventana.destroy,
                   bg="#004D98", fg="white",
                   font=("Arial", 11, "bold"),
                   padx=20, pady=5).pack(pady=20)
    
    def eliminar_evento(self):
        """Elimina el evento seleccionado"""
        seleccion = self.ui.events_tree.selection()
        
        if not seleccion:
            messagebox.showwarning("Selección requerida",
                                  "Por favor, seleccione un evento de la lista")
            return
        
        # Obtener el evento seleccionado
        item = self.ui.events_tree.item(seleccion[0])
        nombre_evento = item['values'][0]
        
        # Buscar el evento
        eventos = self.gestor.buscar_por_nombre(nombre_evento)
        if not eventos:
            messagebox.showerror("Error", "Evento no encontrado")
            return
        
        evento = eventos[0]
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar el evento '{evento.nombre}'?"
        )
        
        if confirmacion:
            if self.gestor.eliminar_evento(evento.id):
                messagebox.showinfo("Eliminado", 
                                  f"Evento '{evento.nombre}' eliminado exitosamente")
                self.mostrar_todos_eventos()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el evento")
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas en la UI"""
        try:
            stats = self.gestor.obtener_estadisticas()
            
            # Preparar datos para la UI
            datos_stats = {
                'total_events': str(stats['total_eventos']),
                'upcoming_events': str(stats['eventos_proximos']),
                'total_capacity': f"{stats['capacidad_total']:,}",
                'most_common_type': stats['tipo_mas_comun'],
                'type_distribution': stats['tipos_eventos']
            }
            
            # Actualizar UI
            self.ui.update_statistics(datos_stats)
            
        except Exception as e:
            print(f"Error al actualizar estadísticas: {e}")