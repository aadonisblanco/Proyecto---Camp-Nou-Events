
from datetime import datetime

#Clase para los eventos del estadio
class Event:
    #Diferentes eventos posibles
    Events = ["Partido oficial", "Partido amistoso", "Concierto", "Entrenamiento"
              "Galas benéfica", "Tour por el museo del club",
              "Obras de construcción", "Limpieza y mantenimiento del césped y gradas"]
    
    def __init__(self, type, name, date, duration, space, resources):
        if type not in Event.Events:
            raise ValueError(f"Tipo de evento inválido.")
        self.type = type
        self.name = name
        self.date = date
        self.duration = duration
        self.space = space
        self.resources = resources if resources else[]
    def __str__(self):
        return (f"[{self.type}] {self.name} - {self.date} - {self.duration}hrs - {self.space}")
    
    def Duration(a):
        pass
    
    def Space(a):
        pass