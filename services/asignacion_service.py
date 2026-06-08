from models.asignacion import Asignacion

<<<<<<< HEAD
class AsignacionService:
  def __init__(self, manejador_persistencia):
    self.manejador_persistencia = manejador_persistencia
    self.persistence = manejador_persistencia

  def _cargar(self):
    return self.manejador_persistencia.cargar_datos()

  def _guardar(self, datos):
    self.manejador_persistencia.guardar_datos(datos)

  def crear(self, id_tarea, id_empleado):
=======

class AsignacionService:
  # Servicio para gestionar asignaciones de empleados a tareas
  
  def __init__(self, manejador_persistencia):
    # Constructor: recibe el manejador de persistencia
    self.manejador_persistencia = manejador_persistencia

  def _cargar(self):
    # Carga los datos desde el manejador de persistencia
    return self.manejador_persistencia.cargar_datos()

  def _guardar(self, datos):
    # Guarda los datos en el manejador de persistencia
    self.manejador_persistencia.guardar_datos(datos)

  def crear(self, id_tarea, id_empleado):
    # Crea una nueva asignación con horas iniciales en 0
>>>>>>> main
    datos = self._cargar()
    nuevo_id = self.manejador_persistencia.obtener_proximo_id(datos["asignaciones"])
    asignacion = Asignacion(nuevo_id, id_tarea, id_empleado, horas=0.0)
    datos["asignaciones"].append(asignacion.to_dict())
    self._guardar(datos)
    return asignacion

  def obtener_todos(self):
<<<<<<< HEAD
=======
    # Retorna todas las asignaciones
>>>>>>> main
    datos = self._cargar()
    return [Asignacion.from_dict(a) for a in datos["asignaciones"]]

  def obtener_por_id(self, id_asignacion):
<<<<<<< HEAD
=======
    # Obtiene una asignación por su ID
>>>>>>> main
    datos = self._cargar()
    asignacion = next((a for a in datos["asignaciones"] if a["id"] == id_asignacion), None)
    return Asignacion.from_dict(asignacion) if asignacion else None

  def obtener_por_tarea(self, id_tarea):
<<<<<<< HEAD
=======
    # Obtiene todas las asignaciones de una tarea específica
>>>>>>> main
    datos = self._cargar()
    return [
      Asignacion.from_dict(a)
      for a in datos["asignaciones"]
      if a["id_tarea"] == id_tarea
    ]

  def obtener_por_tarea_y_empleado(self, id_tarea, id_empleado):
<<<<<<< HEAD
=======
    # Obtiene una asignación por tarea y empleado
>>>>>>> main
    datos = self._cargar()
    asignacion = next(
      (
        a
        for a in datos["asignaciones"]
        if a["id_tarea"] == id_tarea and a["id_empleado"] == id_empleado
      ),
      None,
    )
    return Asignacion.from_dict(asignacion) if asignacion else None

  def obtener_por_empleado(self, id_empleado):
<<<<<<< HEAD
=======
    # Obtiene todas las asignaciones de un empleado específico
>>>>>>> main
    datos = self._cargar()
    return [
      Asignacion.from_dict(a)
      for a in datos["asignaciones"]
      if a["id_empleado"] == id_empleado
    ]

  def agregar_horas(self, id_tarea, id_empleado, horas):
<<<<<<< HEAD
    if not isinstance(horas, (int, float)):
      raise ValueError("Las horas deben ser un número.")
    if horas < 0 or horas > 12:
      raise ValueError("Las horas deben estar entre 0 y 12.")
=======
    # Agrega horas a una asignación (solo valida horas ingresadas, no el total)
    if not isinstance(horas, (int, float)):
      raise ValueError("Las horas deben ser un número.")
    if horas < 0 or horas > 12:
      raise ValueError("No se pueden registrar más de 12 horas al día.")
>>>>>>> main

    datos = self._cargar()
    asignacion = next(
      (
        a
        for a in datos["asignaciones"]
        if a["id_tarea"] == id_tarea and a["id_empleado"] == id_empleado
      ),
      None,
    )

    if asignacion is None:
<<<<<<< HEAD
=======
      # Crea nueva asignación si no existe
>>>>>>> main
      nuevo_id = self.manejador_persistencia.obtener_proximo_id(datos["asignaciones"])
      asignacion = Asignacion(nuevo_id, id_tarea, id_empleado, horas=horas)
      datos["asignaciones"].append(asignacion.to_dict())
    else:
<<<<<<< HEAD
      nuevo_total = float(asignacion["horas"]) + float(horas)
      if nuevo_total > 12:
        raise ValueError("No se pueden registrar más de 12 horas al día.")
=======
      # Suma las horas al total existente
      nuevo_total = float(asignacion["horas"]) + float(horas)
>>>>>>> main
      asignacion["horas"] = nuevo_total

    self._guardar(datos)
    return True

  def actualizar_horas(self, id_asignacion, horas):
<<<<<<< HEAD
=======
    # Actualiza el total de horas de una asignación existente
>>>>>>> main
    if not isinstance(horas, (int, float)):
      raise ValueError("Las horas deben ser un número.")
    if horas < 0 or horas > 12:
      raise ValueError("No se pueden registrar más de 12 horas al día.")

    datos = self._cargar()
    asignacion = next((a for a in datos["asignaciones"] if a["id"] == id_asignacion), None)
    
    if not asignacion:
      return False

    asignacion["horas"] = float(horas)
    self._guardar(datos)
    return True

  def eliminar(self, id_asignacion):
<<<<<<< HEAD
    datos = self._cargar()
    asignacion = next((a for a in datos["asignaciones"] if a["id"] == id_asignacion), None)
    
=======
    # Elimina una asignación por su ID
    datos = self._cargar()
    asignacion = next((a for a in datos["asignaciones"] if a["id"] == id_asignacion), None)

>>>>>>> main
    if not asignacion:
      return False

    datos["asignaciones"] = [a for a in datos["asignaciones"] if a["id"] != id_asignacion]
    self._guardar(datos)
    return True