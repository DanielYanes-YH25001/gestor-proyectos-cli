import json
from pathlib import Path


class ManejadorPersistencia:
  """Clase que maneja la lectura y escritura de los datos en el archivo JSON"""

  def __init__(self, filepath = None):
    self.filepath = Path(filepath or Path(__file__).resolve().parent.parent / "data.json")

  def _crear_archivo_vacio(self):
    """Crea un archivo JSON vacío con las claves esperadas"""

    self.guardar_datos(
      {
        "proyectos": [],
        "empleados": [],
        "tareas": [],
        "asignaciones": []
      }
    )

  def cargar_datos(self):
    """Carga el archivo JSON, creando un archivo vacío si no existe"""
    
    if not self.filepath.exists():
      self._crear_archivo_vacio()

    with self.filepath.open("r", encoding = "utf-8") as file:
      contenido = json.load(file)

    return {
      "proyectos": contenido.get("proyectos", []),
      "empleados": contenido.get("empleados", []),
      "tareas": contenido.get("tareas", []),
      "asignaciones": contenido.get("asignaciones", [])
    }

  def guardar_datos(self, datos):
    """
    Guarda los datos en el archivo JSON con un formato legible

    Args:
      datos (dict): Diccionario con las claves esperadas para las
      listas de proyectos, empleados, tareas y asignaciones
    """

    with self.filepath.open("w", encoding = "utf-8") as file:
      json.dump(
        {
          "proyectos": datos.get("proyectos", []),
          "empleados": datos.get("empleados", []),
          "tareas": datos.get("tareas", []),
          "asignaciones": datos.get("asignaciones", [])
        },
        file,
        indent=2,
        ensure_ascii=False
      )

  def obtener_proximo_id(self, lista):
    """
    Devuelve el siguiente ID disponible para la lista de empleados

    Args:
      lista (list[dict]): Lista que contiene los diccionarios de empleados
    """

    if not lista:
      return 1
    return max(item["id"] for item in lista) + 1
