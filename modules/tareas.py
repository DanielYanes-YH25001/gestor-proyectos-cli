from modules.ui import error, info, prompt_input, render_menu, render_table, success
from utils import validar_entrada


def mostrar_tareas(tarea_service):
  """
  Muestra una tabla con todas las tareas registradas

  Args:
    tarea_service (TareaService): Servicio de tarea con operaciones CRUD
  """

  tareas = tarea_service.obtener_todos()
  if not tareas:
    info("No hay tareas registradas.")
    return

  rows = [(t.id, t.id_proyecto, t.descripcion) for t in tareas]
  render_table(["ID", "Proyecto ID", "Descripción"], rows, title = "Lista de Tareas")


def mostrar_asignaciones(asignacion_service, tarea_service, empleado_service):
  """
  Muestra todas las asignaciones con datos de la tarea y empleado relacionados, y
  las horas trabajadas por el empleado

  Args:
    asignacion_service (AsignacionService): Servicio de asignación con operaciones CRUD
    tarea_service (TareaService): Servicio de tarea con operaciones CRUD
    empleado_service (EmpleadoService): Servicio de empleado con operaciones CRUD
  """

  asignaciones = asignacion_service.obtener_todos()
  if not asignaciones:
    info("No hay asignaciones registradas.")
    return

  rows = []
  for a in asignaciones:
    tarea = tarea_service.obtener_por_id(a.id_tarea)
    empleado = empleado_service.obtener_por_id(a.id_empleado)
    tarea_descripcion = tarea.descripcion if tarea else "Desconocida"
    empleado_nombre = empleado.nombre if empleado else "Desconocido"
    empleado_rol = empleado.rol if empleado else "Desconocido"
    rows.append(
      (
        a.id,
        a.id_tarea,
        tarea_descripcion,
        f"{empleado_nombre} ({empleado_rol})",
        a.horas
      )
    )

  render_table(
    ["ID", "Tarea ID", "Tarea", "Empleado (Rol)", "Horas"],
    rows,
    title = "Lista de Asignaciones"
  )


def reporte_horas_por_proyecto(proyecto_service):
  """
  Muestra las horas totales invertidas en un proyecto

  Args:
    proyecto_service (ProyectoService): Servicio de proyecto con operaciones CRUD
  """

  datos = proyecto_service.manejador_persistencia.cargar_datos()
  proyectos = proyecto_service.obtener_todos()

  if not proyectos:
    info("No hay proyectos registrados.")
    return

  rows = [(p.id, p.nombre) for p in proyectos]
  render_table(["ID", "Nombre"], rows, title = "Proyectos disponibles")

  try:
    id_proyecto = int(prompt_input("Ingrese el ID del proyecto a consultar"))
    proyecto = proyecto_service.obtener_por_id(id_proyecto)
    if not proyecto:
      error("Error: El proyecto no existe.")
      return

    tareas_del_proyecto = [t["id"] for t in datos["tareas"] if t["id_proyecto"] == id_proyecto]
    total_horas = sum(
      a["horas"]
      for a in datos["asignaciones"]
      if a["id_tarea"] in tareas_del_proyecto
    )

    success(f"El proyecto '{proyecto.nombre}' tiene un total de {total_horas} horas invertidas.")
  except ValueError:
    error("Error: Ingrese un ID numérico válido.")


def reporte_horas_por_tarea(tarea_service, asignacion_service):
  """
  Muestra las horas totales invertidas en una tarea específica

  Args:
    tarea_service (TareaService): Servicio de tarea con operaciones CRUD
    asignacion_service (AsignacionService): Servicio de asignación con operaciones CRUD
  """

  tareas = tarea_service.obtener_todos()
  if not tareas:
    info("No hay tareas creadas.")
    return

  rows = [(t.id, t.id_proyecto, t.descripcion) for t in tareas]
  render_table(["ID", "Proyecto ID", "Descripción"], rows, title = "Tareas disponibles")

  try:
    id_tarea = int(prompt_input("Ingrese el ID de la tarea a consultar"))
    tarea = tarea_service.obtener_por_id(id_tarea)
    if not tarea:
      error("Error: La tarea no existe.")
      return

    asignaciones = asignacion_service.obtener_por_tarea(id_tarea)
    total_horas = sum(a.horas for a in asignaciones)
    success(f"La tarea '{tarea.descripcion}' tiene un total de {total_horas} horas invertidas.")
  except ValueError:
    error("Error: Ingrese un ID numérico válido.")


def menu_tareas(tarea_service, proyecto_service, empleado_service, asignacion_service):
  """
  Menú interactivo para gestionar tareas, asignaciones y reportes

  Args:
    tarea_service (TareaService): Servicio de tarea con operaciones CRUD
    proyecto_service (ProyectoService): Servicio de proyecto con operaciones CRUD
    empleado_service (EmpleadoService): Servicio de empleado con operaciones CRUD
    asignacion_service (AsignacionService): Servicio de asignación con operaciones CRUD
  """

  while True:
    render_menu(
      "Gestión de Tareas y Asignaciones",
      [
        "Ver todas las tareas",
        "Crear nueva tarea",
        "Actualizar tarea",
        "Eliminar tarea",
        "Asignar tarea a empleado y registrar horas",
        "Actualizar horas de asignación",
        "Ver todas las asignaciones",
        "Eliminar asignación",
        "Reporte: Total de horas por Proyecto",
        "Reporte: Total de horas por Tarea",
        "Volver al menú principal"
      ]
    )

    opcion = prompt_input("Seleccione una opción").strip()

    if opcion == "1":
      mostrar_tareas(tarea_service)

    elif opcion == "2":
      try:
        id_proyecto = int(prompt_input("Ingrese el ID del proyecto para esta tarea"))
        proyecto = proyecto_service.obtener_por_id(id_proyecto)
        if not proyecto:
          error("Error: El proyecto no existe.")
          continue

        descripcion = validar_entrada("Descripción de la tarea")
        tarea = tarea_service.crear(id_proyecto, descripcion)
        success(f"Tarea creada con ID {tarea.id}.")
      except ValueError:
        error("Error: El ID debe ser un número entero válido.")

    elif opcion == "3":
      try:
        id_tarea = int(prompt_input("Ingrese el ID de la tarea a actualizar"))
        tarea = tarea_service.obtener_por_id(id_tarea)
        if not tarea:
          error("Error: Tarea no encontrada.")
          continue

        descripcion = prompt_input(
          f"Nueva descripción (actual: {tarea.descripcion}) [Enter para conservar]",
          default = ""
        ).strip()
        if not descripcion:
          descripcion = None

        tarea_service.actualizar(id_tarea, descripcion=descripcion)
        success("Tarea actualizada correctamente.")
      except ValueError as err:
        error(f"Error: {err}")

    elif opcion == "4":
      try:
        id_tarea = int(prompt_input("Ingrese el ID de la tarea a eliminar"))
        confirmacion = prompt_input(
          "ADVERTENCIA: Esto eliminará la tarea y sus asignaciones. (si/no)",
          default = "no"
        ).strip().lower()
        if confirmacion == "si":
          if tarea_service.eliminar(id_tarea):
            success("Tarea eliminada correctamente.")
          else:
            error("Error: Tarea no encontrada.")
        else:
          info("Operación cancelada.")
      except ValueError:
        error("Error: Ingrese un ID numérico válido.")

    elif opcion == "5":
      try:
        id_tarea = int(prompt_input("ID de la tarea"))
        id_empleado = int(prompt_input("ID del empleado"))

        tarea = tarea_service.obtener_por_id(id_tarea)
        empleado = empleado_service.obtener_por_id(id_empleado)
        if not tarea or not empleado:
          error("Error: Tarea o empleado no encontrados.")
          continue

        horas = float(prompt_input("Horas trabajadas hoy"))
        asignacion_service.agregar_horas(id_tarea, id_empleado, horas)
        success("Registro de horas almacenado correctamente.")
      except ValueError as err:
        error(f"Error: {err}")

    elif opcion == "6":
      try:
        id_asignacion = int(prompt_input("Ingrese el ID de la asignación"))
        horas = float(prompt_input("Nuevo total de horas (0-12)"))
        if asignacion_service.actualizar_horas(id_asignacion, horas):
          success("Horas actualizadas correctamente.")
        else:
          error("Error: Asignación no encontrada.")
      except ValueError as err:
        error(f"Error: {err}")

    elif opcion == "7":
      mostrar_asignaciones(
        asignacion_service,
        tarea_service,
        empleado_service
      )

    elif opcion == "8":
      try:
        id_asignacion = int(prompt_input("Ingrese el ID de la asignación a eliminar"))
        confirmacion = prompt_input(
          "¿Desea eliminar esta asignación? (si/no)",
          default = "no"
        ).strip().lower()
        if confirmacion == "si":
          if asignacion_service.eliminar(id_asignacion):
            success("Asignación eliminada correctamente.")
          else:
            error("Error: Asignación no encontrada.")
        else:
          info("Operación cancelada.")
      except ValueError:
        error("Error: Ingrese un ID numérico válido.")

    elif opcion == "9":
      reporte_horas_por_proyecto(proyecto_service)

    elif opcion == "10":
      reporte_horas_por_tarea(tarea_service, asignacion_service)

    elif opcion == "11":
      break

    else:
      error("Opción inválida. Por favor, seleccione una de las opciones.")
