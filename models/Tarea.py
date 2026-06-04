#clase para crear las tareas, con las validaciones
class Tarea:
  def __init__(self, id, id_proyecto, descripcion):
    if not isinstance(id, int) or id <= 0:
      raise ValueError("El ID de la tarea debe ser un entero positivo.")
    if not isinstance(id_proyecto, int) or id_proyecto <= 0:
      raise ValueError("El ID de proyecto debe ser un entero positivo.")
    if not descripcion or not isinstance(descripcion, str):
      raise ValueError("La descripción de la tarea debe ser una cadena no vacía.")

    self.id = id
    self.id_proyecto = id_proyecto
    self.descripcion = descripcion.strip()
#metodo para guardar los datos en JSON
  def to_dict(self):
    return {
      "id": self.id,
      "id_proyecto": self.id_proyecto,
      "descripcion": self.descripcion,
    }
#metodo de clase para traer una tarea
  @classmethod
  def from_dict(cls, data):
    return cls(
      id=data["id"],
      id_proyecto=data["id_proyecto"],
      descripcion=data["descripcion"],
    )
#metodo para imprimir los datos de una tarea 
  def __str__(self):
    return f"Tarea(id={self.id}, id_proyecto={self.id_proyecto}, descripcion='{self.descripcion}')"