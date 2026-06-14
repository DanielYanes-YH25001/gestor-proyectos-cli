import unittest
from unittest.mock import Mock

from services.empleado_service import EmpleadoService
from modules.persistence import ManejadorPersistencia
from models.empleado import Empleado


class EmpleadosTests(unittest.TestCase):
  """
  Clase de pruebas unitarias para el servicio de empleados.
  Utiliza Mock para aislar las pruebas de la capa de persistencia (sin IO real).
  """

  def setUp(self):
    """
    Configuración inicial que se ejecuta antes de cada prueba.
    Crea un mock de ManejadorPersistencia y una instancia del servicio.
    """
    self.mock_persistencia = Mock(spec = ManejadorPersistencia)
    self.service = EmpleadoService(self.mock_persistencia)

    self.lista_empleados_iniciales = [
      {"id": 1, "nombre": "Ana Pérez", "rol": "Desarrollador"},
      {"id": 2, "nombre": "Luis Gómez", "rol": "Analista"}
    ]

  def test_excepciones_creacion_modelo_empleado(self):
    """
    Prueba que el modelo Empleado valide correctamente los parámetros.
    Debe lanzar ValueError cuando se proporcionan datos inválidos.
    """
    with self.assertRaises(ValueError):
      Empleado("1", "Daniel Yanes", "Cybersecurity Analyst")

    with self.assertRaises(ValueError):
      Empleado(-999, "Daniel Yanes", "Cybersecurity Analyst")

    with self.assertRaises(ValueError):
      Empleado(1, 999, "Cybersecurity Analyst")

    with self.assertRaises(ValueError):
      Empleado(1, "Daniel Yanes", 999)

  def test_str_representacion_modelo_empleado(self):
    """
    Prueba la representación en string del modelo Empleado.
    """
    empleado_creado = Empleado(1, "Daniel Yanes", "Cybersecurity Analyst")

    self.assertEqual(
      empleado_creado.__str__(),
      "Empleado(id=1, nombre='Daniel Yanes', rol='Cybersecurity Analyst')"
    )

  def test_obtener_todos_empleados(self):
    """
    Prueba la obtención de todos los empleados.
    Verifica que se carguen los datos correctamente y se retorne la lista completa.
    """
    datos = {
      "proyectos": [],
      "empleados": self.lista_empleados_iniciales,
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_todos()

    self.assertEqual(
      [{"id": e.id, "nombre": e.nombre, "rol": e.rol} for e in resultado],
      self.lista_empleados_iniciales
    )
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_not_called()

  def test_crear_empleado(self):
    """
    Prueba la creación de un nuevo empleado.
    Verifica que se genere un ID correcto y se guarde en la persistencia.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos
    self.mock_persistencia.obtener_proximo_id.return_value = 3

    empleado = self.service.crear("María López", "QA")

    self.assertEqual(empleado.id, 3)
    self.assertEqual(empleado.nombre, "María López")
    self.assertEqual(empleado.rol, "QA")
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["empleados"]), 3)
    self.assertEqual(
      datos["empleados"][-1],
      {"id": 3, "nombre": "María López", "rol": "QA"}
    )

  def test_actualizar_empleado(self):
    """
    Prueba la actualización completa de un empleado existente.
    Verifica que se actualicen tanto nombre como rol correctamente.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.service.actualizar(2, "Luis G.", "Líder")

    self.assertTrue(actualizado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(datos["empleados"][1]["nombre"], "Luis G.")
    self.assertEqual(datos["empleados"][1]["rol"], "Líder")

  def test_eliminar_empleado(self):
    """
    Prueba la eliminación de un empleado.
    Verifica que se elimine el empleado y todas sus asignaciones asociadas.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": [
        {"id": 1, "id_tarea": 1, "id_empleado": 2, "horas": 4.0},
        {"id": 2, "id_tarea": 2, "id_empleado": 1, "horas": 2.0}
      ]
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    eliminado = self.service.eliminar(2)

    self.assertTrue(eliminado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["empleados"]), 1)
    self.assertFalse(any(e["id"] == 2 for e in datos["empleados"]))
    self.assertFalse(
      any(a["id_empleado"] == 2 for a in datos["asignaciones"])
    )

  def test_obtener_por_id_empleado(self):
    """
    Prueba la obtención de un empleado por su ID cuando existe.
    """
    datos = {
      "proyectos": [],
      "empleados": self.lista_empleados_iniciales,
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_id(1)

    self.assertIsNotNone(resultado)
    self.assertEqual(resultado.id, 1)
    self.assertEqual(resultado.nombre, "Ana Pérez")

  def test_obtener_por_id_empleado_no_existe(self):
    """
    Prueba la obtención de un empleado por ID cuando no existe.
    Debe retornar None
    """
    datos = {
      "proyectos": [],
      "empleados": self.lista_empleados_iniciales,
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_id(999)

    self.assertIsNone(resultado)

  def test_actualizar_empleado_solo_nombre(self):
    """
    Prueba la actualización parcial de un empleado (solo nombre).
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.service.actualizar(1, "Nuevo Nombre")

    self.assertTrue(actualizado)
    self.assertEqual(datos["empleados"][0]["nombre"], "Nuevo Nombre")
    self.assertEqual(datos["empleados"][0]["rol"], "Desarrollador")

  def test_actualizar_empleado_solo_rol(self):
    """
    Prueba la actualización parcial de un empleado (solo rol).
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.service.actualizar(1, rol="Nuevo Rol")

    self.assertTrue(actualizado)
    self.assertEqual(datos["empleados"][0]["nombre"], "Ana Pérez")
    self.assertEqual(datos["empleados"][0]["rol"], "Nuevo Rol")

  def test_actualizar_empleado_nombre_vacio(self):
    """
    Prueba que no se pueda actualizar con nombre vacío.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar(1, "")

  def test_actualizar_empleado_nombre_no_string(self):
    """
    Prueba que no se pueda actualizar con nombre que no sea string.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar(1, 123)

  def test_actualizar_empleado_rol_vacio(self):
    """
    Prueba que no se pueda actualizar con rol vacío.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar(1, rol="")

  def test_actualizar_empleado_rol_no_string(self):
    """
    Prueba que no se pueda actualizar con rol que no sea string.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar(1, rol=123)

  def test_actualizar_empleado_no_existe(self):
    """
    Prueba la actualización de un empleado que no existe.
    Debe retornar False.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.actualizar(999, "Nuevo Nombre")

    self.assertFalse(resultado)

  def test_eliminar_empleado_no_existe(self):
    """
    Prueba la eliminación de un empleado que no existe.
    Debe retornar False.
    """
    datos = {
      "proyectos": [],
      "empleados": list(self.lista_empleados_iniciales),
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.eliminar(999)

    self.assertFalse(resultado)


if __name__ == "__main__":
  unittest.main()