from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import stock_roto
import matplotlib.pyplot as plt
import pandas as pd
import io

def generate_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)

    sku_a_analizar = '1500'
    dataframe_1 = stock_roto.preprocesamiento.lectura(stock_roto.parametros.RUTA_SALES_REPORT)
    dataframe_1['Fecha Venta'] = pd.to_datetime(dataframe_1['Fecha Venta'], dayfirst=True)

    # Capturar los resultados en variables o strings
    analisis_result = stock_roto.analisis_producto(dataframe_1, sku_a_analizar)
    
    # Crear el gráfico en una imagen en memoria
    grafico_filename = "grafico.png"
    plt.figure(figsize=(12, 8))
    stock_roto.grafico_ventas_por_semana(dataframe_1, sku_a_analizar)
    plt.savefig(grafico_filename, format="png")
    plt.close()  # Cerrar la figura de Matplotlib
    
    # Agregar los resultados al PDF
    c.drawString(100, 750, "Reporte de Análisis de Producto")
    if analisis_result:
        c.drawString(100, 730, analisis_result)
    
    # Insertar la imagen del gráfico en el PDF
    c.drawImage(grafico_filename, 100, 400, width=400, height=300)
    
    # Guardar y cerrar el PDF
    c.save()

if __name__ == "__main__":
    generate_pdf("mi_reporte_con_datos.pdf")
