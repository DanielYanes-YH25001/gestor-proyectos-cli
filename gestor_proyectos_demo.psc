Algoritmo GestorProyectos
    // Definición de variables
    Definir opcion Como Entero
    Definir horasTrabajadas, totalHoras Como Real
    Definir nombreProyecto, nombreEmpleado, nombreTarea Como Cadena
    
    // Inicialización de datos simulados para la demo
    nombreProyecto <- "Desarrollo de App para Turismo"
    nombreEmpleado <- "Carlos"
    nombreTarea <- "Conexión a Base de Datos Oracle"
    totalHoras <- 0
    
    Repetir
        // Módulo 1 - Menú principal para la navegación
        Escribir "========================================"
        Escribir " GESTOR DE PROYECTOS: ", nombreProyecto
        Escribir "========================================"
        Escribir "1. Registrar horas trabajadas en la tarea"
        Escribir "2. Ver resumen y total de horas"
        Escribir "3. Salir"
        Escribir "Seleccione una opción: "
        Leer opcion
        
        Segun opcion Hacer
            1:
                // TODO: Alexis - Módulo 2: Registro de horas y Validación de Reglas del Negocio
                // 1. Pedir al usuario que ingrese la cantidad de horas trabajadas hoy usando Escribir y Leer (guardar en variable horasTrabajadas).
                // 2. Crear un bloque Si... Entonces para validar:
                //    - Si horasTrabajadas > 24, mostrar error de jornada irreal.
                //    - Si horasTrabajadas < 0, mostrar error de horas negativas.
                //    - Si los datos son correctos, sumar horasTrabajadas a la variable totalHoras y mostrar mensaje de éxito.
                
            2:
                // TODO: Wilbert - Módulo 3: Visualización de datos
                // 1. Mostrar en pantalla un resumen claro usando la función Escribir.
                // 2. Debes imprimir las variables: nombreProyecto, nombreTarea, nombreEmpleado y el totalHoras acumulado hasta el momento.
				
				//Módulo 3
				Escribir "                                                                       "
				Escribir "====================== RESUMEN DE ACTIVIDAD ==========================="
				Escribir "_______________________________________________________________________"
				Escribir " GESTOR DE PROYECTOS: " nombreProyecto
				Escribir "_______________________________________________________________________"
				Escribir " TAREA:               " nombreTarea
				Escribir "_______________________________________________________________________"
				Escribir " Empleado:            " nombreEmpleado
				Escribir "_______________________________________________________________________"
				Escribir " Horas acumuladas     " totalHoras
				Escribir "_______________________________________________________________________"
				Escribir "====================== FIN DE RESUMEN ================================"
				Escribir "                                                                       "

            3:
                Escribir "Saliendo del gestor de proyectos ..."

            De Otro Modo:
                Escribir "Opción inválida. Por favor, seleccione 1, 2 o 3."
        FinSegun
        
    Hasta Que opcion = 3
FinAlgoritmo
