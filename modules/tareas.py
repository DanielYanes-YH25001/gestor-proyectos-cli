import datos

def reporte_horas_por_proyecto():
  print("\n--- REPORTE: HORAS TOTALES POR PROYECTO ---")

  # Claúsula de guarda en caso no hayan proyectos
  if not datos.proyectos:
    print("No hay proyectos registrados.")
    return

  # Se muestran los proyectos disponibles para que el usuario elija
  print("Proyectos Disponibles:")
  for p in datos.proyectos:
    print(f"ID: {p['id']} | Nombre: {p['nombre']}")

  try:
    id_proyecto = int(input("\nIngrese el ID del proyecto a consultar: "))

    # Se valida que el proyecto exista
    proyecto_existe = next((p for p in datos.proyectos if p["id"] == id_proyecto), None)
    if not proyecto_existe:
      print("Error: El proyecto no existe.")
      return

    # Se buscan todas las tareas que pertenezcan al proyecto
    tareas_del_proyecto = [t["id"] for t in datos.tareas if t["id_proyecto"] == id_proyecto]

    # Se suman las horas de las asignaciones que coincidan con esas tareas
    total_horas = 0
    for asignacion in datos.asignaciones:
      if asignacion["id_tarea"] in tareas_del_proyecto:
        total_horas += asignacion["horas"]

    # Mostramos el total de horas
    print(
      f"\n=> El proyecto '{proyecto_existe['nombre']}' tiene un total de {total_horas} horas invertidas."
    )

  except ValueError:
    print("Error: Ingrese un ID numérico válido.")

def reporte_horas_por_tarea():
  print("\n--- REPORTE: HORAS TOTALES POR TAREA ---")

  # Claúsula de guarda en caso no hayan tareas
  if not datos.tareas:
    print("No hay tareas creadas.")
    return

  # Se muestran todas las tareas disponibles
  print("Tareas Disponibles:")
  for t in datos.tareas:
    print(
      f"ID: {t['id']} | Proyecto ID: {t['id_proyecto']} | Descripción: {t['descripcion']}"
    )

  try:
    id_tarea = int(input("\nIngrese el ID de la tarea a consultar: "))

    # Se valida que la tarea exista
    tarea_existe = next((t for t in datos.tareas if t["id"] == id_tarea), None)
    if not tarea_existe:
      print("Error: La tarea no existe.")
      return

    # Se suman las horas de todas las asignaciones vinculadas a esta tarea
    total_horas = sum(a["horas"] for a in datos.asignaciones if a["id_tarea"] == id_tarea)

    # Mostramos el total de horas
    print(
      f"\n=> La tarea '{tarea_existe['descripcion']}' tiene un total de {total_horas} horas invertidas."
    )

  except ValueError:
    print("Error: Ingrese un ID numérico válido.")

def validar_entrada(mensaje):
  while True:
    valor = input(mensaje).strip()
    if valor:
      return valor
    print("Error: El campo no puede estar vacío. Intente de nuevo.")

def menu_tareas():
  while True:
    print("\n--- SECCIÓN: GESTIÓN DE TAREAS Y ASIGNACIONES ---")
    print("1. Ver todas las tareas")
    print("2. Crear nueva tarea")
    print("3. Asignar tarea a empleado y registrar horas")
    print("4. Reporte: Total de horas por Proyecto")
    print("5. Reporte: Total de horas por Tarea")
    print("6. Volver al menú principal")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
      # Validamos si existen tareas
      if not datos.tareas:
        print("No hay tareas registradas.")
      else:
        # Mostramos la información de cada tarea
        for t in datos.tareas:
          print(
            f"ID Tarea: {t['id']} | Proyecto ID: {t['id_proyecto']} | Descripción: {t['descripcion']}"
          )

    elif opcion == "2":
      try:
        id_proyecto = int(input("Ingrese el ID del proyecto para esta tarea: "))

        # Validamos si el proyecto existe usando su ID
        if not any(p["id"] == id_proyecto for p in datos.proyectos):
          print("Error: El proyecto no existe.")
        else:
          # Validamos la descripción de la tarea y la agregamos a la lista de tareas
          desc = validar_entrada("Descripción de la tarea: ")
          datos.tareas.append({
            "id": datos.id_tarea_actual,
            "id_proyecto": id_proyecto,
            "descripcion": desc
          })
          print(f"Tarea creada con ID {datos.id_tarea_actual}.")
          datos.id_tarea_actual += 1

      except ValueError:
        print("Error: El ID debe ser un número entero.")

    elif opcion == "3":
      try:
        id_tarea = int(input("ID de la Tarea: "))
        id_empleado = int(input("ID de el Empleado: "))

        # Validamos si la tarea o empleado existen utilizando sus IDs
        if not any(t["id"] == id_tarea for t in datos.tareas) or not any(e["id"] == id_empleado for e in datos.empleados):
          print("Error: Tarea o Empleado no encontrados.")
        else:
          # Verificamos si el empleado ya tiene asignada la tarea
          asignacion = next(
            (a for a in datos.asignaciones if a["id_tarea"] == id_tarea and a["id_empleado"] == id_empleado),
            None,
          )

          # En caso no la tenga asignada, creamos una nueva
          if not asignacion:
            asignacion = {"id_tarea": id_tarea, "id_empleado": id_empleado, "horas": 0.0}
            datos.asignaciones.append(asignacion)

          # Caso contrario, registramos sus horas trabajadas
          horas = float(input("Horas trabajadas hoy: "))
          if horas > 12:
            print("Error: No se pueden registrar más de 12 horas al día.")
          elif horas < 0:
            print("Error: No se permiten horas negativas.")
          else:
            asignacion["horas"] += horas
            print(f"Registro exitoso. Total: {asignacion['horas']} horas.")

      except ValueError:
        print("Error: Ingrese valores numéricos válidos.")

    elif opcion == "4":
      # Mostramos horas trabajadas por proyecto
      reporte_horas_por_proyecto()

    elif opcion == "5":
      # Mostramos horas trabajadas por tarea
      reporte_horas_por_tarea()

    elif opcion == "6":
      break
    
    else:
      print("Opción inválida. Por favor, seleccione una de las opciones.")
