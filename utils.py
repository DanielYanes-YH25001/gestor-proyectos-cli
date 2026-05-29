from modules.ui import prompt_input, error


def validar_entrada(mensaje):
  while True:
    valor = prompt_input(mensaje).strip()
    if valor:
      return valor
    error("El campo no puede estar vacío. Intente de nuevo.")
