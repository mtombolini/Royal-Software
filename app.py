from flask import Flask, render_template, url_for, jsonify
import exportador

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/stock_roto_page')
def stock_roto_page():
    df = exportador.tabla_stock_critico  # Asegúrate de que esta variable contenga la tabla que quieres mostrar
    image_url = url_for('static', filename='imagenes/lupa.png')
    df['DETALLE'] = df.apply(lambda row: f'<button class="lupa-button" data-sku="{row["SKU"]}"><img src="{image_url}" alt="Lupa" width="20" height="20"></button>', axis=1)
    tabla_html = df.to_html(escape=False)  # escape=False permite incluir HTML en la tabla
    return render_template('stock_critico.html', tabla=tabla_html)

@app.route('/detalle/<sku>')
def detalle(sku):
    return render_template('detalle.html', sku=sku)

@app.route('/informacion_detallada/<sku>')
def informacion_detallada(sku):
    info_producto, info_estadistica = exportador.exportacion_detalle_producto(
        sku,
        exportador.dataframe_productos,
        exportador.dataframe_ventas,
        exportador.dataframe_recepcion,
        exportador.dataframe_stock,
        exportador.fecha_inicio,
        exportador.fecha_fin
    )
    
    return jsonify({
        "info_producto": info_producto,
        "info_estadistica": info_estadistica
    })

if __name__ == '__main__':
    app.run(debug=True)
