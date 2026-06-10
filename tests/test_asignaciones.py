import unittest
from unittest.mock import Mock

from services.asignacion_service import AsignacionService
from modules.persistence import ManejadorPersistencia
from models.asignacion import Asignacion


class AsignacionesTests(unittest.TestCase):
  def setUp(self):
    self.mock_persistencia = Mock(spec = ManejadorPersistencia)
    self.service = AsignacionService(self.mock_persistencia)

    self.lista_asignaciones_iniciales = [
      {"id": 1, "id_tarea": 1, "id_empleado": 1, "horas": 4.0},
      {"id": 2, "id_tarea": 2, "id_empleado": 2, "horas": 3.5}
    ]
  
  def test_excepciones_creacion_modelo_asignacion(self):
    with self.assertRaises(ValueError):
      Asignacion("1", 1, 1, 5)

    with self.assertRaises(ValueError):
      Asignacion(-999, 1, 1, 5)

    with self.assertRaises(ValueError):
      Asignacion(1, "1", 1, 5)

    with self.assertRaises(ValueError):
      Asignacion(1, -999, 1, 5)

    with self.assertRaises(ValueError):
      Asignacion(1, 1, "1", 5)

    with self.assertRaises(ValueError):
      Asignacion(1, 1, -999, 5)

    with self.assertRaises(ValueError):
      Asignacion(1, 1, 1, "5")

  def test_str_representacion_modelo_asignacion(self):
    asignacion_creada = Asignacion(1, 1, 1, 5)
    
    self.assertEqual(
      asignacion_creada.__str__(),
      "Asignacion(id=1, id_tarea=1, id_empleado=1, horas=5.0)"
    )

  def test_obtener_todas_las_asignaciones(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": self.lista_asignaciones_iniciales
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_todos()

    self.assertEqual(
      [
        {
          "id": a.id,
          "id_tarea": a.id_tarea,
          "id_empleado": a.id_empleado,
          "horas": a.horas
        }
        for a in resultado
      ],
      self.lista_asignaciones_iniciales
    )
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_not_called()

  def test_crear_asignacion(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos
    self.mock_persistencia.obtener_proximo_id.return_value = 3

    asignacion = self.service.crear(3, 2)

    self.assertEqual(asignacion.id, 3)
    self.assertEqual(asignacion.id_tarea, 3)
    self.assertEqual(asignacion.id_empleado, 2)
    self.assertEqual(asignacion.horas, 0.0)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["asignaciones"]), 3)
    self.assertEqual(
      datos["asignaciones"][-1],
      {"id": 3, "id_tarea": 3, "id_empleado": 2, "horas": 0.0}
    )

  def test_agregar_horas_a_asignacion_existente(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.agregar_horas(1, 1, 2.5)

    self.assertTrue(resultado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(datos["asignaciones"][0]["horas"], 6.5)

  def test_actualizar_horas_de_asignacion(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.service.actualizar_horas(2, 5)

    self.assertTrue(actualizado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(datos["asignaciones"][1]["horas"], 5.0)

  def test_eliminar_asignacion(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    eliminado = self.service.eliminar(1)

    self.assertTrue(eliminado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["asignaciones"]), 1)
    self.assertFalse(any(a["id"] == 1 for a in datos["asignaciones"]))

  def test_obtener_por_id_asignacion(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": self.lista_asignaciones_iniciales
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_id(1)

    self.assertIsNotNone(resultado)
    self.assertEqual(resultado.id, 1)
    self.assertEqual(resultado.id_tarea, 1)
    self.assertEqual(resultado.id_empleado, 1)

  def test_obtener_por_id_asignacion_no_existe(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": self.lista_asignaciones_iniciales
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_id(999)

    self.assertIsNone(resultado)

  def test_obtener_por_tarea(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": self.lista_asignaciones_iniciales
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_tarea(1)

    self.assertEqual(len(resultado), 1)
    self.assertEqual(resultado[0].id_tarea, 1)

  def test_obtener_por_tarea_y_empleado(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": self.lista_asignaciones_iniciales
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_tarea_y_empleado(1, 1)

    self.assertIsNotNone(resultado)
    self.assertEqual(resultado.id_tarea, 1)
    self.assertEqual(resultado.id_empleado, 1)

  def test_obtener_por_tarea_y_empleado_no_existe(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": self.lista_asignaciones_iniciales
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_tarea_y_empleado(999, 999)

    self.assertIsNone(resultado)

  def test_obtener_por_empleado(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": self.lista_asignaciones_iniciales
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_empleado(1)

    self.assertEqual(len(resultado), 1)
    self.assertEqual(resultado[0].id_empleado, 1)

  def test_agregar_horas_horas_no_es_numero(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.agregar_horas(1, 1, "abc")

  def test_agregar_horas_horas_negativas(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.agregar_horas(1, 1, -1)

  def test_agregar_horas_horas_mayores_a_12(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.agregar_horas(1, 1, 13)

  def test_agregar_horas_excede_limite_diario(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": [{"id": 1, "id_tarea": 1, "id_empleado": 1, "horas": 10.0}]
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.agregar_horas(1, 1, 13)

  def test_agregar_horas_nueva_asignacion(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos
    self.mock_persistencia.obtener_proximo_id.return_value = 1

    resultado = self.service.agregar_horas(1, 1, 5)

    self.assertTrue(resultado)
    self.assertEqual(len(datos["asignaciones"]), 1)

  def test_actualizar_horas_horas_no_es_numero(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar_horas(1, "abc")

  def test_actualizar_horas_horas_negativas(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar_horas(1, -1)

  def test_actualizar_horas_horas_mayores_a_12(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar_horas(1, 13)

  def test_actualizar_horas_asignacion_no_existe(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.actualizar_horas(999, 5)

    self.assertFalse(resultado)

  def test_eliminar_asignacion_no_existe(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": [],
      "asignaciones": list(self.lista_asignaciones_iniciales)
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    eliminado = self.service.eliminar(999)

    self.assertFalse(eliminado)


if __name__ == "__main__":
  unittest.main()
