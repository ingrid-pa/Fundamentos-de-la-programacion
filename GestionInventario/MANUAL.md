# Manual de uso — Motor de Gestión de Inventario

Aplicación de consola en Python para gestionar el inventario de una pequeña tienda:
calcula precios con IVA, aplica descuentos por volumen, valida existencias, genera
informes de stock y guarda los datos en un fichero CSV.

## Requisitos

- Python 3.10 o superior (el menú usa `match`).

## Cómo ejecutarlo

Abre una terminal en la carpeta del proyecto y escribe:

```
python main.py
```

(En Linux/Mac puede ser `python3 main.py`.)

Al arrancar, el programa carga automáticamente `inventario.csv`. Si el fichero no
existe, avisa y empieza con un inventario vacío.

## Estructura del proyecto

| Archivo          | Contenido |
|------------------|-----------|
| `main.py`        | Programa principal: menú (`while` + `match`) y una función por opción. |
| `constantes.py`  | Constantes: IVA, ruta del fichero, stock mínimo y tramos de descuento. |
| `calculos.py`    | Lógica de negocio: `calcular_iva`, `calcular_descuento`, `validar_stock`, valor del almacén, búsquedas… |
| `ficheros.py`    | Lectura y escritura del inventario en CSV. |
| `entrada.py`     | Lectura de teclado con control de errores (`try`/`except`). |
| `inventario.csv` | Fichero de datos de ejemplo. |

## Menú principal

```
===== GESTIÓN DE INVENTARIO =====
1. Listar productos
2. Añadir producto
3. Vender producto
4. Reponer stock
5. Modificar precio
6. Eliminar producto
7. Informe de stock
8. Guardar ahora
0. Guardar y salir
```

1. **Listar productos**: tabla con nombre, precio sin IVA, precio con IVA y stock.
2. **Añadir producto**: pide nombre, precio sin IVA y cantidad. No permite nombres repetidos.
3. **Vender producto**: pide el producto y las unidades. Comprueba que haya stock,
   aplica el descuento por volumen y el IVA, muestra el ticket y descuenta las unidades.
4. **Reponer stock**: suma unidades a un producto existente.
5. **Modificar precio**: cambia el precio sin IVA de un producto.
6. **Eliminar producto**: borra un producto (pide confirmación `s/n`).
7. **Informe de stock**: número de productos, unidades totales, valor del almacén
   (con y sin IVA) y productos con stock bajo (menos de 5 unidades).
8. **Guardar ahora**: guarda el inventario sin salir.
0. **Guardar y salir**: guarda el inventario en `inventario.csv` y cierra el programa.

Los nombres de producto no distinguen mayúsculas: `arroz 1kg` encuentra `Arroz 1kg`.

## Descuentos por volumen

| Unidades compradas | Descuento |
|--------------------|-----------|
| menos de 10        | 0 %       |
| de 10 a 19         | 5 %       |
| de 20 a 49         | 10 %      |
| 50 o más           | 15 %      |

El descuento se aplica antes del IVA (21 %).

**Ejemplo:** 25 unidades de Arroz 1kg a 1,20 € → 30,00 € − 10 % = 27,00 € + IVA = **32,67 €**.

## Control de errores

- Si escribes letras en un campo numérico, se muestra un error y se vuelve a pedir el dato.
- Los precios aceptan coma o punto decimal (`2,50` o `2.50`).
- No se admiten cantidades ni precios negativos.
- No se puede vender más unidades de las que hay en stock.
- Si `inventario.csv` no existe, el programa empieza vacío y lo crea al guardar.
- Si una línea del CSV está mal escrita, se ignora con un aviso y se cargan las demás.

## Formato del fichero `inventario.csv`

Una línea por producto, con los campos separados por punto y coma (precio sin IVA,
con punto decimal):

```
nombre;precio;cantidad
Arroz 1kg;1.2;40
```

Por eso no se permite el carácter `;` en los nombres de producto.
