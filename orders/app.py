from flask import Flask, request
from model_orders import Orders

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "MICROSERVICES - ORDERS"

@app.route("/listar/<id_qualquer>/", methods=["GET"])
@app.route("/listar/", methods=["GET"])
def get_orders(id_qualquer=None):
    response = Orders().retornar_order(id_qualquer)
    if response:
        return response
    return "Nenhum valor foi encontrado", 400


@app.route("/criar/", methods=["POST"])
def post_order():
    body_request = request.get_json()
    for i in list(body_request.keys()):
        if i not in ['user_id', 'item_description', 'item_quantity', 'item_price', 'total_value']:
            return "Campos faltantes", 400
    retorno = Orders().validar_campos(body_request)
    if not isinstance(retorno, dict):
        return retorno #que será uma mensagem de erro
    if Orders().cadastrar_orders(retorno):
        return "Pedido cadastrado com sucesso!", 200
    return "Pedido não Cadastrado. Problema no banco de dados.", 400


@app.route("/alterar/<id>/", methods=["PUT"])
def put_order(id):
    if not Orders().checar_id_order_exists(id):
         return "Id do pedido inválido.", 400
    body_request = request.get_json()
    if len(body_request) < 1:
        return "Nenhum valor de atualização passado", 400
    retorno = Orders().validar_campos(body_request)
    if not isinstance(retorno, dict):
        return retorno #que será uma mensagem de erro
    if Orders().atualizar_order(id, retorno):
        return f"Usuário {id} alterado com sucesso!"
    return f"Ops, usuário {id} não foi alterado."


@app.route("/excluir/<id>/", methods=["DELETE"])
def delete_order(id):
    if not Orders().checar_id_order_exists(id):
        return "Id do pedido inválido.", 400
    if Orders().excluir_order(id):
        return f"Usuário {id} excluído com sucesso", 200
    return f"Ops, usuário {id} não foi excluído.", 400

# app.run(debug=True)


