Organizador de Eventos - Camp Nou📌 
Descripción general
Este proyecto es una aplicación de escritorio desarrollada en Python que permite gestionar eventos en el estadio Camp Nou. Combina una interfaz gráfica intuitiva con lógica de validación y almacenamiento persistente en archivos JSON, ofreciendo herramientas para crear, visualizar, analizar y exportar eventos.El sistema está diseñado para ser modular:UI Visual: interfaz gráfica construida con Tkinter y ttk.Controlador: conecta la interfaz con la lógica de negocio.Gestor de eventos: maneja la creación, almacenamiento, búsqueda y exportación de eventos.

Funcionalidades principales
Creación de eventos: formulario con validación de nombre, fecha, hora, duración, tipo, ubicación, capacidad y descripción.Visualización: tabla interactiva con búsqueda y filtros, además de detalles completos de cada evento.Estadísticas: métricas como total de eventos, próximos eventos, capacidad total, tipo más común e ingresos estimados.Gestión completa: creación, búsqueda, visualización detallada, actualización y eliminación de eventos.Exportación a CSV: exporta todos los eventos para análisis externo.Persistencia: almacenamiento automático en events_data.json.

Librerías utilizadas
El proyecto se apoya únicamente en librerías estándar de Python:Tkinter / ttk → interfaz gráfica.tkinter.messagebox → mensajes de validación y confirmación.datetime / timedelta → manejo de fechas y horas.json / os → almacenamiento persistente en archivos JSON.csv → exportación de eventos.re → generación de IDs únicos.typing → anotaciones de tipos.No requiere instalación de librerías externas.

Instalación
Instalar Python 3.x.Clonar o descargar este repositorio.No es necesario instalar dependencias externas, ya que todas las librerías usadas son parte de la biblioteca estándar de Python.

Uso paso a paso
Ejecuta el archivo main.py.Se abrirá la interfaz gráfica con tres pestañas:➕ Crear Evento → formulario para ingresar datos.📅 Ver Eventos → tabla interactiva con búsqueda y filtros.📊 Estadísticas → métricas y distribución de eventos.Los eventos se guardan automáticamente en events_data.json.Desde el gestor de eventos, puedes exportar todos los datos a CSV (eventos_exportados.csv).


Estructura del proyecto
main.py → punto de entrada, inicializa la interfaz gráfica.ui_visual.py → clase EventOrganizerUI, define la interfaz gráfica con pestañas y formularios.controller.py → clase ControladorEventos, conecta la interfaz con la lógica de gestión, validando datos y actualizando estadísticas.events.py → clase Evento y GestorEventos, maneja la creación, almacenamiento, búsqueda, eliminación y exportación de eventos.events_data.json → archivo de datos donde se guardan los eventos creados.

Ejemplo de flujo de trabajo
Crear un evento desde la pestaña ➕ Crear Evento.Visualizarlo en la pestaña 📅 Ver Eventos.Consultar estadísticas en 📊 Estadísticas.Exportar los eventos a CSV para análisis externo.

Extensibilidad
El proyecto está diseñado para ser fácilmente ampliable:Se pueden añadir nuevos tipos de eventos en la lista TIPOS_EVENTO.Se pueden definir más ubicaciones en UBICACIONES_CAMP_NOU.El gestor permite implementar nuevas funciones de filtrado o reportes.
