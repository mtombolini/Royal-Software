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

def exportacion(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, lista_sku, fecha_inicio, fecha_fin):
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
    #df_exportacion.to_excel("exportacion.xlsx", index=False)
    tabla_html = df_exportacion.to_html()
    ruta_guardado = os.path.join("static", "tabla.html")
    with open(ruta_guardado, 'w') as f:
        f.write(tabla_html)
    print("SE EXPORTO")

    # Ahora tienes un DataFrame df_exportacion con los datos que deseas exportar
    # Puedes guardar este DataFrame en un archivo CSV u realizar cualquier otro procesamiento necesario.
    
    return df_exportacion


# --------------------------
# Programa principal
# --------------------------

exportacion(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, lista_sku, fecha_inicio, fecha_fin)
