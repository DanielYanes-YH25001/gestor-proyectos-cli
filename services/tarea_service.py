from models.tarea import Tarea

class TareaService:
  def __init__(self, manejador_persistencia):
    self.manejador_persistencia = manejador_persistencia

  def _cargar(self):
    return self.manejador_persistencia.cargar_datos()

  def _guardar(self, datos):
    self.manejador_persistencia.guardar_datos(datos)

  def crear(self, id_proyecto, descripcion):
    datos = self._cargar()
    nuevo_id = self.manejador_persistencia.obtener_proximo_id(datos["tareas"])
    tarea = Tarea(nuevo_id, id_proyecto, descripcion)
    datos["tareas"].append(tarea.to_dict())
    self._guardar(datos)
    return tarea

  def obtener_todos(self):
    datos = self._cargar()
    return [Tarea.from_dict(t) for t in datos["tareas"]]

  def obtener_por_id(self, id_tarea):
    datos = self._cargar()
    tarea = next((t for t in datos["tareas"] if t["id"] == id_tarea), None)
    return Tarea.from_dict(tarea) if tarea else None

  def obtener_por_proyecto(self, id_proyecto):
    datos = self._cargar()
    return [
      Tarea.from_dict(t)
      for t in datos["tareas"]
      if t["id_proyecto"] == id_proyecto
    ]

  def actualizar(self, id_tarea, descripcion=None):
    datos = self._cargar()
    tarea = next((t for t in datos["tareas"] if t["id"] == id_tarea), None)
    if not tarea:
      return False

    if descripcion is not None:
      if not isinstance(descripcion, str) or not descripcion.strip():
        raise ValueError("La descripción de la tarea debe ser una cadena no vacía.")
      tarea["descripcion"] = descripcion.strip()

    self._guardar(datos)
    return True

  def eliminar(self, id_tarea):
    datos = self._cargar()
    tarea = next((t for t in datos["tareas"] if t["id"] == id_tarea), None)
    if not tarea:
      return False

    datos["asignaciones"] = [a for a in datos["asignaciones"] if a["id_tarea"] != id_tarea]
    datos["tareas"] = [t for t in datos["tareas"] if t["id"] != id_tarea]

    self._guardar(datos)
    return True