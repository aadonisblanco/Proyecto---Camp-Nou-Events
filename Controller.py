class EventController:
    def __init__(self, ui, event_manager):
        self.ui = ui
        self.event_manager = event_manager
        
        # Conectar botones UI a métodos del controlador
        self.ui.save_button.config(command=self.save_event)
        self.ui.clear_button.config(command=self.clear_form)
        # ... etc