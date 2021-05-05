from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "MICROSERVICES - ORDERS"

@app.route("/listar/<id_order>/", methods=["GET"])
@app.route("/listar/<id_user>/", methods=["GET"])
@app.route("/listar/", methods=["GET"])
def get_listar_orders(id_user=None, id_order=None):
    response = 1
    return response

@app.route("/criar/", methods=["POST"])
def get_criar_order():



    #checar se algum dos campos do dict não foi preenchido
    response = 1
    return response

@app.route("/alterar/", methods=["PUT"])
def get_alterar_order():
    response = 1
    return response

@app.route("/excluir/", methods=["DELETE"])
def get_excluir_order():
    response = 1
    return response

app.run(debug=True)


