# EXPORTACIÓN DE INFORMACIÓN 

# Importar bibliotecas necesarias
import pandas as pd
import os
import analisis_sku
import preprocesamiento
import parametros

# Leer DataFrames y convertir la columna de fechas
dataframe_ventas = preprocesamiento.lectura(parametros.RUTA_REPORTE_VENTAS, 5)
dataframe_ventas['Fecha Venta'] = pd.to_datetime(dataframe_ventas['Fecha Venta'], dayfirst=True)
dataframe_recepcion = preprocesamiento.lectura(parametros.RUTA_REPORTE_INGRESOS, 6)
dataframe_recepcion['Fecha'] = pd.to_datetime(dataframe_recepcion['Fecha'], dayfirst=True)
dataframe_productos = preprocesamiento.lectura(parametros.RUTA_REPORTE_PRODUCTOS, 0)
dataframe_stock = preprocesamiento.lectura(parametros.RUTA_REPORTE_STOCK, 4)

# Parámetros de análisis
fecha_inicio = pd.to_datetime('2022-09-01')
fecha_fin = pd.to_datetime('2023-09-10')
lista_sku = list(dataframe_productos['SKU'].unique())

def exportacion_stock_critico(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, lista_sku, fecha_inicio, fecha_fin):
    # Crear una lista para almacenar las filas de datos
    filas = []

    for sku in lista_sku:
        procesador_sku = analisis_sku.ProcesadorSku(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, sku, fecha_inicio, fecha_fin)
        informacion = procesador_sku.informacion_compactada()
        
        # Verifica si la información es válida antes de agregarla
        if informacion is not None:
            sku, nombre, comprar = informacion
            filas.append([sku, nombre, comprar])

    # Crea un DataFrame con las filas y columnas especificadas
    columnas = ["SKU", "NOMBRE DEL PRODUCTO", "CANTIDAD A COMPRAR"]
    df_exportacion = pd.DataFrame(filas, columns=columnas)
    tabla_html = df_exportacion.to_html()

    ruta_guardado = os.path.join("static", "tabla.html")
    with open(ruta_guardado, 'w') as f:
        f.write(tabla_html)

    print("SE EXPORTO")

    return df_exportacion


def exportacion_detalle_producto(sku, dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, fecha_inicio, fecha_fin):
    procesador_sku = analisis_sku.ProcesadorSku(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, sku, fecha_inicio, fecha_fin)
    informacion_producto = procesador_sku.informacion_detallada()
    informacion_estadistica = procesador_sku.informacion_estadistica()
    return informacion_producto, informacion_estadistica




# --------------------------
# Programa principal
# --------------------------

tabla_stock_critico = exportacion_stock_critico(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, lista_sku, fecha_inicio, fecha_fin)

