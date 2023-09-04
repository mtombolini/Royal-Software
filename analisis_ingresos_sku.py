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



# Función para graficar stock acumulado de un SKU específico en un rango de fechas
def grafico_stock_acumulado_por_fecha(dataframe, sku, fecha_inicio, fecha_fin):
    df_producto = dataframe[(dataframe['SKU'] == sku) & ((dataframe['Fecha'] >= fecha_inicio) & (dataframe['Fecha'] <= fecha_fin))]

    if df_producto.empty:
        print(f"No se encontraron registros para el SKU: {sku}")
        return

    # Crear copias para evitar SettingWithCopyWarning
    df_ingresos = df_producto[df_producto['Nota'] == 'Importar Stock: Matías González'].copy()
    df_compras = df_producto[df_producto['Documento de Recepción'].str.contains('Factura', case=False)].copy()

    # Etiquetar las filas
    df_ingresos['Tipo'] = 'Ingreso'
    df_compras['Tipo'] = 'Compra'

    # Unir y ordenar
    df_unificado = pd.concat([df_ingresos, df_compras]).sort_values('Fecha')

    # Calcular el stock acumulado para todo (ingresos y compras)
    df_unificado['Stock Acumulado'] = df_unificado['Cantidad'].cumsum()

    # Graficar
    plt.figure(figsize=(12, 8))

    if len(df_unificado) == 1:
        plt.scatter(df_unificado['Fecha'], df_unificado['Stock Acumulado'], label=f'Stock acumulado')
    
    else:
        plt.plot(df_unificado['Fecha'], df_unificado['Stock Acumulado'], label='Stock acumulado')

    plt.xlabel('Fecha')
    plt.ylabel('Stock acumulado')
    plt.title(f"Stock acumulado por fecha - SKU: {sku}")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# --------------------------
# Programa principal
# --------------------------

# Leer el DataFrame y convertir la columna de fechas
dataframe_1 = preprocesamiento.lectura(parametros.RUTA_REPORTE_INGRESOS)
dataframe_1['Fecha'] = pd.to_datetime(dataframe_1['Fecha'], dayfirst=True)

# Parámetros de análisis
sku_a_analizar = '6010262'
fecha_inicio_analisis = pd.to_datetime('2022-01-01')
fecha_fin_analisis = pd.to_datetime('2023-08-31')

# Ejecutar las funciones de análisis y gráficos
print(analisis_producto_por_fecha(dataframe_1, sku_a_analizar, fecha_inicio_analisis, fecha_fin_analisis))
grafico_stock_acumulado_por_fecha(dataframe_1, sku_a_analizar, fecha_inicio_analisis, fecha_fin_analisis)