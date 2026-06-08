class Empleado:
  """clase para crear el empleado, con las validaciones"""

  def __init__(self, id, nombre, rol):
    if not isinstance(id, int) or id <= 0:
      raise ValueError("El ID del empleado debe ser un entero positivo.")
    if not nombre or not isinstance(nombre, str):
      raise ValueError("El nombre del empleado debe ser una cadena no vacía.")
    if not rol or not isinstance(rol, str):
      raise ValueError("El rol del empleado debe ser una cadena no vacía.")

    self.id = id
    self.nombre = nombre.strip()
    self.rol = rol.strip()

  def to_dict(self):
    """metodo para guardar los datos en JSON"""

    return {
      "id": self.id,
      "nombre": self.nombre,
      "rol": self.rol,
    }

  @classmethod
  def from_dict(cls, data):
    """metodo de clase para traer un empleado"""

    return cls(
      id=data["id"],
      nombre=data["nombre"],
      rol=data["rol"],
    )

  def __str__(self):
    """metodo para imprimir los datos de un empleado"""
    
    return f"Empleado(id={self.id}, nombre='{self.nombre}', rol='{self.rol}')"  