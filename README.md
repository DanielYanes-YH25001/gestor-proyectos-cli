# Gestor de Proyectos Simple - Aplicación CLI

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Rich](https://img.shields.io/badge/rich-15.0.0-blue.svg)](https://pypi.org/project/rich/)
[![Contributors](https://img.shields.io/github/contributors/DanielYanes-YH25001/gestor-proyectos-cli.svg)](https://github.com/DanielYanes-YH25001/gestor-proyectos-cli/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/DanielYanes-YH25001/gestor-proyectos-cli.svg?style=social)](https://github.com/DanielYanes-YH25001/gestor-proyectos-cli/stargazers)

**Universidad de El Salvador - Facultad Multidisciplinaria de Occidente**

**Carrera:** Ingeniería en Desarrollo de Software.

**Asignatura:** Lógica de Programación.

## Descripción del Proyecto

Esta es una aplicación de Interfaz de Línea de Comandos (CLI) desarrollada con Python. El objetivo principal del sistema es funcionar como un gestor de proyectos donde se puedan administrar múltiples tareas asignadas a diferentes empleados.

## Lógica de Negocio

- Un proyecto contiene varias tareas que se pueden delegar a diferentes empleados.
- El sistema permite registrar la cantidad de horas trabajadas por los empleados en cada tarea específica.
- Se incluye la funcionalidad para calcular el total de horas invertidas, ya sea filtrando por tarea individual o por proyecto completo.
- Se agregan validaciones de seguridad para evitar que se ingresen datos erróneos, como impedir que un empleado registre jornadas irreales, como por ejemplo más de 12 horas en un solo día o valores negativos.

## Estado del Proyecto

Actualmente primera versión del proyecto **completada ✅**. Para la tercera entrega se implementan nuevas funcionalidades para tener un gestor más robusto. Además se agrega persistencia de datos como lo son el registro de proyectos, empleados, tareas y asignaciones, y se implementa una nueva UI mejorada con la librería Rich de Python.

## Tecnologías

| Lenguaje   | Librerías                              | Diseño Lógico          | Control de Versiones |
| ---------- | -------------------------------------- | ---------------------- | -------------------- |
| Python 3.x | [Rich](https://pypi.org/project/rich/) | Pseudocódigo en PSeInt | Git y GitHub         |

## Integrantes del Equipo

- Daniel Eduardo Yanes Hércules - YH25001
- Alexis Jonathan Mazariego Mazariego - MM24002
- Wilbert Adalberto Martinez Trejo - MT23002

## Instrucciones de Ejecución

### Requisitos Previos

- Python 3.x instalado en tu sistema
- pip (gestor de paquetes de Python)

### Instalación y Configuración del Entorno

#### 1. Clonar el repositorio:

```bash
git clone https://github.com/DanielYanes-YH25001/gestor-proyectos-cli.git
cd gestor-proyectos-cli
```

#### 2. Crear un entorno virtual

- En Linux/macOS:

  ```bash
  python3 -m venv env
  ```

- En Windows (PowerShell y CMD):

  ```PowerShell
  python -m venv env
  ```

> Como ejemplo se ha utilizado el nombre `env` para el entorno virtual. Puedes utilizar el nombre que prefieras.

#### 3. Activar el entorno virtual

- En Linux/macOS:

  ```bash
  source env/bin/activate
  ```

- En Windows (PowerShell):

  ```powershell
  .\env\Scripts\activate
  ```

  o también:

  ```powershell
  .\env\Scripts\Activate.ps1
  ```

  Si se lanza algún error abrir PowerShell como administrador y ejecutar:

  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

  Esto le indicará a PowerShell que permita la ejecución de scripts para el usuario actual del sistema. Presiona <kbd>S</kbd> + <kbd>Enter</kbd> para confirmar, y vuelve a intentar activar el entorno virtual.

- En Windows (CMD):

  ```cmd
  .\env\Scripts\activate
  ```

  o también:

  ```cmd
  .\env\Scripts\activate.bat
  ```

Notarás que el entorno virtual se ha activado con éxito cuando en el prompt de la terminal se muestre entre paréntesis el nombre de tu entorno virtual `(env)`.

#### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar el Gestor de Proyectos

Para iniciar la aplicación CLI del gestor de proyectos, ejecuta:

```bash
python main.py
```

Esto abrirá el menú principal donde podrás realizar operaciones como crear proyectos, registrar empleados, asignar tareas y registrar horas de trabajo.

### Ejecutar las Pruebas Unitarias

Las pruebas unitarias del proyecto se encuentran en la carpeta `tests/`. Para ejecutarlas utiliza el módulo `unittest` de Python:

#### 1. Ejecutar todas las pruebas

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

#### 2. Ejecutar un archivo de pruebas específico

```bash
python -m unittest tests.test_proyectos -v
python -m unittest tests.test_empleados -v
python -m unittest tests.test_tareas -v
python -m unittest tests.test_asignaciones -v
python -m unittest tests.test_persistence -v
```

#### 3. Ejecutar una prueba específica:

```bash
python -m unittest tests.test_proyectos.ProyectosTests.test_nombre_de_metodo -v
```

> El parámetro `-v` (verbose) proporciona una salida detallada de las pruebas. Para ejecuciones sin muchos detalles omite este parámetro.

### Medir la Cobertura de Pruebas

Para medir la cobertura de las pruebas unitarias y ver qué porcentaje del código está siendo probado, utiliza la herramienta `coverage`:

#### 1. Ejecutar pruebas con medición de cobertura

```bash
coverage run --omit="tests/*" -m unittest discover -s tests -p "test_*.py"
```

#### 2. Ver el reporte de cobertura en la terminal

```bash
coverage report
```

#### 3. Generar un reporte HTML detallado

```bash
coverage html
```

Esto creará una carpeta `htmlcov/` con un reporte interactivo. Puedes abrir el archivo `htmlcov/index.html` en tu navegador para ver los detalles.

#### 4. Limpiar los datos de cobertura previos

```bash
coverage erase
```

> El parámetro `-v` no funciona con coverage. Si necesitas salida detallada de las pruebas, combina los comandos de forma alternativa.
