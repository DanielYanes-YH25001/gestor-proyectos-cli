from modules import datos

def validar_entrada(mensaje):
    """
    Solicita un valor al usuario y asegura que no este vacio.
    """
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        else:
            print("Error: El campo no puede estar vacio. Intente de nuevo.")

def menu_empleados():
    """
    Muestra el menu de gestion de empleados y procesa las opciones.
    """
    while True:
        print("\n--- SECCION: GESTION DE EMPLEADOS ---")
        print("1. Ver lista de empleados")
        print("2. Agregar nuevo empleado")
        print("3. Volver al menu principal")
        
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            print("\n--- LISTA DE EMPLEADOS ---")
            
            # Verificamos si la lista en el modulo datos este vacia
            if not datos.empleados:
                print("No hay empleados registrados.")
            else:
                for e in datos.empleados:
                    print(f"ID: {e['id']} | Nombre: {e['nombre']} | Rol: {e['rol']}")

        elif opcion == "2":
            # Usamos nuestra funci�n de validacion para asegurar datos limpios
            nombre = validar_entrada("Ingrese el nombre del empleado: ")
            rol = validar_entrada("Ingrese el rol (Ej. Desarrollador): ")

            nuevo_empleado = {
                "id": datos.id_empleado_actual,
                "nombre": nombre,
                "rol": rol
            }

            datos.empleados.append(nuevo_empleado)
            print(f"Exito: Empleado '{nombre}' registrado con ID {datos.id_empleado_actual}.")
            
            # Incrementamos el contador global de IDs para el pr�ximo registro
            datos.id_empleado_actual += 1

        elif opcion == "3":
            # Salimos del bucle para volver al men� anterior
            break
            
        else:
            print("Opcion invalida. Por favor, seleccione una de las tres opciones.")