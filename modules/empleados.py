from modules.ui import error, info, prompt_input, render_menu, render_table, success
from utils import validar_entrada


def menu_empleados(empleado_service):
  """
  Menú interactivo para gestionar empleados

  Args:
    empleado_service (EmpleadoService): Servicio de empleado con operaciones CRUD
  """
  
  while True:
    render_menu(
      "Gestión de Empleados",
      [
        "Ver lista de empleados",
        "Agregar nuevo empleado",
        "Actualizar empleado",
        "Eliminar empleado",
        "Volver al menú principal"
      ]
    )

    opcion = prompt_input("Seleccione una opción").strip()

    if opcion == "1":
      empleados = empleado_service.obtener_todos()
      if not empleados:
        info("No hay empleados registrados.")
      else:
        rows = [(e.id, e.nombre, e.rol) for e in empleados]
        render_table(["ID", "Nombre", "Rol"], rows, title = "Lista de Empleados")

    elif opcion == "2":
      try:
        nombre = validar_entrada("Ingrese el nombre del empleado")
        rol = validar_entrada("Ingrese el rol (Ej. Desarrollador)")
        empleado = empleado_service.crear(nombre, rol)
        success(f"Empleado '{empleado.nombre}' registrado con ID {empleado.id}.")
      except ValueError as err:
        error(f"Error: {err}")

    elif opcion == "3":
      try:
        id_empleado = int(prompt_input("Ingrese el ID del empleado a actualizar"))
        empleado = empleado_service.obtener_por_id(id_empleado)
        if not empleado:
          error("Error: Empleado no encontrado.")
          continue

        nombre = prompt_input(
          f"Nuevo nombre (actual: {empleado.nombre}) [Enter para conservar]",
          default = ""
        ).strip()
        rol = prompt_input(
          f"Nuevo rol (actual: {empleado.rol}) [Enter para conservar]",
          default = ""
        ).strip()

        if not nombre:
          nombre = None
        if not rol:
          rol = None

        empleado_service.actualizar(id_empleado, nombre = nombre, rol = rol)
        success("Empleado actualizado correctamente.")
      except ValueError as err:
        error(f"Error: {err}")

    elif opcion == "4":
      try:
        id_empleado = int(prompt_input("Ingrese el ID del empleado a eliminar"))
        confirmacion = prompt_input(
          "ADVERTENCIA: Esto eliminará el empleado y sus asignaciones. (si/no)",
          default = "no"
        ).strip().lower()

        if confirmacion == "si":
          if empleado_service.eliminar(id_empleado):
            success("Empleado eliminado correctamente.")
          else:
            error("Error: Empleado no encontrado.")
        else:
          info("Operación cancelada.")
      except ValueError:
        error("Error: Ingrese un ID numérico válido.")

    elif opcion == "5":
      break

    else:
      error("Opción inválida. Por favor, seleccione una de las opciones.")
