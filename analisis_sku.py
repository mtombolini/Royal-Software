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

# Función para graficar stock acumulado de un SKU específico en un rango de fechas
def grafico_stock_acumulado_por_fecha(dataframe_venta, dataframe_stock, sku, fecha_inicio, fecha_fin):
    df_venta_producto = dataframe_venta[(dataframe_venta['SKU'] == sku) & ((dataframe_venta['Fecha Venta'] >= fecha_inicio) & (dataframe_venta['Fecha Venta'] <= fecha_fin))]
    df_stock_producto = dataframe_stock[(dataframe_stock['SKU'] == sku) & ((dataframe_venta['Fecha'] >= fecha_inicio) & (dataframe_stock['Fecha'] <= fecha_fin))]

    if df_venta_producto.empty or df_stock_producto.empty:
        print(f"No se encontraron registros para el SKU: {sku}")
        return

    # Crear copias para evitar SettingWithCopyWarning
    df_ingresos = df_stock_producto[df_stock_producto['Nota'] == 'Importar Stock: Matías González'].copy()
    df_compras = df_stock_producto[df_stock_producto['Documento de Recepción'].str.contains('Factura', case=False)].copy()
    df_ventas = df_venta_producto[df_venta_producto['Tipo Movimiento'] == 'Venta'].copy()

    # Etiquetar las filas
    df_ingresos['Tipo'] = 'Ingreso'
    df_compras['Tipo'] = 'Compra'
    df_ventas['Tipo'] = 'Venta'

    # Unir y ordenar
    df_unificado = pd.concat([df_ingresos, df_compras, df_ventas]).sort_values('Fecha')

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
dataframe_ventas = preprocesamiento.lectura(parametros.RUTA_REPORTE_VENTAS)
dataframe_ventas['Fecha Venta'] = pd.to_datetime(dataframe_ventas['Fecha Venta'], dayfirst=True)
dataframe_stock = preprocesamiento.lectura(parametros.RUTA_REPORTE_INGRESOS)
dataframe_stock['Fecha'] = pd.to_datetime(dataframe_stock['Fecha'], dayfirst=True)

# Parámetros de análisis
sku_a_analizar = '1500'
fecha_inicio_analisis = pd.to_datetime('2023-01-01')
fecha_fin_analisis = pd.to_datetime('2023-08-31')

# Ejecutar las funciones de análisis y gráficos
grafico_stock_acumulado_por_fecha(dataframe_ventas, dataframe_stock, sku_a_analizar, fecha_inicio_analisis, fecha_fin_analisis)
