#ui visual
import tkinter as tk
from tkinter import ttk

class EventOrganizerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Eventos - Camp Nou")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables para los datos del eventocz
        self.event_name_var = tk.StringVar()
        self.event_date_var = tk.StringVar()
        self.event_time_var = tk.StringVar()
        self.event_duration_var = tk.StringVar()
        self.event_type_var = tk.StringVar()
        self.event_location_var = tk.StringVar()
        self.event_description_var = tk.StringVar()
        self.event_capacity_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        # Variables para estadísticas
        self.total_events_var = tk.StringVar(value="0")
        self.upcoming_events_var = tk.StringVar(value="0")
        self.total_capacity_var = tk.StringVar(value="0")
        self.most_common_type_var = tk.StringVar(value="N/A")
        
        # Configurar la interfaz
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título principal
        title_frame = tk.Frame(main_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="🏟️ ORGANIZADOR DE EVENTOS - CAMP NOU", 
                font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#004D98").pack()
        tk.Label(title_frame, text="Gestiona todos los eventos del estadio", 
                font=("Arial", 12), bg="#f0f0f0", fg="#666").pack()
        
        # Crear pestañas
        tab_control = ttk.Notebook(main_frame)
        
        # Pestaña 1: Crear evento
        self.create_tab = ttk.Frame(tab_control)
        tab_control.add(self.create_tab, text="➕ Crear Evento")
        
        # Pestaña 2: Ver eventos
        self.view_tab = ttk.Frame(tab_control)
        tab_control.add(self.view_tab, text="📅 Ver Eventos")
        
        # Pestaña 3: Estadísticas
        self.stats_tab = ttk.Frame(tab_control)
        tab_control.add(self.stats_tab, text="📊 Estadísticas")
        
        tab_control.pack(expand=1, fill=tk.BOTH)
        
        # Configurar cada pestaña
        self.setup_create_tab()
        self.setup_view_tab()
        self.setup_stats_tab()
        
    def setup_create_tab(self):
        # Frame principal para el formulario
        form_frame = tk.Frame(self.create_tab, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título del formulario
        tk.Label(form_frame, text="NUEVO EVENTO", font=("Arial", 18, "bold"), 
                bg="white", fg="#004D98").pack(pady=(10, 20))
        
        # Frame para los campos del formulario (2 columnas)
        fields_frame = tk.Frame(form_frame, bg="white")
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Columna izquierda
        left_column = tk.Frame(fields_frame, bg="white")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna derecha
        right_column = tk.Frame(fields_frame, bg="white")
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Campos del formulario - Columna izquierda
        self.create_form_field(left_column, "Nombre del Evento:", self.event_name_var, "Ej: Partido de Liga", 0)
        self.create_form_field(left_column, "Fecha (DD/MM/AAAA):", self.event_date_var, "Ej: 15/12/2024", 1)
        self.create_form_field(left_column, "Hora (HH:MM):", self.event_time_var, "Ej: 21:00", 2)
        self.create_form_field(left_column, "Duración (horas):", self.event_duration_var, "Ej: 2.5", 3)
        self.create_form_field(left_column, "Ubicación:", self.event_location_var, "Ej: Tribuna Principal", 4)
        
        # Campos del formulario - Columna derecha
        self.create_form_field(right_column, "Tipo de Evento:", self.event_type_var, "Ej: Partido, Concierto, etc.", 0)
        
        # Capacidad
        tk.Label(right_column, text="Capacidad estimada:", font=("Arial", 10, "bold"), 
                bg="white", anchor="w").grid(row=2, column=0, sticky="w", pady=(15, 5))
        
        capacity_frame = tk.Frame(right_column, bg="white")
        capacity_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        tk.Entry(capacity_frame, textvariable=self.event_capacity_var, 
                font=("Arial", 11), width=20).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(capacity_frame, text="personas", bg="white", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Descripción (área de texto)
        tk.Label(right_column, text="Descripción:", font=("Arial", 10, "bold"),
                bg="white", anchor="w").grid(row=4, column=0, sticky="w", pady=(15, 5))
        
        desc_frame = tk.Frame(right_column, bg="white", height=100)
        desc_frame.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        desc_frame.grid_propagate(False)
        
        self.desc_text = tk.Text(desc_frame, font=("Arial", 11), height=5, width=40)
        self.desc_text.pack(fill=tk.BOTH, expand=True)
        
        # Botones de acción (con placeholders para funciones)
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=20)
        
        self.save_button = tk.Button(button_frame, text="Guardar Evento",
                 bg="#004D98", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=10, cursor="hand2")
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        self.clear_button = tk.Button(button_frame, text="Limpiar Formulario",
                 bg="#A50044", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=10, cursor="hand2")
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        self.exit_button = tk.Button(button_frame, text="Salir", command=self.root.quit,
                 bg="#666", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=10, cursor="hand2")
        self.exit_button.pack(side=tk.RIGHT, padx=10)
        
    def create_form_field(self, parent, label_text, variable, placeholder, row):
        """Crea un campo del formulario con etiqueta y entrada"""
        tk.Label(parent, text=label_text, font=("Arial", 10, "bold"), 
                bg="white", anchor="w").grid(row=row*2, column=0, sticky="w", pady=(15, 5))
        
        entry = tk.Entry(parent, textvariable=variable, font=("Arial", 11), width=30)
        entry.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 15))
        
        # Mostrar placeholder
        entry.insert(0, placeholder)
        entry.config(fg="grey")
        
        # Funciones para manejar el placeholder
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")
                
        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="grey")
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
    def setup_view_tab(self):
        # Frame principal
        main_frame = tk.Frame(self.view_tab, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        tk.Label(main_frame, text="EVENTOS PROGRAMADOS", font=("Arial", 18, "bold"), 
                bg="white", fg="#004D98").pack(pady=(10, 20))
        
        # Barra de búsqueda y filtros
        search_frame = tk.Frame(main_frame, bg="white")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Buscar:", bg="white", 
                font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                               font=("Arial", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        self.search_button = tk.Button(search_frame, text="Buscar",
                 bg="#004D98", fg="white", font=("Arial", 10, "bold"),
                 padx=15)
        self.search_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.show_all_button = tk.Button(search_frame, text="Mostrar Todos",
                 bg="#A50044", fg="white", font=("Arial", 10, "bold"),
                 padx=15)
        self.show_all_button.pack(side=tk.LEFT)
        
        # Frame para la tabla de eventos
        table_frame = tk.Frame(main_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview para mostrar eventos
        columns = ("Nombre", "Fecha", "Hora", "Tipo", "Ubicación", "Capacidad")
        self.events_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.events_tree.heading(col, text=col)
            self.events_tree.column(col, width=120)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.events_tree.yview)
        self.events_tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar widgets
        self.events_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción para eventos seleccionados
        action_frame = tk.Frame(main_frame, bg="white")
        action_frame.pack(fill=tk.X, pady=10)
        
        self.view_details_button = tk.Button(action_frame, text="Ver Detalles",
                 bg="#004D98", fg="white", font=("Arial", 10, "bold"),
                 padx=15)
        self.view_details_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_event_button = tk.Button(action_frame, text="Eliminar Evento",
                 bg="#A50044", fg="white", font=("Arial", 10, "bold"),
                 padx=15)
        self.delete_event_button.pack(side=tk.LEFT, padx=5)
        
    def setup_stats_tab(self):
        # Frame principal
        main_frame = tk.Frame(self.stats_tab, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        tk.Label(main_frame, text="ESTADÍSTICAS DE EVENTOS", font=("Arial", 18, "bold"), 
                bg="white", fg="#004D98").pack(pady=(10, 20))
        
        # Frame para estadísticas
        stats_frame = tk.Frame(main_frame, bg="white")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Estadísticas en tarjetas
        cards_frame = tk.Frame(stats_frame, bg="white")
        cards_frame.pack(fill=tk.X, pady=10)
        
        # Crear tarjetas de estadísticas
        self.create_stat_card(cards_frame, "Total Eventos", self.total_events_var, "#004D98", 0)
        self.create_stat_card(cards_frame, "Próximos Eventos", self.upcoming_events_var, "#A50044", 1)
        self.create_stat_card(cards_frame, "Capacidad Total", self.total_capacity_var, "#004D98", 2)
        self.create_stat_card(cards_frame, "Tipo Más Común", self.most_common_type_var, "#A50044", 3)
        
        # Gráfico de tipos de eventos (simulado con etiquetas)
        tk.Label(stats_frame, text="Distribución por Tipo de Evento", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=(30, 10))
        
        chart_frame = tk.Frame(stats_frame, bg="white", height=200)
        chart_frame.pack(fill=tk.X, pady=10)
        chart_frame.pack_propagate(False)
        
        # Aquí iría un gráfico real, por ahora mostramos texto
        self.chart_label = tk.Label(chart_frame, text="Gráfico de distribución aparecerá aquí", 
                                   font=("Arial", 12), bg="white", fg="#666")
        self.chart_label.pack(expand=True)
        
        # Botón para actualizar estadísticas
        self.update_stats_button = tk.Button(stats_frame, text="Actualizar Estadísticas",
                 bg="#004D98", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=10, cursor="hand2")
        self.update_stats_button.pack(pady=20)
        
    def create_stat_card(self, parent, title, value_var, color, column):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        card.grid(row=0, column=column, padx=10, sticky="nsew")
        
        # Configurar grid para expandirse
        parent.grid_columnconfigure(column, weight=1)
        
        # Contenido de la tarjeta
        tk.Label(card, text=title, font=("Arial", 12, "bold"), 
                bg=color, fg="white").pack(pady=(10, 5))
        
        tk.Label(card, textvariable=value_var, font=("Arial", 24, "bold"), 
                bg=color, fg="white").pack(pady=(5, 10))
        
        card.config(width=150, height=100)
        
    def clear_form_fields(self):
        """Limpia todos los campos del formulario"""
        # Esta función se conectará a la lógica del controlador
        pass
        
    def get_form_data(self):
        """Obtiene los datos del formulario como diccionario"""
        # Función para limpiar y convertir valores
        def procesar_valor(valor, placeholder, es_numero=False):
            # Si es igual al placeholder, devolver vacío/cero
            if valor == placeholder:
                return "" if not es_numero else "0"
            
            # Limpiar espacios
            valor = valor.strip()
            
            # Si es número y está vacío, devolver cero
            if es_numero and not valor:
                return "0"
                
            return valor
        
        # Diccionario de placeholders exactos
        placeholders = {
            'nombre': 'Ej: Partido de Liga',
            'fecha': 'Ej: 15/12/2024', 
            'hora': 'Ej: 21:00',
            'duracion': 'Ej: 2.5',
            'tipo': 'Ej: Partido, Concierto, etc.',
            'ubicacion': 'Ej: Tribuna Principal'
        }
        
        # Procesar cada campo
        nombre = procesar_valor(self.event_name_var.get(), placeholders['nombre'])
        fecha = procesar_valor(self.event_date_var.get(), placeholders['fecha'])
        hora = procesar_valor(self.event_time_var.get(), placeholders['hora'])
        duracion = procesar_valor(self.event_duration_var.get(), placeholders['duracion'], es_numero=True)
        tipo = procesar_valor(self.event_type_var.get(), placeholders['tipo'])
        ubicacion = procesar_valor(self.event_location_var.get(), placeholders['ubicacion'])
        capacidad = self.event_capacity_var.get().strip()
        descripcion = self.desc_text.get("1.0", tk.END).strip()
        
        # Convertir capacidad vacía a "0"
        if not capacidad:
            capacidad = "0"
        
        return {
            "nombre": nombre,
            "fecha": fecha,
            "hora": hora,
            "duracion": duracion,
            "tipo": tipo,
            "ubicacion": ubicacion,
            "descripcion": descripcion,
            "capacidad": capacidad
        }
        
    def display_events(self, events_list):
        """Muestra la lista de eventos en el Treeview"""
        # Limpiar lista actual
        for item in self.events_tree.get_children():
            self.events_tree.delete(item)
        
        # Agregar eventos a la lista
        for event in events_list:
            self.events_tree.insert("", tk.END, values=(
                event.get("name", ""),
                event.get("date", ""),
                event.get("time", ""),
                event.get("type", ""),
                event.get("location", ""),
                event.get("capacity", "")
            ))
            
    def update_statistics(self, stats_dict):
        """Actualiza las estadísticas mostradas"""
        self.total_events_var.set(stats_dict.get("total_events", "0"))
        self.upcoming_events_var.set(stats_dict.get("upcoming_events", "0"))
        self.total_capacity_var.set(stats_dict.get("total_capacity", "0"))
        self.most_common_type_var.set(stats_dict.get("most_common_type", "N/A"))
        
        # Actualizar gráfico (simulado)
        if "type_distribution" in stats_dict:
            chart_text = "Distribución:\n"
            for t, count in stats_dict["type_distribution"].items():
                chart_text += f"{t}: {count} eventos\n"
            self.chart_label.config(text=chart_text)

# Punto de entrada para probar solo la interfaz visual
if __name__ == "__main__":
    root = tk.Tk()
    app = EventOrganizerUI(root)
    root.mainloop()