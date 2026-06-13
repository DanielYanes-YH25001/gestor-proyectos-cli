import unittest
from unittest.mock import Mock

from services.tarea_service import TareaService
from modules.persistence import ManejadorPersistencia
from models.tarea import Tarea


class TareasTests(unittest.TestCase):
  def setUp(self):
    self.mock_persistencia = Mock(spec = ManejadorPersistencia)
    self.service = TareaService(self.mock_persistencia)

    self.lista_tareas_iniciales = [
      {"id": 1, "id_proyecto": 1, "descripcion": "Diseñar esquema preliminar de base de datos"},
      {"id": 2, "id_proyecto": 1, "descripcion": "Crear modelo lógico"},
      {"id": 3, "id_proyecto": 2, "descripcion": "Probar endpoint"}
    ]

  def test_excepciones_creacion_modelo_tarea(self):
    with self.assertRaises(ValueError):
      Tarea("1", 1, "Elaborar estructura de carpetas y archivos")

    with self.assertRaises(ValueError):
      Tarea(-999, 1, "Elaborar estructura de carpetas y archivos")

    with self.assertRaises(ValueError):
      Tarea(1, "1", "Elaborar estructura de carpetas y archivos")

    with self.assertRaises(ValueError):
      Tarea(1, -999, "Elaborar estructura de carpetas y archivos")

    with self.assertRaises(ValueError):
      Tarea(1, 1, None)

    with self.assertRaises(ValueError):
      Tarea(1, 1, 999)

  def test_str_representacion_modelo_tarea(self):
    tarea_creada = Tarea(1, 1, "Elaborar estructura de carpetas y archivos")

    self.assertEqual(
      tarea_creada.__str__(),
      "Tarea(id=1, id_proyecto=1, descripcion='Elaborar estructura de carpetas y archivos')"
    )

  def test_obtener_todas_las_tareas(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": self.lista_tareas_iniciales,
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_todos()

    self.assertEqual(
      [
        {
          "id": t.id,
          "id_proyecto": t.id_proyecto,
          "descripcion": t.descripcion
        }
        for t in resultado
      ],
      self.lista_tareas_iniciales
    )
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_not_called()

  def test_crear_tarea(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": list(self.lista_tareas_iniciales),
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos
    self.mock_persistencia.obtener_proximo_id.return_value = 4

    tarea = self.service.crear(2, "Documentar API")

    self.assertEqual(tarea.id, 4)
    self.assertEqual(tarea.id_proyecto, 2)
    self.assertEqual(tarea.descripcion, "Documentar API")
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["tareas"]), 4)
    self.assertEqual(
      datos["tareas"][-1],
      {"id": 4, "id_proyecto": 2, "descripcion": "Documentar API"}
    )

  def test_actualizar_tarea(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": list(self.lista_tareas_iniciales),
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    actualizado = self.service.actualizar(3, "Probar endpoints de la REST API")

    self.assertTrue(actualizado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(
      datos["tareas"][2]["descripcion"],
      "Probar endpoints de la REST API"
    )

  def test_eliminar_tarea(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": list(self.lista_tareas_iniciales),
      "asignaciones": [
        {"id": 1, "id_tarea": 3, "id_empleado": 1, "horas": 5.0},
        {"id": 2, "id_tarea": 1, "id_empleado": 2, "horas": 3.0}
      ]
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    eliminado = self.service.eliminar(3)

    self.assertTrue(eliminado)
    self.mock_persistencia.cargar_datos.assert_called_once()
    self.mock_persistencia.guardar_datos.assert_called_once()
    self.assertEqual(len(datos["tareas"]), 2)
    self.assertFalse(any(t["id"] == 3 for t in datos["tareas"]))
    self.assertFalse(
      any(a["id_tarea"] == 3 for a in datos["asignaciones"])
    )

  def test_obtener_por_id_tarea(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": self.lista_tareas_iniciales,
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_id(1)

    self.assertIsNotNone(resultado)
    self.assertEqual(resultado.id, 1)
    self.assertEqual(resultado.descripcion, "Diseñar esquema preliminar de base de datos")

  def test_obtener_por_id_tarea_no_existe(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": self.lista_tareas_iniciales,
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_id(999)

    self.assertIsNone(resultado)

  def test_obtener_por_proyecto(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": self.lista_tareas_iniciales,
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.obtener_por_proyecto(1)

    self.assertEqual(len(resultado), 2)
    self.assertTrue(all(t.id_proyecto == 1 for t in resultado))

  def test_actualizar_tarea_descripcion_vacia(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": list(self.lista_tareas_iniciales),
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar(1, "")

  def test_actualizar_tarea_descripcion_no_string(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": list(self.lista_tareas_iniciales),
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    with self.assertRaises(ValueError):
      self.service.actualizar(1, 123)

  def test_actualizar_tarea_no_existe(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": list(self.lista_tareas_iniciales),
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.actualizar(999, "Nueva descripción")

    self.assertFalse(resultado)

  def test_eliminar_tarea_no_existe(self):
    datos = {
      "proyectos": [],
      "empleados": [],
      "tareas": list(self.lista_tareas_iniciales),
      "asignaciones": []
    }
    self.mock_persistencia.cargar_datos.return_value = datos

    resultado = self.service.eliminar(999)

    self.assertFalse(resultado)


if __name__ == "__main__":
  unittest.main()
