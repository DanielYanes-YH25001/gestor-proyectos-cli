class Asignacion:
  """Clase para modelar una asignación"""

  def __init__(self, id, id_tarea, id_empleado, horas = 0.0):
    if not isinstance(id, int) or id <= 0:
      raise ValueError("El ID de la asignación debe ser un entero positivo.")
    if not isinstance(id_tarea, int) or id_tarea <= 0:
      raise ValueError("El ID de tarea debe ser un entero positivo.")
    if not isinstance(id_empleado, int) or id_empleado <= 0:
      raise ValueError("El ID de empleado debe ser un entero positivo.")
    if not isinstance(horas, (int, float)):
      raise ValueError("Las horas deben ser un número.")

    self.id = id
    self.id_tarea = id_tarea
    self.id_empleado = id_empleado
    self.horas = float(horas)

  def to_dict(self):
    """Método para guardar los datos en JSON"""
    return {
      "id": self.id,
      "id_tarea": self.id_tarea,
      "id_empleado": self.id_empleado,
      "horas": self.horas
    }

  @classmethod
  def from_dict(cls, data):
    """Método de clase para traer una asignación"""
    return cls(
      id = data["id"],
      id_tarea = data["id_tarea"],
      id_empleado = data["id_empleado"],
      horas = data.get("horas", 0.0)
    )

  def __str__(self):
    """Método para imprimir los atributos de la asignación"""
    return f"Asignacion(id={self.id}, id_tarea={self.id_tarea}, id_empleado={self.id_empleado}, horas={self.horas})"