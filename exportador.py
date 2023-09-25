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

def exportacion_stock_critico(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, lista_sku):
    filas = []

    for sku in lista_sku:
        procesador_sku = analisis_sku.ProcesadorSku(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, sku)
        informacion = procesador_sku.informacion_compactada()
        
        if informacion is not None:
            sku, nombre, proovedor, informacion_1, informacion_2, comprar = informacion
            filas.append([sku, nombre, proovedor, informacion_1, informacion_2, comprar])

    columnas = ["SKU", "NOMBRE DEL PRODUCTO", "PROOVEDOR", "COSTO NETO", "INFORMACIÓN 2", "CANTIDAD A COMPRAR"]
    df_exportacion = pd.DataFrame(filas, columns=columnas)
    return df_exportacion

def exportacion_detalle_producto(sku, dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock):
    procesador_sku = analisis_sku.ProcesadorSku(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, sku)
    return procesador_sku

# Programa principal
tabla_stock_critico = exportacion_stock_critico(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, lista_sku)
