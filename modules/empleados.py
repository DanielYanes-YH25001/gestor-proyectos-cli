import datos

def validar_entrada(mensaje):
  """Solicita un valor al usuario y asegura que no esté vacío."""
  while True:
    valor = input(mensaje).strip()
    if valor:
      return valor
    print("Error: El campo no puede estar vacío. Intente de nuevo.")


def mostrar_empleados():
  """Muestra la lista de empleados registrados."""
  print("\n--- LISTA DE EMPLEADOS ---")
  
  if not datos.empleados:
    print("No hay empleados registrados.")
    return

  for e in datos.empleados:
    print(f"ID: {e['id']} | Nombre: {e['nombre']} | Rol: {e['rol']}")


def registrar_empleado():
  """Gestiona el flujo para añadir un nuevo empleado."""
  print("\n--- REGISTRAR NUEVO EMPLEADO ---")
  nombre = validar_entrada("Ingrese el nombre del empleado: ")
  rol = validar_entrada("Ingrese el rol (Ej. Desarrollador): ")

  nuevo_empleado = {
    "id": datos.id_empleado_actual,
    "nombre": nombre,
    "rol": rol
  }

  datos.empleados.append(nuevo_empleado)
  print(f"¡Éxito!: Empleado '{nombre}' registrado con ID {datos.id_empleado_actual}.")
  
  # Incrementamos el contador global para el próximo registro
  datos.id_empleado_actual += 1


def menu_empleados():
  """Muestra el menú de gestión de empleados y procesa las opciones."""
  while True:
    print("\n--- SECCIÓN: GESTIÓN DE EMPLEADOS ---")
    print("1. Ver lista de empleados")
    print("2. Agregar nuevo empleado")
    print("3. Volver al menú principal")
    
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
      mostrar_empleados()
    elif opcion == "2":
      registrar_empleado()
    elif opcion == "3":
      print("Volviendo al menú principal...")
      break
    else:
      print("Opción inválida. Por favor, seleccione una de las opciones válidas (1-3).")