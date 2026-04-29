from modules import proyectos, empleados, tareas

def main():
  # Bucle infinito para mantener el programa en ejecución
  while True:
    # Menú principal
    print("\n=========================")
    print("  GESTOR DE PROYECTOS")
    print("=========================")
    print("1. Gestionar Proyectos")
    print("2. Gestionar Empleados")
    print("3. Gestionar Tareas y Asignaciones")
    print("4. Salir del gestor")

    # Solicitamos al usuario que seleccione una opción
    opcion = input("Seleccione una sección: ")

    # Validamos la opción ingresada por el usuario
    if opcion == "1":
      # Llama al menú de gestión de proyectos
      proyectos.menu_proyectos()

    elif opcion == "2":
      # Llama al menú de gestión de empleados
      empleados.menu_empleados()

    elif opcion == "3":
      # Llama al menú de gestión de tareas y asignaciones
      tareas.menu_tareas()

    elif opcion == "4":
      print("Saliendo del gestor de proyectos...")
      break

    else:
      print("Opción inválida. Por favor, seleccione una de las cuatro opciones.")

# Punto de entrada del programa; evita que la función principal
# se ejecute si este archivo no se ejecuta directamente
if __name__ == "__main__":
  main()
