# ANÁLISIS DE PRODUCTOS POR SKU

# Importar bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from sklearn.linear_model import LinearRegression
from pandas.tseries.offsets import MonthEnd
import parametros
import preprocesamiento
from datetime import datetime, timedelta
import re
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller, acf, pacf



# --------------------------
# Funciones de análisis
# --------------------------


class ProcesadorSku():
    def __init__(self, dataframe_productos, dataframe_venta, dataframe_recepcion, dataframe_stock, sku, fecha_inicio, fecha_fin):
        # Parámetros de análisis
        self.f_inicio = fecha_inicio
        self.f_fin = fecha_fin

        # Dataframes
        self.df_venta = dataframe_venta[(dataframe_venta['SKU'] == sku) & (dataframe_venta['Fecha Venta'] >= self.f_inicio) & (dataframe_venta['Fecha Venta'] <= self.f_fin)]
        self.df_recepcion = dataframe_recepcion[(dataframe_recepcion['SKU'] == sku) & (dataframe_recepcion['Fecha'] >= self.f_inicio) & (dataframe_recepcion['Fecha'] <= self.f_fin)]
        self.df_productos = dataframe_productos
        self.df_stock = dataframe_stock[(dataframe_stock['SKU'] == sku)]

        # Atributos del producto
        self.sku = sku
        self.nombre = self.obtener_nombre()
        self.tipo = self.obtener_tipo()
        self.stock = self.obtener_stock()

        # Kardex
        self.kardex = self.kardex()


    # Función para obtener el nombre del producto
    def obtener_nombre(self):
        nombre = str(self.df_productos[self.df_productos['SKU'] == self.sku]['Nombre del Producto'])
        return nombre
    
    
    # Función para obtener el tipo de producto (descuento) del producto    
    def obtener_tipo(self):
        resultado = re.search(r'\[(.*?)\]', self.nombre)
        
        tipos = {"IM": "IMPORTACION",
                "PZ": "PLAZA",
                "OF": "OFERTA"}
        
        if resultado:
            descuento = resultado.group(1)
            tipo = tipos.get(descuento, "ERROR")
            return tipo
        else:
            return "No se encontró el tipo de producto entre corchetes."
        
    
    # Función para obtener el stock actual del producto
    def obtener_stock(self):
        stock_total = self.df_stock['Stock'].sum()
        return stock_total

        
        
    # Función para crear dataframe general (tarjeta de existencia)
    def kardex(self):
        df_recepcion = self.df_recepcion.copy()
        df_ventas = self.df_venta.copy()

        columnas_df_recepcion = ["Fecha", "Documento de Recepción", "Nota", "SKU", "Cantidad"]
        columnas_df_ventas = ["Tipo Movimiento", "Fecha Venta", "SKU", "Cantidad"]

        df_recepcion = df_recepcion.loc[:, columnas_df_recepcion]
        df_ventas = df_ventas.loc[:, columnas_df_ventas]

        df_ventas.rename(columns={'Fecha Venta': 'Fecha'}, inplace=True)

        df_kardex = pd.concat([df_recepcion, df_ventas])

        df_kardex['Documento de Recepción'] = df_kardex['Documento de Recepción'].fillna('')
        df_kardex.loc[df_kardex['Documento de Recepción'].str.contains('Factura', case=False), 'Tipo Movimiento'] = "Compra"
        df_kardex.loc[df_kardex['Nota'] == 'Importar Stock: Matías González', 'Tipo Movimiento'] = 'Ingreso'

        print("AAA", self.sku)
        
        df_kardex.loc[df_kardex['Tipo Movimiento'] == 'Compra', 'Signo'] = 1
        df_kardex.loc[df_kardex['Tipo Movimiento'] == 'Ingreso', 'Signo'] = 1
        df_kardex.loc[df_kardex['Tipo Movimiento'] == 'Venta', 'Signo'] = -1
        df_kardex.loc[df_kardex['Tipo Movimiento'] == 'Devolucion', 'Signo'] = -1

        df_kardex = df_kardex.sort_values('Fecha')
        df_kardex['Stock'] = (df_kardex['Cantidad'] * df_kardex['Signo']).cumsum()
        df_kardex = df_kardex.dropna(subset=['Tipo Movimiento'])
        df_kardex = df_kardex.loc[:, ['Fecha', 'SKU', 'Cantidad', 'Tipo Movimiento', 'Stock']]
        
        #df_kardex.to_excel("kardex.xlsx", index=False)

        return df_kardex


    # Funcion para calcular la cantidad de unidades vendidas por mes
    def ventas_periodicas(self, periodo):
        kardex = self.kardex

        kardex_ventas = kardex.loc[kardex['Tipo Movimiento'] == 'Venta'].copy()
        kardex_ventas['Fecha'] = pd.to_datetime(kardex_ventas['Fecha'])
        kardex_ventas.set_index('Fecha', inplace=True)

        ventas = kardex_ventas.resample(periodo)['Cantidad'].sum()

        ventas.to_excel("mensuales.xlsx")

        return ventas
    
    def stock_tiempo(self):
        kardex = self.kardex
        df_vacio = pd.DataFrame(pd.date_range(start=self.f_inicio, end=self.f_fin), columns=['Fecha'])
        df_ajustado = df_completo = pd.merge(df_vacio, kardex, on='Fecha', how='left')
        df_ajustado['Stock'].ffill(inplace=True)
        return df_ajustado



    # Función para calcular parámetros estadísticos de ventas periodicas
    def analisis_ventas_periodicas(self, periodo):
        ventas = self.ventas_periodicas(periodo)

        # Estadísticas Descriptivas
        media = np.mean(ventas)
        mediana = np.median(ventas)
        desviacion_estandar = np.std(ventas)
        
        print(f"Media de Ventas: {media}")
        print(f"Mediana de Ventas: {mediana}")
        print(f"Desviación Estándar de Ventas: {desviacion_estandar}")
        
        # Gráfica de Ventas a lo largo del tiempo
        plt.figure(figsize=(12, 6))
        plt.plot(ventas.index, ventas.values, marker='o', linestyle='-')
        plt.title("Ventas Periódicas")
        plt.xlabel("Fecha")
        plt.ylabel("Cantidad Vendida")
        plt.grid(True)
        plt.show()
        
        # Autocorrelación
        autocorrelacion = ventas.autocorr(lag=1)  # Autocorrelación con un retraso (lag) de 1 periodo
        print(f"Autocorrelación con un periodo de retraso: {autocorrelacion}")

        # Percentiles
        percentil_25 = np.percentile(ventas.dropna(), 25)
        percentil_75 = np.percentile(ventas.dropna(), 75)
        print(f"Percentil 25: {percentil_25}")
        print(f"Percentil 75: {percentil_75}")

        # Estacionalidad (descomposición básica usando promedio móvil, por ejemplo)
        ventas_rolling = ventas.rolling(window=4).mean()
        plt.figure(figsize=(12, 6))
        plt.plot(ventas.index, ventas.values, label='Original')
        plt.plot(ventas_rolling.index, ventas_rolling.values, label='Promedio Móvil')
        plt.legend(loc='best')
        plt.title("Estacionalidad en Ventas")
        plt.grid(True)
        plt.show()

    
    def prediccion(self):
        # Calcular el promedio móvil de 3 meses (trimestral)
        ventas = self.ventas_periodicas('W')  # Obtener ventas semanales (cambia 'M' por 'W')
        promedio_movil = ventas.rolling(window=3).mean()  # Calcular el promedio móvil de 3 semanas

        # Pronosticar la próxima semana (el último valor del promedio móvil)
        ultimo_valor_promedio_movil = promedio_movil.iloc[-1]

        # Agregar el pronóstico a la serie de ventas semanales
        fecha_proxima_semana = ventas.index[-1] + pd.DateOffset(weeks=1)  # Calcula la fecha de la próxima semana
        ventas.loc[fecha_proxima_semana] = ultimo_valor_promedio_movil

        # Mostrar el pronóstico
        print(f"Pronóstico para la próxima semana ({fecha_proxima_semana}): {ultimo_valor_promedio_movil}")


    def deteccion(self):
        df_stock = self.stock_tiempo()
        print(f'SKU: {self.sku}')

        dias_stock = (df_stock['Stock'] > 0).sum()
        unidades_vendidas = df_stock[df_stock['Tipo Movimiento'] == 'Venta']['Cantidad'].sum()
        
        #print(dias_stock)
        #print(unidades_vendidas)
        # print(f'RMM: {RMM}')

        if self.stock == 0:
            if dias_stock > 1:
                RMM = round((unidades_vendidas / dias_stock) * 30)
                if RMM >= 1:
                    print(f'El SKU: {self.sku} requiere la compra de {RMM} unidades.')
            
            



        




# --------------------------
# Programa principal
# --------------------------

# Leer el DataFrame y convertir la columna de fechas
dataframe_ventas = preprocesamiento.lectura(parametros.RUTA_REPORTE_VENTAS, 5)
dataframe_ventas['Fecha Venta'] = pd.to_datetime(dataframe_ventas['Fecha Venta'], dayfirst=True)
dataframe_recepcion = preprocesamiento.lectura(parametros.RUTA_REPORTE_INGRESOS, 6)
dataframe_recepcion['Fecha'] = pd.to_datetime(dataframe_recepcion['Fecha'], dayfirst=True)
dataframe_productos = preprocesamiento.lectura(parametros.RUTA_REPORTE_PRODUCTOS, 0)
dataframe_stock = preprocesamiento.lectura(parametros.RUTA_REPORTE_STOCK, 4)

# Parámetros de análisis
sku = '400666'
fecha_inicio_analisis = pd.to_datetime('2022-09-01')
fecha_fin_analisis = pd.to_datetime('2023-09-10')

# Procesador 
#procesador_sku = ProcesadorSku(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, sku, fecha_inicio_analisis, fecha_fin_analisis)
# procesador_sku.prediccion()
# procesador_sku.analisis_ventas_periodicas('D')
#procesador_sku.deteccion()


lista_sku = list(dataframe_productos['SKU'].unique())
lista_sku.remove("A999")
lista_sku.remove("R045-A")
# lista_sku.remove("15AF5D")
# lista_sku.remove("15D2C2")


for sku in lista_sku:
    procesador_sku = ProcesadorSku(dataframe_productos, dataframe_ventas, dataframe_recepcion, dataframe_stock, sku, fecha_inicio_analisis, fecha_fin_analisis)
    procesador_sku.deteccion()



# Arreglar sku que tienen kardex vacio porque no han tenido movimientos