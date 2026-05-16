# modules/proyectos.py
import datos
def validar_entrada(mensaje):
  """
  Solicita un valor al usuario y valida que no esté vacío.
  
  Args:
    mensaje (str): Mensaje a mostrar al usuario
    
  Returns:
    str: Valor ingresado por el usuario (sin espacios en blanco al inicio/final)
  """
  while True:
    valor = input(mensaje).strip()
    if valor:
      return valor
    else:
      print("Error: El campo no puede estar vacío. Intente de nuevo.")

def menu_proyectos():
  """
  Muestra el menú de gestión de proyectos y maneja las opciones del usuario.
  """
  while True:
    print("\n--- SECCIÓN: GESTIÓN DE PROYECTOS ---")
    print("1. Ver lista de proyectos")
    print("2. Agregar nuevo proyecto")
    print("3. Volver al menú principal")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
      print("\n--- LISTA DE PROYECTOS ---")
      
      if not datos.proyectos:
        print("No hay proyectos registrados.")
      else:
        for p in datos.proyectos:
          print(f"ID: {p['id']} | Nombre: {p['nombre']} | Estado: {p['estado']}")
    
    elif opcion == "2":
      nombre = validar_entrada("Ingrese el nombre del proyecto: ")
      
      nuevo_proyecto = {
        "id": datos.id_proyecto_actual,
        "nombre": nombre,
        "estado": "Activo"
      }
      datos.proyectos.append(nuevo_proyecto)
      print(f"Éxito: Proyecto '{nombre}' creado con ID {datos.id_proyecto_actual}.")
      datos.id_proyecto_actual += 1
    
    elif opcion == "3":
      break
    
    else:
      print("Opción inválida. Por favor, seleccione una de las tres opciones.")