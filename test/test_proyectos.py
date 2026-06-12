import unittest
from unittest.mock import Mock

from services.proyecto_service import ProyectoService
from modules.persistence import ManejadorPersistencia
from models.proyecto import Proyecto


class ProyectosTests(unittest.TestCase):
  def setUp(self):
    """Configura el entorno inicial simulando la persistencia de datos"""

    self.mock_persistencia = Mock(spec=ManejadorPersistencia)
    self.proyecto_service = ProyectoService(self.mock_persistencia)

    self.lista_proyectos_iniciales = [
      {"id": 1, "nombre": "App de Turismo de El Salvador", "estado": "Activo"},
      {"id": 2, "nombre": "Diseño de Base de Datos para Tienda", "estado": "Activo"},
      {"id": 3, "nombre": "Dashboard de Ventas", "estado": "Activo"},
      {"id": 4, "nombre": "Sitio Web para Academia", "estado": "Activo"},
    ]

  def test_excepciones_creacion_modelo_proyecto(self):
    """Valida que el modelo lance errores ante datos inválidos"""

    with self.assertRaises(ValueError):
      Proyecto("1", "Sistema de asistencia por reconocimiento facial", "Activo")

    with self.assertRaises(ValueError):
      Proyecto(-999, "Sistema de asistencia por reconocimiento facial", "Activo")

    with self.assertRaises(ValueError):
      Proyecto(1, 999, "Activo")

    with self.assertRaises(ValueError):
      Proyecto(1, "Sistema de asistencia por reconocimiento facial", "Otro Estado")
  
  def test_str_representacion_modelo_proyecto(self):
    """Verifica que el texto representativo del proyecto sea correcto"""

    proyecto_creado = Proyecto(1, "Sistema de asistencia por reconocimiento facial", "Activo")
    
    self.assertEqual(
      proyecto_creado.__str__(),
      "Proyecto(id=1, nombre='Sistema de asistencia por reconocimiento facial', estado='Activo')"
    )

  def test_obtener_lista_proyectos(self):
    """Comprueba que el servicio liste todos los proyectos guardados"""

    self.mock_persistencia.cargar_datos.return_value = {
      "proyectos": self.lista_proyectos_iniciales,
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }

    resultado = self.proyecto_service.obtener_todos()

    self.assertEqual(
      [{"id": p.id, "nombre": p.nombre, "estado": p.estado} for p in resultado],
      self.lista_proyectos_iniciales,
    )
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_not_called()

  def test_agregar_nuevo_proyecto(self):
    """Verifica la inserción exitosa de un proyecto en persistencia"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos
    self.mock_persistencia.obtener_proximo_id.return_value = 5

    nuevo_proyecto = self.proyecto_service.crear("Aplicación para Viajes", "Activo")

    self.assertEqual(nuevo_proyecto.id, 5)
    self.assertEqual(nuevo_proyecto.nombre, "Aplicación para Viajes")
    self.assertEqual(nuevo_proyecto.estado, "Activo")
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["proyectos"]), 5)
    self.assertEqual(
      datos["proyectos"][-1],
      {
        "id": 5,
        "nombre": "Aplicación para Viajes",
        "estado": "Activo"
      }
    )

  def test_actualizar_proyecto(self):
    """Confirma la modificación correcta de un proyecto por ID"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.proyecto_service.actualizar(4, "Videojuego Shooter", "Activo")

    self.assertTrue(actualizado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(
      datos["proyectos"][3]["nombre"],
      "Videojuego Shooter"
    )
    self.assertEqual(
      datos["proyectos"][3]["estado"],
      "Activo"
    )

  def test_eliminar_proyecto(self):
    """Comprueba el borrado exitoso de un proyecto existente"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    eliminado = self.proyecto_service.eliminar(4)

    self.assertTrue(eliminado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["proyectos"]), 3)
    self.assertFalse(any(p["id"] == 4 for p in datos["proyectos"]))

  def test_obtener_por_id_proyecto(self):
    """Valida la búsqueda correcta de proyecto usando su ID"""
    
    self.mock_persistencia.cargar_datos.return_value = {
      "proyectos": self.lista_proyectos_iniciales,
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }

    resultado = self.proyecto_service.obtener_por_id(1)

    self.assertIsNotNone(resultado)
    self.assertEqual(resultado.id, 1)
    self.assertEqual(resultado.nombre, "App de Turismo de El Salvador")

  def test_obtener_por_id_proyecto_no_existe(self):
    """Asegura que devuelva None buscando un ID no registrado"""

    self.mock_persistencia.cargar_datos.return_value = {
      "proyectos": self.lista_proyectos_iniciales,
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }

    resultado = self.proyecto_service.obtener_por_id(999)

    self.assertIsNone(resultado)

  def test_actualizar_proyecto_solo_nombre(self):
    """Modifica parcialmente el proyecto cambiando solamente su nombre actual"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.proyecto_service.actualizar(1, "Nuevo Nombre")

    self.assertTrue(actualizado)
    self.assertEqual(datos["proyectos"][0]["nombre"], "Nuevo Nombre")
    self.assertEqual(datos["proyectos"][0]["estado"], "Activo")

  def test_actualizar_proyecto_solo_estado(self):
    """Modifica parcialmente el proyecto cambiando solamente su estado actual"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.proyecto_service.actualizar(1, estado="Pausado")

    self.assertTrue(actualizado)
    self.assertEqual(datos["proyectos"][0]["nombre"], "App de Turismo de El Salvador")
    self.assertEqual(datos["proyectos"][0]["estado"], "Pausado")

  def test_actualizar_proyecto_nombre_vacio(self):
    """Rechaza la actualización si asignas un nombre vacío"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.proyecto_service.actualizar(1, "")

  def test_actualizar_proyecto_nombre_no_string(self):
    """Evita actualizar nombres usando tipos de datos inválidos"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.proyecto_service.actualizar(1, 123)

  def test_actualizar_proyecto_estado_invalido(self):
    """Deniega actualizaciones si usas estados no permitidos textualmente"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.proyecto_service.actualizar(1, estado="Invalido")

  def test_actualizar_proyecto_no_existe(self):
    """Retorna False intentando actualizar un ID no existente"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.proyecto_service.actualizar(999, "Nuevo Nombre")

    self.assertFalse(resultado)

  def test_eliminar_proyecto_no_existe(self):
    """Retorna False intentando eliminar un ID no existente"""
    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [],
      "asignaciones": [],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.proyecto_service.eliminar(999)

    self.assertFalse(resultado)

  def test_eliminar_proyecto_con_tareas_y_asignaciones(self):
    """Garantiza el borrado en cascada de dependencias vinculadas"""

    datos = {
      "proyectos": list(self.lista_proyectos_iniciales),
      "empleados": [],
      "tareas": [
        {"id": 1, "id_proyecto": 1, "descripcion": "Tarea 1"},
        {"id": 2, "id_proyecto": 1, "descripcion": "Tarea 2"},
      ],
      "asignaciones": [
        {"id": 1, "id_tarea": 1, "id_empleado": 1, "horas": 5},
        {"id": 2, "id_tarea": 2, "id_empleado": 1, "horas": 3},
      ],
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    eliminado = self.proyecto_service.eliminar(1)

    self.assertTrue(eliminado)
    self.assertEqual(len(datos["proyectos"]), 3)
    self.assertEqual(len(datos["tareas"]), 0)
    self.assertEqual(len(datos["asignaciones"]), 0)


if __name__ == "__main__":
  unittest.main()