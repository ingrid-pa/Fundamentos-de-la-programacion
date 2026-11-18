# main.py
# Programa principal: Motor de Gestión de Inventario.
# Muestra un menú en bucle (while) y ejecuta cada opción con match
# (equivalente al switch de otros lenguajes).
# Al arrancar carga el inventario del fichero y al salir lo guarda.

import constantes as c
import calculos
import ficheros
from entrada import leer_entero, leer_decimal, leer_texto


def mostrar_menu() -> None:
    """Muestra las opciones del menú principal."""
    print("\n===== GESTIÓN DE INVENTARIO =====")
    print("1. Listar productos")
    print("2. Añadir producto")
    print("3. Vender producto")
    print("4. Reponer stock")
    print("5. Modificar precio")
    print("6. Eliminar producto")
    print("7. Informe de stock")
    print("8. Guardar ahora")
    print("0. Guardar y salir")


def listar_productos(productos: list) -> None:
    """Muestra una tabla con todos los productos."""
    if len(productos) == 0:
        print("El inventario está vacío.")
        return
    print(f"\n{'Nº':<4}{'Producto':<22}{'Precio':>10}{'Con IVA':>10}{'Stock':>8}")
    print("-" * 54)
    for i, p in enumerate(productos, start=1):
        print(f"{i:<4}{p['nombre']:<22}{p['precio']:>9.2f}€"
              f"{calculos.precio_con_iva(p['precio']):>9.2f}€{p['cantidad']:>8}")


def anadir_producto(productos: list) -> None:
    """Pide los datos de un producto nuevo y lo añade a la lista."""
    nombre = leer_texto("Nombre del producto: ")
    if calculos.buscar_producto(productos, nombre) != -1:
        print("Ya existe un producto con ese nombre. Usa 'Reponer stock'.")
        return
    precio = leer_decimal("Precio sin IVA (€): ")
    cantidad = leer_entero("Cantidad inicial: ")
    productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
    print(f"Producto '{nombre}' añadido.")


def pedir_producto_existente(productos: list) -> int:
    """Pide un nombre y devuelve la posición del producto, o -1 si no existe."""
    nombre = leer_texto("Nombre del producto: ")
    posicion = calculos.buscar_producto(productos, nombre)
    if posicion == -1:
        print(f"No existe ningún producto llamado '{nombre}'.")
    return posicion


def vender_producto(productos: list) -> None:
    """Registra una venta: valida stock, aplica descuento e IVA y resta unidades."""
    posicion = pedir_producto_existente(productos)
    if posicion == -1:
        return
    producto = productos[posicion]
    unidades = leer_entero(f"Unidades a vender (disponibles: {producto['cantidad']}): ", 1)

    if not calculos.hay_stock_suficiente(producto["cantidad"], unidades):
        print("No hay stock suficiente para esta venta.")
        return

    subtotal = producto["precio"] * unidades
    descuento = calculos.calcular_descuento(unidades)
    total = calculos.calcular_total_venta(producto["precio"], unidades)

    print("\n--- Ticket ---")
    print(f"{unidades} x {producto['nombre']} a {producto['precio']:.2f}€ = {subtotal:.2f}€")
    if descuento > 0:
        print(f"Descuento por volumen: {descuento * 100:.0f}%")
    print(f"IVA ({c.IVA * 100:.0f}%) incluido")
    print(f"TOTAL A PAGAR: {total:.2f}€")

    producto["cantidad"] -= unidades
    if producto["cantidad"] < c.STOCK_MINIMO:
        print(f"Atención: quedan solo {producto['cantidad']} unidades de {producto['nombre']}.")


def reponer_stock(productos: list) -> None:
    """Suma unidades al stock de un producto."""
    posicion = pedir_producto_existente(productos)
    if posicion == -1:
        return
    unidades = leer_entero("Unidades a añadir: ", 1)
    productos[posicion]["cantidad"] += unidades
    print(f"Stock actualizado: {productos[posicion]['cantidad']} unidades.")


def modificar_precio(productos: list) -> None:
    """Cambia el precio (sin IVA) de un producto."""
    posicion = pedir_producto_existente(productos)
    if posicion == -1:
        return
    productos[posicion]["precio"] = leer_decimal("Nuevo precio sin IVA (€): ")
    print("Precio actualizado.")


def eliminar_producto(productos: list) -> None:
    """Elimina un producto del inventario tras pedir confirmación."""
    posicion = pedir_producto_existente(productos)
    if posicion == -1:
        return
    confirmacion = input(f"¿Seguro que quieres eliminar '{productos[posicion]['nombre']}'? (s/n): ")
    if confirmacion.strip().lower() == "s":
        eliminado = productos.pop(posicion)
        print(f"Producto '{eliminado['nombre']}' eliminado.")
    else:
        print("Operación cancelada.")


def informe_stock(productos: list) -> None:
    """Muestra el valor total del almacén y los productos con stock bajo."""
    valor = calculos.calcular_valor_almacen(productos)
    total_unidades = 0
    for p in productos:
        total_unidades += p["cantidad"]

    print("\n===== INFORME DE STOCK =====")
    print(f"Productos distintos: {len(productos)}")
    print(f"Unidades totales:    {total_unidades}")
    print(f"Valor del almacén sin IVA: {valor:.2f}€")
    print(f"Valor del almacén con IVA: {calculos.precio_con_iva(valor):.2f}€")

    bajos = calculos.productos_stock_bajo(productos)
    if len(bajos) == 0:
        print("No hay productos con stock bajo.")
    else:
        print(f"\nProductos con stock bajo (menos de {c.STOCK_MINIMO} uds):")
        for p in bajos:
            print(f"  - {p['nombre']}: {p['cantidad']} uds")


def main() -> None:
    """Punto de entrada: carga datos, ejecuta el menú y guarda al salir."""
    productos = ficheros.cargar_inventario(c.RUTA_FICHERO)

    salir = False
    while not salir:
        mostrar_menu()
        opcion = leer_entero("Elige una opción: ")
        match opcion:
            case 1:
                listar_productos(productos)
            case 2:
                anadir_producto(productos)
            case 3:
                vender_producto(productos)
            case 4:
                reponer_stock(productos)
            case 5:
                modificar_precio(productos)
            case 6:
                eliminar_producto(productos)
            case 7:
                informe_stock(productos)
            case 8:
                if ficheros.guardar_inventario(productos, c.RUTA_FICHERO):
                    print("Inventario guardado.")
            case 0:
                if ficheros.guardar_inventario(productos, c.RUTA_FICHERO):
                    print("Inventario guardado. ¡Hasta pronto!")
                salir = True
            case _:
                print("Opción no válida. Elige un número del 0 al 8.")


# Solo se ejecuta main() si este archivo se lanza directamente
if __name__ == "__main__":
    main()
