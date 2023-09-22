from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import pandas as pd

# Crear un DataFrame de ejemplo
df = pd.DataFrame({'Fecha': ['2022-01-01', '2022-01-02', '2022-01-03'],
                   'Stock': [100, 90, 80]})

# Convertir la columna 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Crear la figura
p = figure(title="Rotación de Stock", x_axis_label='Fecha', y_axis_label='Stock', x_axis_type="datetime")

# Añadir una línea
p.line(df['Fecha'], df['Stock'], legend_label="Stock", line_width=2)

# Guardar en un archivo HTML
output_file("rotacion_de_stock.html")

# Mostrar la figura
show(p)

# O para incrustar en tu aplicación web
script, div = components(p)
