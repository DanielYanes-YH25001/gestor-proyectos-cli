#clase para crear el empleado, con las validaciones
class Empleado:
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
#metodo para guardar los datos en JSON
  def to_dict(self):
    return {
      "id": self.id,
      "nombre": self.nombre,
      "rol": self.rol,
    }
#metodo de clase para traer un empleado
  @classmethod
  def from_dict(cls, data):
    return cls(
      id=data["id"],
      nombre=data["nombre"],
      rol=data["rol"],
    )
#metodo para imprimir los datos de un empleado
  def __str__(self):
    return f"Empleado(id={self.id}, nombre='{self.nombre}', rol='{self.rol}')"