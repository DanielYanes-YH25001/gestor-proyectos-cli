#clase para crear la asignacion de proyecto, con las validaciones
class Asignacion:
  def __init__(self, id, id_tarea, id_empleado, horas=0.0):
    if not isinstance(id, int) or id <= 0:
      raise ValueError("El ID de la asignación debe ser un entero positivo.")
    if not isinstance(id_tarea, int) or id_tarea <= 0:
      raise ValueError("El ID de tarea debe ser un entero positivo.")
    if not isinstance(id_empleado, int) or id_empleado <= 0:
      raise ValueError("El ID de empleado debe ser un entero positivo.")
    if not isinstance(horas, (int, float)):
      raise ValueError("Las horas deben ser un número.")
    if horas < 0 or horas > 12:
      raise ValueError("Las horas deben estar entre 0 y 12.")

    self.id = id
    self.id_tarea = id_tarea
    self.id_empleado = id_empleado
    self.horas = float(horas)
#metodo para guardar los datos en JSON
  def to_dict(self):
    return {
      "id": self.id,
      "id_tarea": self.id_tarea,
      "id_empleado": self.id_empleado,
      "horas": self.horas,
    }
#metodo de clase para traer una asigancion
  @classmethod
  def from_dict(cls, data):
    return cls(
      id=data["id"],
      id_tarea=data["id_tarea"],
      id_empleado=data["id_empleado"],
      horas=data.get("horas", 0.0),
    )
#metodo para imprimir los atributos de la asignacion
  def __str__(self):
    return (
      f"Asignacion(id={self.id}, id_tarea={self.id_tarea}, "
      f"id_empleado={self.id_empleado}, horas={self.horas})"
    )