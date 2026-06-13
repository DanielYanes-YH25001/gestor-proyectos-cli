from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

console = Console()


def render_header(title):
  """
  Renderiza un encabezado decorado en la terminal

  Args:
    title (str): Título del encabezado
  """

  console.print(
    Panel(
      Text(title, justify = "center", style = "bold white"),
      style = "blue",
      expand = False
    )
  )


def render_menu(title, options):
  """
  Muestra un menú de opciones numeradas

  Args:
    title (str): Título del menú
    options (list[str]): Lista de opciones a mostrar
  """

  table = Table(show_header = False, box = box.SIMPLE, pad_edge = False)
  table.add_column("Opción", style = "bold cyan")
  table.add_column("Descripción", style = "white")

  for index, option in enumerate(options, 1):
    table.add_row(str(index), option)

  console.print(Panel(table, title = f"[b]{title}[/]", border_style = "bright_blue"))


def render_table(columns, rows, title = None):
  """
  Renderiza una tabla con las filas y columnas dadas

  Args:
    columns (list[str]): Lista de columnas
    rows (list[str]): Lista de filas
    title (str): Título de la tabla
  """

  table = Table(show_header = True, header_style = "bold magenta")
  for column in columns:
    table.add_column(column)

  for row in rows:
    table.add_row(*[str(cell) for cell in row])

  if title is not None:
    console.print(Panel(table, title = f"[b]{title}[/]", border_style = "bright_blue"))
  else:
    console.print(table)


def info(message):
  """
  Imprime un mensaje en color cyan

  Args:
    message (str): Mensaje a imprimir
  """
  console.print(f"[cyan]{message}[/]")


def success(message):
  """
  Imprime un mensaje en color verde

  Args:
    message (str): Mensaje a imprimir
  """
  console.print(f"[green]{message}[/]")


def warn(message):
  """
  Imprime un mensaje en color amarillo

  Args:
    message (str): Mensaje a imprimir
  """
  console.print(f"[yellow]{message}[/]")


def error(message):
  """
  Imprime un mensaje en negrita de color rojo

  Args:
    message (str): Mensaje a imprimir
  """
  console.print(f"[bold red]{message}[/]")


def prompt_input(label, default = None):
  """
  Renderiza una entrada para el usuario, con un texto y valor por defecto dado

  Args:
    label (str): Texto para entrada
    default (str): Valor por defecto que tomará la entrada en caso no se brinde ninguno
  """

  if default is not None:
    return Prompt.ask(f"[bold green]{label}[/]", default = default)
  return Prompt.ask(f"[bold green]{label}[/]")
