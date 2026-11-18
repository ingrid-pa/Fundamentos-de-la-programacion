# ficheros.py
# Persistencia: guarda y carga el inventario en un fichero CSV.
# Formato de cada línea:  nombre;precio;cantidad
# Se usa "with" para que el archivo se cierre siempre, aunque haya un error.

import constantes as c
from calculos import validar_stock


def cargar_inventario(ruta: str) -> list:
    """Lee el inventario desde el fichero CSV y devuelve una lista de productos.
    Si el fichero no existe, devuelve una lista vacía.
    Las líneas con errores se ignoran mostrando un aviso."""
    productos = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            num_linea = 0
            for linea in archivo:
                num_linea += 1
                linea = linea.strip()
                if linea == "":
                    continue
                try:
                    nombre, precio, cantidad = linea.split(c.SEPARADOR)
                    nombre = nombre.strip()
                    precio = float(precio)
                    cantidad = int(cantidad)
                    if nombre == "" or precio < 0 or not validar_stock(cantidad):
                        raise ValueError("valores fuera de rango")
                    productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
                except ValueError:
                    print(f"Aviso: la línea {num_linea} del fichero no es válida y se ignora.")
    except FileNotFoundError:
        print(f"No existe el fichero '{ruta}'. Se empieza con un inventario vacío.")
    except OSError as error:
        print(f"Error al leer el fichero: {error}")
    else:
        print(f"Inventario cargado: {len(productos)} productos.")
    return productos


def guardar_inventario(productos: list, ruta: str) -> bool:
    """Guarda la lista de productos en el fichero CSV (sobrescribe el anterior).
    Devuelve True si se ha guardado correctamente."""
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            for p in productos:
                archivo.write(f"{p['nombre']}{c.SEPARADOR}{p['precio']}{c.SEPARADOR}{p['cantidad']}\n")
        return True
    except OSError as error:
        print(f"Error al guardar el fichero: {error}")
        return False
