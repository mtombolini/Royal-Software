# ANÁLISIS DE PRODUCTOS POR SKU

# Importar bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from pandas.tseries.offsets import MonthEnd
import parametros
import preprocesamiento
from datetime import datetime, timedelta
import re

# --------------------------
# Funciones de análisis
# --------------------------

class ProcesadorSku():
    def __init__(self, dataframe_productos, dataframe_venta, dataframe_stock, sku, fecha_inicio, fecha_fin):
        self.sku = sku
        self.f_inicio = fecha_inicio
        self.f_fin = fecha_fin
        self.df_venta = dataframe_venta[(dataframe_venta['SKU'] == self.sku) & (dataframe_venta['Fecha Venta'] >= self.f_inicio) & (dataframe_venta['Fecha Venta'] <= self.f_fin)]
        self.df_stock = dataframe_stock[(dataframe_stock['SKU'] == self.sku) & (dataframe_stock['Fecha'] >= self.f_inicio) & (dataframe_stock['Fecha'] <= self.f_fin)]
        self.df_productos = dataframe_productos
        self.nombre = self.df_venta['Producto / Servicio'].iloc[0]

    def verificacion_existencia(self):
        if self.df_venta.empty or self.df_stock.empty:
            return f"No se encontraron registros para el SKU: {self.sku}"

    def tipo_producto(self):
        resultado = re.search(r'\[(.*?)\]', self.nombre)
        if resultado:
            descuento = resultado.group(1)
            if descuento == "IM":
                return "IMPORTACION"
            elif descuento == "PZ":
                return "PLAZA"
            elif descuento == "OF":
                return "OFERTA"
            else:
                return "ERROR"
        else:
            return "No se encontró el tipo de producto entre corchetes."
        
    def informacion_inventario(self):
        unidades_ingresadas = self.df_stock[self.df_stock['Nota'] == 'Importar Stock: Matías González']['Cantidad'].sum()
        unidades_compradas = self.df_stock[self.df_stock['Documento de Recepción'].str.contains('Factura', case=False)]['Cantidad'].sum()
        ultima_fecha_compra = self.df_stock[self.df_stock['Documento de Recepción'].str.contains('Factura', case=False)]['Fecha'].max()

        return (f"Unidades ingresadas: {unidades_ingresadas}\n"
                f"Unidades compradas: {unidades_compradas}\n"
                f"Última fecha de compra: {ultima_fecha_compra}")
      
    def informacion_venta_total(self):
        unidades_vendidas = self.df_venta[self.df_venta['Tipo Movimiento'] == 'Venta']['Cantidad'].sum()
        unidades_devueltas = self.df_venta[self.df_venta['Tipo Movimiento'] == 'Devolucion']['Cantidad'].sum()
        ultima_fecha_venta = self.df_venta['Fecha Venta'].max()

        return (f"Unidades vendidas: {unidades_vendidas}\n"
                f"Unidades devueltas: {unidades_devueltas}\n"
                f"Última fecha de venta: {ultima_fecha_venta}")
    
    def informacion_venta_periodica(self):
        columnas_deseadas = ['Tipo Movimiento', 'SKU', 'Cantidad']
        dataframe_ventas = self.df_venta.copy()
        dataframe_ventas['Fecha Venta'] = pd.to_datetime(dataframe_ventas['Fecha Venta'])
        dataframe_ventas.set_index('Fecha Venta', inplace=True)
        dataframe_ventas = dataframe_ventas.loc[:, columnas_deseadas]
        dataframe_ventas.to_excel("ventasdata.xlsx", index=False)

        ventas_mensuales = dataframe_ventas.resample('M').sum()
        ventas_mensuales.index = ventas_mensuales.index.strftime('%B-%Y')
        
        return(f"Ventas mensuales: {ventas_mensuales['Cantidad']}\n"
               f"Ventas totales: {ventas_mensuales['Cantidad'].sum()}")

    
    def busqueda_alternativo(self):
        def modificar_string(texto):
            # Eliminar contenido entre '' usando una expresión regular
            texto = re.sub(r"''[^']*''", '', texto)
            
            # Eliminar contenido entre [] y lo que sigue después de los corchetes
            texto = re.sub(r'\[[^\]]*\].*', '', texto)
            
            # Eliminar espacios en blanco adicionales al final
            texto = texto.strip()
            return texto

        nombre_procesado = modificar_string(self.nombre)
        df_alternativos = self.df_productos[self.df_productos['Nombre del Producto'].str.contains(nombre_procesado, case=False, regex=False)]
        sku_alternativos = df_alternativos['SKU'].tolist()
        return sku_alternativos
    
    def impresion_información(self):
        print("----------------------------------------------------------------- ")
        print("---------------------INFORMACIÓN DE PRODUCTO---------------------")
        print(f"SKU: {self.sku}")
        print(f"PRODUCTO: {self.nombre}")
        print(f'TIPO: {self.tipo_producto()}')
        print("----------------------------------------------------------------- ")
        print(self.informacion_inventario())
        print("----------------------------------------------------------------- ")
        print(self.informacion_venta_total())
        print("----------------------------------------------------------------- ")
        print(f'Productos alternativos: {self.busqueda_alternativo()}')
        print("----------------------------------------------------------------- ")
        print(self.informacion_venta_periodica())
        print("----------------------------------------------------------------- ")
        print("")

    def procesador_dataframe_stock_historico(self):
        # ---- GRAFICO STOCK EN EL TIEMPO ----
        # Crear copias para evitar SettingWithCopyWarning
        df_ingresos = self.df_stock[self.df_stock['Nota'] == 'Importar Stock: Matías González'].copy()
        df_compras = self.df_stock[self.df_stock['Documento de Recepción'].str.contains('Factura', case=False)].copy()
        df_ventas = self.df_venta[self.df_venta['Tipo Movimiento'] == 'Venta'].copy()
        df_devoluciones = self.df_venta[self.df_venta['Tipo Movimiento'] == 'Devolucion'].copy()
        df_vacio = pd.DataFrame(pd.date_range(start=self.f_inicio, end=self.f_fin), columns=['Fecha'])

        # Renombrar la columna 'Fecha Venta' en df_ventas para que sea 'Fecha'
        df_ventas.rename(columns={'Fecha Venta': 'Fecha'}, inplace=True)
        df_devoluciones.rename(columns={'Fecha Venta': 'Fecha'}, inplace=True)

        # Indicar el signo de cada operación
        df_ingresos['Signo'] = 1
        df_compras['Signo'] = 1
        df_ventas['Signo'] = -1  # Para restar las ventas
        df_devoluciones['Signo'] = 1
        df_vacio['Signo'] = 0

        # Indicar la naturaleza de cada operación
        df_ingresos['Tipo'] = "Ingreso"
        df_compras['Tipo'] = "Compra"
        df_ventas['Tipo'] = "Venta"  # Para restar las ventas
        df_devoluciones['Tipo'] = "Devolucion"
        df_vacio['Tipo'] = "Sin Movimiento"

        # Unir, ordenar y filtrar dataframe
        df_unificado = pd.concat([df_ingresos, df_compras, df_ventas, df_devoluciones, df_vacio]).sort_values('Fecha')
        df_unificado['Stock Acumulado'] = (df_unificado['Cantidad'] * df_unificado['Signo']).cumsum()
        df_completo = pd.merge(df_vacio, df_unificado, on='Fecha', how='left')
        df_completo['Stock Acumulado'].ffill(inplace=True)

        columnas_deseadas = ['Sucursal', 'Fecha', 'Usuario', 'Vendedor', 'SKU', 'Cantidad', 'Tipo_x', 'Stock Acumulado']
        
        df_completo = df_completo.loc[:, columnas_deseadas]

        # Guardar el DataFrame en un archivo Excel
        df_completo.to_excel("hola_completo.xlsx", index=False)
        return df_completo

        '''
        EXISTE ERROR AL EXPORTAR EL GRÁFICO, LA COLUMNA TIPO NO ESTA FUNCIONANDO CORRECTAMENTE
        '''

    def procesador_dataframe_ventas_semanales(self):
        df_ventas = self.df_venta[self.df_venta['Tipo Movimiento'] == 'Venta'].copy()
        df_ventas.set_index('Fecha Venta', inplace=True)
        df_semana = df_ventas[['Cantidad']].resample('W-Mon').sum()

        # Crear un índice de fechas completo desde la fecha de inicio hasta la fecha final
        indice_completo = pd.date_range(start=self.f_inicio, end=self.f_fin, freq='W-Mon')
        df_semana = df_semana.reindex(indice_completo, fill_value=0)
        df_semana.to_excel("ventasdataframe.xlsx", index=False)

        return df_semana
       
    def visualizacion_grafico(self):
        df_1 = self.procesador_dataframe_stock_historico()
        df_2 = self.procesador_dataframe_ventas_semanales()
        plt.figure(figsize=(12, 8))

        # Graficar dataframes originales
        plt.plot(df_1['Fecha'], df_1['Stock Acumulado'], label='Stock histórico')
        plt.plot(df_2.index, df_2['Cantidad'], label='Ventas por semana')

        # Creación de interpolaciones cúbicas para df_2
        x_smooth_ventas = np.linspace(df_2.index.astype(np.int64).min(), df_2.index.astype(np.int64).max(), 300)
        y_smooth_ventas = make_interp_spline(df_2.index.astype(np.int64), df_2['Cantidad'], k=3)(x_smooth_ventas)
        plt.plot(pd.to_datetime(x_smooth_ventas, unit='ns'), y_smooth_ventas, label='Interpolación cúbica ventas', color='green', linewidth=2)

        # ---- PENDIENTE DE ARREGLO ----
        # x_smooth_stock = np.linspace(df_1.index.astype(np.int64).min(), df_1.index.astype(np.int64).max(), 300)
        # y_smooth_stock = make_interp_spline(df_1.index.astype(np.int64), df_1['Stock Acumulado'], k=3)(x_smooth_stock)
        # plt.plot(pd.to_datetime(x_smooth_stock, unit='ns'), y_smooth_stock, label='Interpolación cúbica stock', color='black', linewidth=2)
        # ------------------------------

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
dataframe_ventas = preprocesamiento.lectura(parametros.RUTA_REPORTE_VENTAS, 5)
dataframe_ventas['Fecha Venta'] = pd.to_datetime(dataframe_ventas['Fecha Venta'], dayfirst=True)
dataframe_stock = preprocesamiento.lectura(parametros.RUTA_REPORTE_INGRESOS, 5)
dataframe_stock['Fecha'] = pd.to_datetime(dataframe_stock['Fecha'], dayfirst=True)
dataframe_productos = preprocesamiento.lectura(parametros.RUTA_REPORTE_PRODUCTOS, 0)

# Parámetros de análisis
sku_a_analizar = 'DA007'
fecha_inicio_analisis = pd.to_datetime('2022-09-01')
fecha_fin_analisis = pd.to_datetime('2023-08-31')

sku = '400273'
#sku = '400666'


procesador_sku = ProcesadorSku(dataframe_productos, dataframe_ventas, dataframe_stock, sku, fecha_inicio_analisis, fecha_fin_analisis)
procesador_sku.impresion_información()
procesador_sku.visualizacion_grafico()