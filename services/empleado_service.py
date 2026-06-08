from models.empleado import Empleado

<<<<<<< HEAD
class EmpleadoService:
  def __init__(self, manejador_persistencia):
    self.manejador_persistencia = manejador_persistencia

  def _cargar(self):
    return self.manejador_persistencia.cargar_datos()

  def _guardar(self, datos):
    self.manejador_persistencia.guardar_datos(datos)

  def crear(self, nombre, rol):
=======

class EmpleadoService:
  # Servicio para gestionar empleados
  
  def __init__(self, manejador_persistencia):
    # Constructor: recibe el manejador de persistencia
    self.manejador_persistencia = manejador_persistencia

  def _cargar(self):
    # Carga los datos desde el manejador de persistencia
    return self.manejador_persistencia.cargar_datos()

  def _guardar(self, datos):
    # Guarda los datos en el manejador de persistencia
    self.manejador_persistencia.guardar_datos(datos)

  def crear(self, nombre, rol):
    # Crea un nuevo empleado
>>>>>>> main
    datos = self._cargar()
    nuevo_id = self.manejador_persistencia.obtener_proximo_id(datos["empleados"])
    empleado = Empleado(nuevo_id, nombre, rol)
    datos["empleados"].append(empleado.to_dict())
    self._guardar(datos)
    return empleado

  def obtener_todos(self):
<<<<<<< HEAD
=======
    # Retorna todos los empleados
>>>>>>> main
    datos = self._cargar()
    return [Empleado.from_dict(e) for e in datos["empleados"]]

  def obtener_por_id(self, id_empleado):
<<<<<<< HEAD
=======
    # Obtiene un empleado por su ID
>>>>>>> main
    datos = self._cargar()
    empleado = next((e for e in datos["empleados"] if e["id"] == id_empleado), None)
    return Empleado.from_dict(empleado) if empleado else None

  def actualizar(self, id_empleado, nombre=None, rol=None):
<<<<<<< HEAD
=======
    # Actualiza los datos de un empleado (nombre y/o rol)
>>>>>>> main
    datos = self._cargar()
    empleado = next((e for e in datos["empleados"] if e["id"] == id_empleado), None)
    if not empleado:
      return False

    if nombre is not None:
      if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre del empleado debe ser una cadena no vacía.")
      empleado["nombre"] = nombre.strip()

    if rol is not None:
      if not isinstance(rol, str) or not rol.strip():
        raise ValueError("El rol del empleado debe ser una cadena no vacía.")
      empleado["rol"] = rol.strip()

    self._guardar(datos)
    return True

  def eliminar(self, id_empleado):
<<<<<<< HEAD
=======
    # Elimina un empleado y sus asignaciones relacionadas
>>>>>>> main
    datos = self._cargar()
    empleado = next((e for e in datos["empleados"] if e["id"] == id_empleado), None)
    if not empleado:
      return False

<<<<<<< HEAD
    datos["asignaciones"] = [a for a in datos["asignaciones"] if a["id_empleado"] != id_empleado]
=======
    # Elimina todas las asignaciones del empleado
    datos["asignaciones"] = [a for a in datos["asignaciones"] if a["id_empleado"] != id_empleado]
    # Elimina el empleado
>>>>>>> main
    datos["empleados"] = [e for e in datos["empleados"] if e["id"] != id_empleado]

    self._guardar(datos)
    return True