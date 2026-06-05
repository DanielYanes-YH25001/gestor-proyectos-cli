from models.proyecto import Proyecto

class ProyectoService:
  def __init__(self, manejador_persistencia):
    self.manejador_persistencia = manejador_persistencia

  def _cargar(self):
    return self.manejador_persistencia.cargar_datos()

  def _guardar(self, datos):
    self.manejador_persistencia.guardar_datos(datos)

  def crear(self, nombre, estado="Activo"):
    datos = self._cargar()
    nuevo_id = self.manejador_persistencia.obtener_proximo_id(datos["proyectos"])
    proyecto = Proyecto(nuevo_id, nombre, estado)
    datos["proyectos"].append(proyecto.to_dict())
    self._guardar(datos)
    return proyecto

  def obtener_todos(self):
    datos = self._cargar()
    return [Proyecto.from_dict(p) for p in datos["proyectos"]]

  def obtener_por_id(self, id_proyecto):
    datos = self._cargar()
    proyecto = next((p for p in datos["proyectos"] if p["id"] == id_proyecto), None)
    return Proyecto.from_dict(proyecto) if proyecto else None

  def actualizar(self, id_proyecto, nombre=None, estado=None):
    datos = self._cargar()
    proyecto = next((p for p in datos["proyectos"] if p["id"] == id_proyecto), None)
    if not proyecto:
      return False

    if nombre is not None:
      if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre del proyecto debe ser una cadena no vacía.")
      proyecto["nombre"] = nombre.strip()

    if estado is not None:
      if estado not in {"Activo", "Finalizado", "Pausado"}:
        raise ValueError("El estado del proyecto debe ser 'Activo', 'Finalizado' o 'Pausado'.")
      proyecto["estado"] = estado

    self._guardar(datos)
    return True

  def eliminar(self, id_proyecto):
    datos = self._cargar()
    proyecto = next((p for p in datos["proyectos"] if p["id"] == id_proyecto), None)
    if not proyecto:
      return False

    datos["tareas"] = [t for t in datos["tareas"] if t["id_proyecto"] != id_proyecto]
    datos["asignaciones"] = [
      a for a in datos["asignaciones"]
      if a["id_tarea"] not in [t["id"] for t in datos["tareas"]]
    ]
    datos["proyectos"] = [p for p in datos["proyectos"] if p["id"] != id_proyecto]

    self._guardar(datos)
    return True