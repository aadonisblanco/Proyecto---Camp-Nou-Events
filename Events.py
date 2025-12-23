# events.py
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import re

class Evento:
    """Clase que representa un evento en el Camp Nou"""
    
    def __init__(self, **kwargs):
        """
        Inicializa un nuevo evento
        
        Args:
            nombre (str): Nombre del evento
            fecha (str): Fecha en formato DD/MM/AAAA
            hora (str): Hora en formato HH:MM
            duracion (float): Duración en horas
            tipo (str): Tipo de evento (Partido, Concierto, etc.)
            ubicacion (str): Ubicación dentro del Camp Nou
            descripcion (str): Descripción detallada
            capacidad (int): Capacidad estimada
            estado (str): Estado del evento (programado, en_curso, finalizado, cancelado)
            precio_base (float): Precio base de entrada (opcional)
            organizador (str): Organizador del evento (opcional)
        """
        self.nombre = kwargs.get('nombre', '')
        self.fecha = kwargs.get('fecha', '')
        self.hora = kwargs.get('hora', '')
        self.duracion = float(kwargs.get('duracion', 2.0))
        self.tipo = kwargs.get('tipo', 'Partido')
        self.ubicacion = kwargs.get('ubicacion', 'Tribuna Principal')
        self.descripcion = kwargs.get('descripcion', '')
        self.capacidad = int(kwargs.get('capacidad', 0))
        self.estado = kwargs.get('estado', 'programado')
        self.precio_base = float(kwargs.get('precio_base', 0.0))
        self.organizador = kwargs.get('organizador', 'FC Barcelona')
        
        # Generar ID único
        self.id = self._generar_id()
        self.fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def _generar_id(self) -> str:
        """Genera un ID único para el evento"""
        nombre_limpio = re.sub(r'[^a-zA-Z0-9]', '', self.nombre)[:10].lower()
        fecha_limpia = self.fecha.replace('/', '')
        return f"{nombre_limpio}_{fecha_limpia}_{self.hora.replace(':', '')}"
    
    @property
    def hora_fin(self) -> str:
        """Calcula la hora de finalización del evento"""
        try:
            hora_inicio = datetime.strptime(self.hora, "%H:%M")
            hora_fin = hora_inicio + timedelta(hours=self.duracion)
            return hora_fin.strftime("%H:%M")
        except:
            return ""
    
    @property
    def fecha_hora_inicio(self) -> Optional[datetime]:
        """Devuelve la fecha y hora de inicio como objeto datetime"""
        try:
            return datetime.strptime(f"{self.fecha} {self.hora}", "%d/%m/%Y %H:%M")
        except:
            return None
    
    @property
    def fecha_hora_fin(self) -> Optional[datetime]:
        """Devuelve la fecha y hora de fin como objeto datetime"""
        try:
            inicio = self.fecha_hora_inicio
            if inicio:
                return inicio + timedelta(hours=self.duracion)
        except:
            return None
        return None
    
    @property
    def es_proximo(self) -> bool:
        """Verifica si el evento está próximo (en las próximas 48 horas)"""
        try:
            inicio = self.fecha_hora_inicio
            if inicio:
                ahora = datetime.now()
                diferencia = inicio - ahora
                return timedelta(hours=0) < diferencia <= timedelta(hours=48)
        except:
            return False
        return False
    
    @property
    def es_hoy(self) -> bool:
        """Verifica si el evento es hoy"""
        try:
            hoy = datetime.now().strftime("%d/%m/%Y")
            return self.fecha == hoy
        except:
            return False
    
    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado del evento"""
        estados_validos = ['programado', 'en_curso', 'finalizado', 'cancelado']
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
            return True
        return False
    
    def actualizar_capacidad(self, nueva_capacidad: int) -> bool:
        """Actualiza la capacidad del evento"""
        if nueva_capacidad >= 0:
            self.capacidad = nueva_capacidad
            return True
        return False
    
    def obtener_ingresos_estimados(self) -> float:
        """Calcula los ingresos estimados del evento"""
        tasa_ocupacion = 0.8  # Suponemos 80% de ocupación
        return self.capacidad * tasa_ocupacion * self.precio_base
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el evento a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha': self.fecha,
            'hora': self.hora,
            'duracion': self.duracion,
            'tipo': self.tipo,
            'ubicacion': self.ubicacion,
            'descripcion': self.descripcion,
            'capacidad': self.capacidad,
            'estado': self.estado,
            'precio_base': self.precio_base,
            'organizador': self.organizador,
            'fecha_creacion': self.fecha_creacion
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Evento':
        """Crea un Evento desde un diccionario"""
        return cls(**data)
    
    def __str__(self) -> str:
        return f"{self.nombre} - {self.fecha} {self.hora} ({self.tipo})"
    
    def __repr__(self) -> str:
        return f"<Evento {self.id}: {self.nombre}>"


class GestorEventos:
    """Clase que gestiona todos los eventos del Camp Nou"""
    
    def __init__(self, archivo_datos: str = "events_data.json"):
        self.archivo_datos = archivo_datos
        self.eventos: List[Evento] = []
        self.cargar_eventos()
    
    def cargar_eventos(self) -> bool:
        """Carga los eventos desde el archivo JSON"""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.eventos = [Evento.from_dict(evento) for evento in datos]
                print(f"✓ Cargados {len(self.eventos)} eventos desde {self.archivo_datos}")
                return True
            else:
                print(f"⚠ Archivo {self.archivo_datos} no encontrado. Se creará uno nuevo.")
                return True
        except Exception as e:
            print(f"✗ Error al cargar eventos: {e}")
            return False
    
    def guardar_eventos(self) -> bool:
        """Guarda los eventos en el archivo JSON"""
        try:
            datos = [evento.to_dict() for evento in self.eventos]
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            print(f"✓ Guardados {len(self.eventos)} eventos en {self.archivo_datos}")
            return True
        except Exception as e:
            print(f"✗ Error al guardar eventos: {e}")
            return False
    
    def agregar_evento(self, evento: Evento) -> bool:
        """Agrega un nuevo evento a la lista"""
        # Verificar que no haya conflictos de horario
        if self.verificar_conflicto_horario(evento):
            print(f"✗ Conflicto de horario para el evento: {evento.nombre}")
            return False
        
        self.eventos.append(evento)
        self.guardar_eventos()
        print(f"✓ Evento agregado: {evento.nombre}")
        return True
    
    def crear_evento(self, **kwargs) -> Optional[Evento]:
        """Crea y agrega un nuevo evento"""
        try:
            evento = Evento(**kwargs)
            if self.agregar_evento(evento):
                return evento
            return None
        except Exception as e:
            print(f"✗ Error al crear evento: {e}")
            return None
    
    def eliminar_evento(self, evento_id: str) -> bool:
        """Elimina un evento por su ID"""
        evento = self.buscar_por_id(evento_id)
        if evento:
            self.eventos.remove(evento)
            self.guardar_eventos()
            print(f"✓ Evento eliminado: {evento.nombre}")
            return True
        print(f"✗ Evento con ID {evento_id} no encontrado")
        return False
    
    def buscar_por_id(self, evento_id: str) -> Optional[Evento]:
        """Busca un evento por su ID"""
        for evento in self.eventos:
            if evento.id == evento_id:
                return evento
        return None
    
    def buscar_por_nombre(self, nombre: str) -> List[Evento]:
        """Busca eventos por nombre (búsqueda parcial)"""
        nombre = nombre.lower()
        return [e for e in self.eventos if nombre in e.nombre.lower()]
    
    def buscar_por_tipo(self, tipo: str) -> List[Evento]:
        """Busca eventos por tipo"""
        tipo = tipo.lower()
        return [e for e in self.eventos if tipo == e.tipo.lower()]
    
    def buscar_por_fecha(self, fecha: str) -> List[Evento]:
        """Busca eventos por fecha"""
        return [e for e in self.eventos if e.fecha == fecha]
    
    def buscar_por_estado(self, estado: str) -> List[Evento]:
        """Busca eventos por estado"""
        return [e for e in self.eventos if e.estado == estado]
    
    def obtener_eventos_proximos(self) -> List[Evento]:
        """Obtiene los eventos próximos (próximas 48 horas)"""
        return [e for e in self.eventos if e.es_proximo]
    
    def obtener_eventos_de_hoy(self) -> List[Evento]:
        """Obtiene los eventos de hoy"""
        return [e for e in self.eventos if e.es_hoy]
    
    def obtener_eventos_por_mes(self, año: int, mes: int) -> List[Evento]:
        """Obtiene los eventos de un mes específico"""
        eventos_mes = []
        for evento in self.eventos:
            try:
                fecha_evento = datetime.strptime(evento.fecha, "%d/%m/%Y")
                if fecha_evento.year == año and fecha_evento.month == mes:
                    eventos_mes.append(evento)
            except:
                continue
        return eventos_mes
    
    def verificar_conflicto_horario(self, nuevo_evento: Evento) -> bool:
        """Verifica si hay conflictos de horario con eventos existentes"""
        if not nuevo_evento.fecha_hora_inicio or not nuevo_evento.fecha_hora_fin:
            return False
        
        for evento_existente in self.eventos:
            if (evento_existente.fecha_hora_inicio and evento_existente.fecha_hora_fin and
                nuevo_evento.fecha_hora_inicio < evento_existente.fecha_hora_fin and
                nuevo_evento.fecha_hora_fin > evento_existente.fecha_hora_inicio):
                return True
        return False
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Genera estadísticas de los eventos"""
        total_eventos = len(self.eventos)
        eventos_programados = len(self.buscar_por_estado('programado'))
        eventos_en_curso = len(self.buscar_por_estado('en_curso'))
        eventos_finalizados = len(self.buscar_por_estado('finalizado'))
        eventos_cancelados = len(self.buscar_por_estado('cancelado'))
        
        # Conteo por tipo
        tipos = {}
        for evento in self.eventos:
            tipos[evento.tipo] = tipos.get(evento.tipo, 0) + 1
        
        # Tipo más común
        tipo_mas_comun = max(tipos, key=tipos.get) if tipos else "N/A"
        
        # Capacidad total
        capacidad_total = sum(evento.capacidad for evento in self.eventos)
        
        # Ingresos estimados totales
        ingresos_totales = sum(evento.obtener_ingresos_estimados() 
                              for evento in self.eventos)
        
        # Próximos eventos
        eventos_proximos = len(self.obtener_eventos_proximos())
        
        return {
            'total_eventos': total_eventos,
            'eventos_programados': eventos_programados,
            'eventos_en_curso': eventos_en_curso,
            'eventos_finalizados': eventos_finalizados,
            'eventos_cancelados': eventos_cancelados,
            'tipos_eventos': tipos,
            'tipo_mas_comun': tipo_mas_comun,
            'capacidad_total': capacidad_total,
            'ingresos_totales': ingresos_totales,
            'eventos_proximos': eventos_proximos
        }
    
    def obtener_todos_para_ui(self) -> List[Dict[str, Any]]:
        """Obtiene todos los eventos en formato para la UI"""
        return [evento.to_dict() for evento in self.eventos]
    
    def filtrar_eventos(self, criterio: str, valor: str) -> List[Dict[str, Any]]:
        """Filtra eventos según criterio"""
        eventos_filtrados = []
        
        criterio = criterio.lower()
        valor = valor.lower()
        
        for evento in self.eventos:
            if criterio == 'nombre' and valor in evento.nombre.lower():
                eventos_filtrados.append(evento.to_dict())
            elif criterio == 'tipo' and valor == evento.tipo.lower():
                eventos_filtrados.append(evento.to_dict())
            elif criterio == 'fecha' and valor == evento.fecha:
                eventos_filtrados.append(evento.to_dict())
            elif criterio == 'ubicacion' and valor in evento.ubicacion.lower():
                eventos_filtrados.append(evento.to_dict())
            elif criterio == 'estado' and valor == evento.estado:
                eventos_filtrados.append(evento.to_dict())
        
        return eventos_filtrados
    
    def actualizar_evento(self, evento_id: str, **kwargs) -> bool:
        """Actualiza un evento existente"""
        evento = self.buscar_por_id(evento_id)
        if not evento:
            return False
        
        # Actualizar solo los campos proporcionados
        for key, value in kwargs.items():
            if hasattr(evento, key):
                setattr(evento, key, value)
        
        self.guardar_eventos()
        print(f"✓ Evento actualizado: {evento.nombre}")
        return True
    
    def exportar_a_csv(self, archivo_salida: str = "eventos_exportados.csv") -> bool:
        """Exporta todos los eventos a un archivo CSV"""
        try:
            import csv
            
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Escribir encabezados
                writer.writerow([
                    'ID', 'Nombre', 'Fecha', 'Hora', 'Duración', 'Tipo',
                    'Ubicación', 'Capacidad', 'Estado', 'Precio Base',
                    'Organizador', 'Fecha Creación'
                ])
                
                # Escribir datos
                for evento in self.eventos:
                    writer.writerow([
                        evento.id, evento.nombre, evento.fecha, evento.hora,
                        evento.duracion, evento.tipo, evento.ubicacion,
                        evento.capacidad, evento.estado, evento.precio_base,
                        evento.organizador, evento.fecha_creacion
                    ])
            
            print(f"✓ Eventos exportados a {archivo_salida}")
            return True
            
        except Exception as e:
            print(f"✗ Error al exportar a CSV: {e}")
            return False


# Tipos de eventos predefinidos para el Camp Nou
TIPOS_EVENTO = [
    "Partido de Liga",
    "Partido de Champions",
    "Partido de Copa",
    "Concierto",
    "Evento Corporativo",
    "Visita Guiada",
    "Evento Deportivo",
    "Presentación",
    "Gala",
    "Otro"
]

# Ubicaciones disponibles en el Camp Nou
UBICACIONES_CAMP_NOU = [
    "Tribuna Principal",
    "Gol Norte",
    "Gol Sur",
    "Palco VIP",
    "Zona Mixta",
    "Sala de Prensa",
    "Museo FC Barcelona",
    "Tienda Oficial",
    "Restaurante",
    "Zona de Entrenamiento"
]

    
    