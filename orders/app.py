from flask import Flask, request
from model_orders import Orders

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "MICROSERVICES - ORDERS"

#Pode-se informar o id do user, id do pedido ou não passar id
@app.route("/listar_order/<id_qualquer>/", methods=["GET"])
@app.route("/listar_order/", methods=["GET"])
def get_orders(id_qualquer=None):
    response = Orders().retornar_order(id_qualquer)
    print(response)
    if response:
        return response
    return "Nenhum valor foi encontrado", 400


@app.route("/criar_order/", methods=["POST"])
def post_order():
    """   Espera receber
    {
    "user_id": str(8),
    "item_description": "str,
    "item_quantity": int > 0,
    "item_price": float > 0,
    "total_value": item_quantity * item_price
    }
    """
    body_request = request.get_json()
    if not Orders().pedido_completo(body_request):
        return "Campos faltantes.", 400
    retorno = Orders().validar_campos(body_request)
    if not isinstance(retorno, dict):
        return retorno #que será uma mensagem de erro
    if Orders().cadastrar_orders(retorno):
        return "Pedido cadastrado com sucesso!", 200
    return "Pedido não Cadastrado. Problema no banco de dados.", 400


@app.route("/alterar_order/<id>/", methods=["PUT"])
def put_order(id):
    """
    Passar o id do pedido na url e informar pelo menos uma
    das keys (que constam na descrição de 'criar_order' neste arquivo
    """
    if not Orders().checar_id_order_exists(id):
         return "Id do pedido inválido.", 400
    body_request = request.get_json()
    if len(body_request) < 1:
        return "Nenhum valor de atualização passado", 400
    retorno = Orders().validar_campos(body_request)
    if not isinstance(retorno, dict):
        return retorno #que será uma mensagem de erro
    if Orders().atualizar_order(id, retorno):
        return f"Pedido {id} alterado com sucesso!"
    return f"Ops, pedido {id} não foi alterado."


@app.route("/excluir_order/<id>/", methods=["DELETE"])
def delete_order(id):
    if not Orders().checar_id_order_exists(id):
        return "Id do pedido inválido.", 400
    if Orders().excluir_order(id):
        return f"Pedido {id} excluído com sucesso", 200
    return f"Ops, pedido {id} não foi excluído.", 400




app.run(debug=True, port=5000)


