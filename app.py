from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/stock_roto_page')
def stock_roto_page():
    return render_template('stock_critico.html')


# @app.route('/stock_roto', methods=['POST'])
# def boton_stock_roto():
#     print("Redirigiendo a stock roto")
#     # Aquí puedes colocar la lógica de tu análisis estadístico en Python
#     # Procesa los datos enviados desde la página HTML (usando request) y realiza el análisis
#     # Devuelve los resultados como JSON
#     resultados = {"resultado1": 42, "resultado2": 23}
#     return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
