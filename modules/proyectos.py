from modules.ui import error, info, prompt_input, render_menu, render_table, success
from utils import validar_entrada


def menu_proyectos(proyecto_service):
  """
  Menú interactivo para gestionar proyectos

  Args:
    proyecto_service (ProyectoService): Servicio de proyecto con operaciones CRUD
  """

  while True:
    render_menu(
      "Gestión de Proyectos",
      [
        "Ver lista de proyectos",
        "Agregar nuevo proyecto",
        "Actualizar proyecto",
        "Eliminar proyecto",
        "Volver al menú principal"
      ]
    )

    opcion = prompt_input("Seleccione una opción").strip()

    if opcion == "1":
      proyectos = proyecto_service.obtener_todos()
      if not proyectos:
        info("No hay proyectos registrados.")
      else:
        rows = [(p.id, p.nombre, p.estado) for p in proyectos]
        render_table(["ID", "Nombre", "Estado"], rows, title = "Lista de Proyectos")

    elif opcion == "2":
      try:
        nombre = validar_entrada("Ingrese el nombre del proyecto")
        proyecto = proyecto_service.crear(nombre)
        success(f"Proyecto '{proyecto.nombre}' creado con ID {proyecto.id}.")
      except ValueError as err:
        error(f"Error: {err}")

    elif opcion == "3":
      try:
        id_proyecto = int(prompt_input("Ingrese el ID del proyecto a actualizar"))
        proyecto = proyecto_service.obtener_por_id(id_proyecto)
        if not proyecto:
          error("Error: Proyecto no encontrado.")
          continue

        nombre = prompt_input(
          f"Nuevo nombre (actual: {proyecto.nombre}) [Enter para conservar]",
          default = ""
        ).strip()
        estado = prompt_input(
          f"Nuevo estado (Activo/Finalizado/Pausado) (actual: {proyecto.estado}) [Enter para conservar]",
          default = ""
        ).strip()

        if not nombre:
          nombre = None
        if not estado:
          estado = None

        proyecto_service.actualizar(id_proyecto, nombre = nombre, estado = estado)
        success("Proyecto actualizado correctamente.")
      except ValueError as err:
        error(f"Error: {err}")

    elif opcion == "4":
      try:
        id_proyecto = int(prompt_input("Ingrese el ID del proyecto a eliminar"))
        confirmacion = prompt_input(
          "ADVERTENCIA: Esto eliminará el proyecto, sus tareas y asignaciones asociadas. (si/no)",
          default = "no"
        ).strip().lower()

        if confirmacion == "si":
          if proyecto_service.eliminar(id_proyecto):
            success("Proyecto eliminado correctamente.")
          else:
            error("Error: Proyecto no encontrado.")
        else:
          info("Operación cancelada.")
      except ValueError:
        error("Error: Ingrese un ID numérico válido.")

    elif opcion == "5":
      break

    else:
      error("Opción inválida. Por favor, seleccione una de las opciones.")
