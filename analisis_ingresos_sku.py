# ANÁLISIS DE PRODUCTOS POR SKU

# Importar bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import parametros
import preprocesamiento
from datetime import datetime, timedelta

# --------------------------
# Funciones de análisis
# --------------------------

# Función para analizar datos de un SKU específico en un rango de fechas
def analisis_producto_por_fecha(dataframe, sku, fecha_inicio, fecha_fin):
    df_producto = dataframe[(dataframe['SKU'] == sku) & (dataframe['Fecha'] >= fecha_inicio) & (dataframe['Fecha'] <= fecha_fin)]

    if df_producto.empty:
        return f"No se encontraron registros para el SKU: {sku}"

    unidades_ingresadas = df_producto[df_producto['Nota'] == 'Importar Stock: Matías González']['Cantidad'].sum()
    unidades_compradas = df_producto[df_producto['Documento de Recepción'].str.contains('Factura', case=False)]['Cantidad'].sum()
    ultima_fecha_compra = df_producto[df_producto['Documento de Recepción'].str.contains('Factura', case=False)]['Fecha'].max()

    return (f"SKU: {sku}\n"
            f"Unidades ingresadas: {unidades_ingresadas}\n"
            f"Unidades compradas: {unidades_compradas}\n"
            f"Última fecha de compra: {ultima_fecha_compra}")


# --------------------------
# Programa principal
# --------------------------

# Leer el DataFrame y convertir la columna de fechas
dataframe_1 = preprocesamiento.lectura(parametros.RUTA_REPORTE_INGRESOS)
dataframe_1['Fecha'] = pd.to_datetime(dataframe_1['Fecha'], dayfirst=True)

#print(dataframe_1.columns)


# Parámetros de análisis
sku_a_analizar = 'H080'
fecha_inicio_analisis = pd.to_datetime('2022-01-01')
fecha_fin_analisis = pd.to_datetime('2023-08-31')

# Ejecutar las funciones de análisis y gráficos
print(analisis_producto_por_fecha(dataframe_1, sku_a_analizar, fecha_inicio_analisis, fecha_fin_analisis))