from modules import empleados, proyectos, tareas
from modules.persistence import ManejadorPersistencia
from modules.ui import error, prompt_input, render_header, render_menu
from services.asignacion_service import AsignacionService
from services.empleado_service import EmpleadoService
from services.proyecto_service import ProyectoService
from services.tarea_service import TareaService


def main():
  # Instanciamos un manejador de persistencia y cargamos los datos
  manejador_persistencia = ManejadorPersistencia()
  manejador_persistencia.cargar_datos()

  proyecto_service = ProyectoService(manejador_persistencia)
  empleado_service = EmpleadoService(manejador_persistencia)
  tarea_service = TareaService(manejador_persistencia)
  asignacion_service = AsignacionService(manejador_persistencia)

  # Bucle infinito para mantener el programa en ejecución
  while True:
    # Se muestra el menú principal
    render_header("GESTOR DE PROYECTOS")
    render_menu(
      "Menú Principal",
      [
        "Gestionar Proyectos",
        "Gestionar Empleados",
        "Gestionar Tareas y Asignaciones",
        "Salir del gestor",
      ],
    )

    # Solicitamos al usuario que seleccione una opción
    opcion = prompt_input("Seleccione una sección").strip()

    if opcion == "1":
      # Llama al menú de gestión de proyectos
      proyectos.menu_proyectos(proyecto_service)

    elif opcion == "2":
      # Llama al menú de gestión de empleados
      empleados.menu_empleados(empleado_service)

    elif opcion == "3":
      # Llama al menú de gestión de tareas y asignaciones
      tareas.menu_tareas(
        tarea_service,
        proyecto_service,
        empleado_service,
        asignacion_service,
      )

    elif opcion == "4":
      break

    else:
      error("Opción inválida. Por favor, seleccione una de las cuatro opciones.")


# Punto de entrada del programa; evita que la función principal
# se ejecute si este archivo no se ejecuta directamente
if __name__ == "__main__":
  main()
