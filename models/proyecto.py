class Proyecto:
  """clase para crear los proyectos, con las validaciones para id, nomre y estado"""

  def __init__(self, id, nombre, estado="Activo"):
    if not isinstance(id, int) or id <= 0:
      raise ValueError("El ID del proyecto debe ser un entero positivo.")
    if not nombre or not isinstance(nombre, str):
      raise ValueError("El nombre del proyecto debe ser una cadena no vacía.")
    if estado not in {"Activo", "Finalizado", "Pausado"}:
      raise ValueError(
        "El estado del proyecto debe ser 'Activo', 'Finalizado' o 'Pausado'."
      )

    self.id = id
    self.nombre = nombre.strip()
    self.estado = estado

  def to_dict(self):
    """metodo para guardar los datos en JSON"""

    return {
      "id": self.id,
      "nombre": self.nombre,
      "estado": self.estado,
    }

  @classmethod
  def from_dict(cls, data):
    """metodo de clase para traer un proyecto"""

    return cls(
      id=data["id"],
      nombre=data["nombre"],
      estado=data.get("estado", "Activo"),
    )
 
  def __str__(self):
    """metodo para imprimir los atributos de un proyecto"""
    
    return f"Proyecto(id={self.id}, nombre='{self.nombre}', estado='{self.estado}')"  