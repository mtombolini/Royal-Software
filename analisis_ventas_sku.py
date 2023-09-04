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
    df_producto = dataframe[(dataframe['SKU'] == sku) & (dataframe['Fecha Venta'] >= fecha_inicio) & (dataframe['Fecha Venta'] <= fecha_fin)]

    if df_producto.empty:
        return f"No se encontraron registros para el SKU: {sku}"

    unidades_vendidas = df_producto[df_producto['Tipo Movimiento'] == 'Venta']['Cantidad'].sum()
    unidades_devueltas = df_producto[df_producto['Tipo Movimiento'] == 'Devolucion']['Cantidad'].sum()
    ultima_fecha_venta = df_producto['Fecha Venta'].max()

    return (f"SKU: {sku}\n"
            f"Unidades vendidas: {unidades_vendidas}\n"
            f"Unidades devueltas: {unidades_devueltas}\n"
            f"Última fecha de venta: {ultima_fecha_venta}")


# Función para graficar ventas por semana de un SKU específico en un rango de fechas
def grafico_ventas_por_semana_por_fecha(dataframe, sku, fecha_inicio, fecha_fin):
    # Filtrar y preparar los datos
    df_producto = dataframe[(dataframe['SKU'] == sku) & (dataframe['Fecha Venta'] >= fecha_inicio) & (dataframe['Fecha Venta'] <= fecha_fin)]
    if df_producto.empty:
        print(f"No se encontraron registros para el SKU: {sku}")
        return

    df_producto.set_index('Fecha Venta', inplace=True)
    df_semana = df_producto[['Cantidad']].resample('W-Mon').sum()

    # Crear un índice de fechas completo desde la fecha de inicio hasta la fecha final
    indice_completo = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='W-Mon')
    df_semana = df_semana.reindex(indice_completo, fill_value=0)

    # Crear el gráfico
    plt.figure(figsize=(12, 8))

    # Dibujar la línea original
    plt.plot(df_semana.index, df_semana['Cantidad'], label='Líneas originales', color='blue', linewidth=2)

    # Interpolación cúbica para suavizar la línea
    x_smooth = np.linspace(df_semana.index.astype(np.int64).min(), df_semana.index.astype(np.int64).max(), 300)
    y_smooth = make_interp_spline(df_semana.index.astype(np.int64), df_semana['Cantidad'], k=3)(x_smooth)
    plt.plot(pd.to_datetime(x_smooth, unit='ns'), y_smooth, label='Interpolación cúbica', color='red', linewidth=2)

    # Ajustar y dibujar la línea de tendencia
    coeffs = np.polyfit(np.arange(len(df_semana)), df_semana['Cantidad'].values, 1)
    trend_line = np.polyval(coeffs, np.arange(len(df_semana)))
    plt.plot(df_semana.index, trend_line, label='Línea de tendencia', color='green', linestyle='--', linewidth=2)

    # Ajustar el gráfico
    plt.xlabel('Semana')
    plt.ylabel('Cantidad de unidades vendidas')
    plt.title(f"Unidades vendidas por semana - SKU: {sku}")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.show()


# --------------------------
# Programa principal
# --------------------------

# Leer el DataFrame y convertir la columna de fechas
dataframe_1 = preprocesamiento.lectura(parametros.RUTA_REPORTE_VENTAS)
dataframe_1['Fecha Venta'] = pd.to_datetime(dataframe_1['Fecha Venta'], dayfirst=True)

# Parámetros de análisis
sku_a_analizar = '1500'
fecha_inicio_analisis = pd.to_datetime('2023-01-01')
fecha_fin_analisis = pd.to_datetime('2023-08-31')

# Ejecutar las funciones de análisis y gráficos
print(analisis_producto_por_fecha(dataframe_1, sku_a_analizar, fecha_inicio_analisis, fecha_fin_analisis))
grafico_ventas_por_semana_por_fecha(dataframe_1, sku_a_analizar, fecha_inicio_analisis, fecha_fin_analisis)
