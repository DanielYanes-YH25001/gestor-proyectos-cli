from modules.ui import prompt_input, error


def validar_entrada(mensaje):
  """
  Solicita un valor al usuario y valida que no esté vacío.
  
  Args:
    mensaje (str): Mensaje a mostrar al usuario
    
  Returns:
    str: Valor ingresado por el usuario (sin espacios en blanco al inicio/final)
  """
  
  while True:
    valor = prompt_input(mensaje).strip()
    if valor:
      return valor
    error("El campo no puede estar vacío. Intente de nuevo.")
