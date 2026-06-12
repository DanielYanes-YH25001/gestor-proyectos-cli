import unittest
import json
import tempfile
from pathlib import Path

from modules.persistence import ManejadorPersistencia


class PersistenceTests(unittest.TestCase):
  def setUp(self):
    self.temp_dir = tempfile.TemporaryDirectory()
    self.temp_path = Path(self.temp_dir.name) / "test_data.json"

  def tearDown(self):
    self.temp_dir.cleanup()

  def test_cargar_datos_archivo_existe(self):
    datos_iniciales = {
      "proyectos": [{"id": 1, "nombre": "Proyecto 1", "estado": "Activo"}],
      "empleados": [{"id": 1, "nombre": "Juan", "rol": "Dev"}],
      "tareas": [{"id": 1, "id_proyecto": 1, "descripcion": "Tarea 1"}],
      "asignaciones": [{"id": 1, "id_tarea": 1, "id_empleado": 1, "horas": 5.0}]
    }

    with open(self.temp_path, "w", encoding = "utf-8") as f:
      json.dump(datos_iniciales, f)

    manejador = ManejadorPersistencia(self.temp_path)
    datos = manejador.cargar_datos()

    self.assertEqual(len(datos["proyectos"]), 1)
    self.assertEqual(len(datos["empleados"]), 1)
    self.assertEqual(len(datos["tareas"]), 1)
    self.assertEqual(len(datos["asignaciones"]), 1)

  def test_cargar_datos_archivo_no_existe(self):
    manejador = ManejadorPersistencia(self.temp_path)
    datos = manejador.cargar_datos()

    self.assertEqual(datos["proyectos"], [])
    self.assertEqual(datos["empleados"], [])
    self.assertEqual(datos["tareas"], [])
    self.assertEqual(datos["asignaciones"], [])
    self.assertTrue(self.temp_path.exists())

  def test_guardar_datos(self):
    manejador = ManejadorPersistencia(self.temp_path)
    datos = {
      "proyectos": [{"id": 1, "nombre": "Proyecto 1", "estado": "Activo"}],
      "empleados": [{"id": 1, "nombre": "Juan", "rol": "Dev"}],
      "tareas": [{"id": 1, "id_proyecto": 1, "descripcion": "Tarea 1"}],
      "asignaciones": [{"id": 1, "id_tarea": 1, "id_empleado": 1, "horas": 5.0}]
    }

    manejador.guardar_datos(datos)

    with open(self.temp_path, "r", encoding = "utf-8") as f:
      contenido = json.load(f)

    self.assertEqual(len(contenido["proyectos"]), 1)
    self.assertEqual(contenido["proyectos"][0]["nombre"], "Proyecto 1")

  def test_guardar_datos_parciales(self):
    manejador = ManejadorPersistencia(self.temp_path)
    datos_parciales = {
      "proyectos": [{"id": 1, "nombre": "Proyecto 1", "estado": "Activo"}],
      "empleados": [],
      "tareas": [],
      "asignaciones": []
    }

    manejador.guardar_datos(datos_parciales)

    with open(self.temp_path, "r", encoding = "utf-8") as f:
      contenido = json.load(f)

    self.assertEqual(len(contenido["proyectos"]), 1)
    self.assertEqual(len(contenido["empleados"]), 0)

  def test_obtener_proximo_id_lista_vacia(self):
    manejador = ManejadorPersistencia(self.temp_path)
    resultado = manejador.obtener_proximo_id([])

    self.assertEqual(resultado, 1)

  def test_obtener_proximo_id_lista_no_vacia(self):
    manejador = ManejadorPersistencia(self.temp_path)
    lista = [
      {"id": 1, "nombre": "Item 1"},
      {"id": 3, "nombre": "Item 3"},
      {"id": 2, "nombre": "Item 2"}
    ]
    resultado = manejador.obtener_proximo_id(lista)

    self.assertEqual(resultado, 4)

  def test_crear_archivo_vacio(self):
    manejador = ManejadorPersistencia(self.temp_path)
    manejador._crear_archivo_vacio()

    self.assertTrue(self.temp_path.exists())

    with open(self.temp_path, "r", encoding = "utf-8") as f:
      contenido = json.load(f)

    self.assertEqual(contenido["proyectos"], [])
    self.assertEqual(contenido["empleados"], [])
    self.assertEqual(contenido["tareas"], [])
    self.assertEqual(contenido["asignaciones"], [])

  def test_cargar_datos_archivo_incompleto(self):
    datos_incompletos = {
      "proyectos": [{"id": 1, "nombre": "Proyecto 1", "estado": "Activo"}]
    }

    with open(self.temp_path, "w", encoding = "utf-8") as f:
      json.dump(datos_incompletos, f)

    manejador = ManejadorPersistencia(self.temp_path)
    datos = manejador.cargar_datos()

    self.assertEqual(len(datos["proyectos"]), 1)
    self.assertEqual(datos["empleados"], [])
    self.assertEqual(datos["tareas"], [])
    self.assertEqual(datos["asignaciones"], [])


if __name__ == "__main__":
  unittest.main()
