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
        Escribir "====================================================="
        Escribir " GESTOR DE PROYECTOS: ", nombreProyecto
        Escribir "====================================================="
        Escribir "1. Registrar horas trabajadas en la tarea"
        Escribir "2. Ver resumen y total de horas"
        Escribir "3. Salir"
        Escribir "Seleccione una opción: "
        Leer opcion
        
        Segun opcion Hacer
            1:
				// Módulo 2 - Registro de horas y Validación de Reglas del Negocio
                Escribir "----------------------------------------"
                Escribir "REGISTRO DE HORAS TRABAJADAS"
                Escribir "----------------------------------------"
                Escribir "Ingrese la cantidad de horas trabajadas hoy: "
                Leer horasTrabajadas
                
                Si horasTrabajadas > 12 Entonces
                    Escribir "ERROR: Jornada irreal. No puede registrar más de 12 horas en un día."
                Sino
                    Si horasTrabajadas < 0 Entonces
                        Escribir "ERROR: Horas negativas. No puede registrar valores negativos."
                    Sino
                        totalHoras <- totalHoras + horasTrabajadas
                        Escribir "ÉXITO: Se han registrado ", horasTrabajadas, " horas correctamente."
                        Escribir "Total acumulado hasta ahora: ", totalHoras, " horas."
                    FinSi
                FinSi
                Escribir ""
            2:
				// Módulo 3 - Visualización de datos
				Escribir "                                                                       "
				Escribir "====================== RESUMEN DE ACTIVIDAD ==========================="
				Escribir " Gestor de proyectos: " nombreProyecto
				Escribir " Tarea:               " nombreTarea
				Escribir " Empleado:            " nombreEmpleado
				Escribir " Horas acumuladas:    " totalHoras
				Escribir "====================== FIN DE RESUMEN ================================"
				Escribir "                                                                       "
            3:
                Escribir "Saliendo del gestor de proyectos..."

            De Otro Modo:
				Escribir "Opción inválida. Por favor, seleccione una de las tres opciones."
				Escribir ""
        FinSegun
        
    Hasta Que opcion = 3
FinAlgoritmo
