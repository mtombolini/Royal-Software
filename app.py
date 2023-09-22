from flask import Flask, render_template, url_for, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
import exportador  # Asegúrate de tener este módulo en tu proyecto
import pandas as pd  # Asegúrate de instalar pandas si no lo has hecho
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carro_compras.db'


db = SQLAlchemy(app)

# Modelo de la base de datos
class CarroCompras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SKU = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), nullable=False)

# Crear una función para inicializar la base de datos
def init_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/stock_roto_page')
def stock_roto_page():
    df = exportador.tabla_stock_critico  # Reemplaza esto con el DataFrame que ya tienes

    # Íconos para los botones de "Aceptar", "Quizás" y "Rechazar"
    icons = {
        'aceptar': url_for('static', filename='imagenes/aceptar.png'),
        'quizas': url_for('static', filename='imagenes/pausa.png'),
        'rechazar': url_for('static', filename='imagenes/rechazado.png'),
        'detalle': url_for('static', filename='imagenes/lupa.png')
    }

    df['Detalle'] = df.apply(
        lambda row: f'<button class="lupa-button" data-sku="{row["SKU"]}"><img src="{icons["detalle"]}" alt="Detalle" width="20" height="20"></button>', axis=1)


    df['Respuesta'] = df.apply(lambda row: ''.join([
    '<div class="button-container">',  # Agregado un contenedor para los botones
    f'<button class="respuesta-button" data-sku="{row["SKU"]}" data-respuesta="si"><img src="{icons["aceptar"]}" alt="Aceptar" width="20" height="20"></button>',
    f'<button class="respuesta-button" data-sku="{row["SKU"]}" data-respuesta="quizas"><img src="{icons["quizas"]}" alt="Quizás" width="20" height="20"></button>',
    f'<button class="respuesta-button" data-sku="{row["SKU"]}" data-respuesta="no"><img src="{icons["rechazar"]}" alt="Rechazar" width="20" height="20"></button>',
    '</div>'  # Cierre del contenedor de botones
    ]), axis=1)


    tabla_html = df.to_html(escape=False)
    return render_template('stock_critico.html', tabla=tabla_html)


@app.route('/detalle/<sku>')
def detalle(sku):
    grafico_path = grafico(sku)  # Llama a la función grafico() para obtener la ruta del gráfico.
    return render_template('detalle.html', sku=sku, grafico_path=grafico_path)


@app.route('/grafico/<sku>')
def grafico(sku):
    procesador = exportador.exportacion_detalle_producto(
        sku,
        exportador.dataframe_productos,
        exportador.dataframe_ventas,
        exportador.dataframe_recepcion,
        exportador.dataframe_stock,
    )
    
    file_path = procesador.grafica_ventas("01/09/2022")
    
    # Devuelve la ruta del archivo para ser usado en el iframe.
    return url_for('static', filename=f'graficos/grafico_{sku}.html')




@app.route('/informacion_detallada/<sku>')
def informacion_detallada(sku):
    procesador = exportador.exportacion_detalle_producto(
        sku,
        exportador.dataframe_productos,
        exportador.dataframe_ventas,
        exportador.dataframe_recepcion,
        exportador.dataframe_stock,
    )

    info_producto = procesador.informacion_detallada()
    info_estadistica = procesador.informacion_estadistica()

    return jsonify({
        "info_producto": info_producto,
        "info_estadistica": info_estadistica
    }) 

@app.route('/registrar_respuesta', methods=['POST'])
def registrar_respuesta():
    data = request.json
    sku = data.get('sku')
    estado = data.get('respuesta')

    respuesta_existente = CarroCompras.query.filter_by(SKU=sku).first()

    if respuesta_existente:
        if respuesta_existente.estado == estado:  # El estado es el mismo, eliminar el registro
            db.session.delete(respuesta_existente)
        else:  # El estado es diferente, actualizar el registro
            respuesta_existente.estado = estado
    else:
        nueva_respuesta = CarroCompras(SKU=sku, estado=estado)
        db.session.add(nueva_respuesta)

    db.session.commit()
    return jsonify({"status": "success"})
    
@app.route('/obtener_respuestas', methods=['GET'])
def obtener_respuestas():
    respuestas = CarroCompras.query.all()
    respuesta_dict = {r.SKU: r.estado for r in respuestas}
    return jsonify(respuesta_dict)

@app.route('/carro_compras')
def carro_compras():
    productos_si = CarroCompras.query.filter_by(estado='si').all()
    return render_template('carro_compras.html', productos=productos_si)



if __name__ == '__main__':
    init_db()  # Llamar a la función para inicializar la base de datos
    app.run(debug=True)