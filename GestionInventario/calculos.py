# calculos.py
# Lógica de negocio: funciones de cálculo y validación.
# Todas reciben los datos por parámetro y devuelven un resultado,
# sin modificar variables globales.
#
# Cada producto se representa con un diccionario:
#   {"nombre": str, "precio": float, "cantidad": int}
# El precio se guarda SIN IVA.

import constantes as c


def calcular_iva(precio: float) -> float:
    """Devuelve el importe del IVA de un precio."""
    return precio * c.IVA


def precio_con_iva(precio: float) -> float:
    """Devuelve el precio con el IVA incluido."""
    return precio + calcular_iva(precio)


def calcular_descuento(unidades: int) -> float:
    """Devuelve el descuento (en tanto por uno) según las unidades compradas."""
    if unidades >= c.UNIDADES_DESCUENTO_3:
        return c.DESCUENTO_3
    elif unidades >= c.UNIDADES_DESCUENTO_2:
        return c.DESCUENTO_2
    elif unidades >= c.UNIDADES_DESCUENTO_1:
        return c.DESCUENTO_1
    else:
        return 0.0


def calcular_total_venta(precio_unitario: float, unidades: int) -> float:
    """Calcula el total de una venta: aplica el descuento por volumen y después el IVA."""
    subtotal = precio_unitario * unidades
    descuento = subtotal * calcular_descuento(unidades)
    return precio_con_iva(subtotal - descuento)


def validar_stock(cantidad: int) -> bool:
    """Comprueba que una cantidad de stock sea válida (no negativa)."""
    return cantidad >= 0


def hay_stock_suficiente(disponible: int, pedidas: int) -> bool:
    """Comprueba si hay unidades suficientes para atender un pedido."""
    return 0 < pedidas <= disponible


def calcular_valor_almacen(productos: list) -> float:
    """Recorre la lista y devuelve el valor total del almacén (sin IVA)."""
    total = 0.0
    for producto in productos:
        total += producto["precio"] * producto["cantidad"]
    return total


def buscar_producto(productos: list, nombre: str) -> int:
    """Devuelve la posición del producto con ese nombre, o -1 si no existe.
    No distingue mayúsculas de minúsculas."""
    for i in range(len(productos)):
        if productos[i]["nombre"].lower() == nombre.lower():
            return i
    return -1


def productos_stock_bajo(productos: list) -> list:
    """Devuelve una lista con los productos cuyo stock es inferior al mínimo."""
    bajos = []
    for producto in productos:
        if producto["cantidad"] < c.STOCK_MINIMO:
            bajos.append(producto)
    return bajos
