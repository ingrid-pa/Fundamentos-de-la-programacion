# entrada.py
# Funciones para leer datos del teclado con control de errores.
# Si el usuario escribe letras donde se espera un número, se captura
# la excepción ValueError y se vuelve a pedir el dato.

import constantes as c


def leer_entero(mensaje: str, minimo: int = 0) -> int:
    """Pide un número entero mayor o igual que 'minimo' hasta que sea válido."""
    while True:
        try:
            numero = int(input(mensaje))
            if numero < minimo:
                print(f"Error: el número debe ser {minimo} o mayor.")
            else:
                return numero
        except ValueError:
            print("Error: debes escribir un número entero (sin letras ni decimales).")


def leer_decimal(mensaje: str, minimo: float = 0.0) -> float:
    """Pide un número decimal mayor o igual que 'minimo'.
    Acepta coma o punto decimal (2,50 o 2.50)."""
    while True:
        try:
            numero = float(input(mensaje).replace(",", "."))
            if numero < minimo:
                print(f"Error: el número debe ser {minimo} o mayor.")
            else:
                return numero
        except ValueError:
            print("Error: debes escribir un número (por ejemplo 2,50).")


def leer_texto(mensaje: str) -> str:
    """Pide un texto no vacío que no contenga el separador del CSV."""
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("Error: el texto no puede estar vacío.")
        elif c.SEPARADOR in texto:
            print(f"Error: el texto no puede contener el carácter '{c.SEPARADOR}'.")
        else:
            return texto
