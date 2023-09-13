from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from io import BytesIO
import parametros

class ReporteReposicion:
    def __init__(self, nombre_archivo):
        self.output_file = nombre_archivo
        self.logo_path = parametros.RUTA_LOGO
        self.tamaño = letter

    def logo(self, c):
        logo = utils.ImageReader(self.logo_path)
        c.drawImage(logo, 50, 700, width=100, height=50)

    def titulo(self, c):
        # Crear un rectángulo de bordes curvos
        c.setFillColorRGB(0.5, 0.5, 0.5)  # Color de relleno gris (puedes personalizarlo)
        c.roundRect(50, 680, 520, 70, 10, stroke=0, fill=1)

    def generar_pdf(self):
        # Crear un objeto canvas para el PDF
        c = canvas.Canvas(self.output_file, pagesize=self.tamaño)

        self.titulo(c)
        self.logo(c)  # Llamar al método logo y pasar el objeto canvas como argumento
          # Llamar al método titulo y pasar el objeto canvas como argumento

        # Agregar el título
        c.setFont("Helvetica-Bold", 24)
        c.drawString(200, 650, "ROYAL")

        # Puedes agregar más contenido aquí, como tablas o gráficos

        # Guardar el PDF
        c.save()

if __name__ == "__main__":
    # Crear una instancia de la clase ReporteReposicion
    reporte = ReporteReposicion("reporte_reposicion.pdf")

    # Generar el PDF
    reporte.generar_pdf()
    print(f"Se ha generado el PDF: {reporte.output_file}")
