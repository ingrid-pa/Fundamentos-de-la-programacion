# constantes.py
# Constantes globales de la aplicación.
# En Python no existen constantes "reales": por convenio se escriben
# en MAYÚSCULAS para indicar que su valor no debe cambiarse.

IVA = 0.21                          # IVA general (21 %)
RUTA_FICHERO = "inventario.csv"     # Fichero donde se guarda el inventario
SEPARADOR = ";"                     # Separador de campos del CSV
STOCK_MINIMO = 5                    # Por debajo de este valor el stock es "bajo"

# Descuentos por volumen de compra: (unidades mínimas, descuento)
# Ordenados de mayor a menor para comprobarlos con if-elif.
UNIDADES_DESCUENTO_3, DESCUENTO_3 = 50, 0.15   # 50 o más uds -> 15 %
UNIDADES_DESCUENTO_2, DESCUENTO_2 = 20, 0.10   # 20 o más uds -> 10 %
UNIDADES_DESCUENTO_1, DESCUENTO_1 = 10, 0.05   # 10 o más uds ->  5 %
