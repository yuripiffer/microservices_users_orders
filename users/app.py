from model_users import User
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "MICROSERVICES - USERS"

#Pode-se informar o id do user ou não passar id
@app.route("/listar_user/<id>/", methods=["GET"])
@app.route("/listar_user/", methods=["GET"])
def get_users(id=None):
    response = User().retornar_user(id)
    if response:
        return response
    return "Nenhum valor foi encontrado", 400


@app.route("/criar_user/", methods=["POST"])
def post_user():
    """   Espera receber
    {
    "nome": str,
    "cpf": "str que depois retirará '.,-/' para persistir,
    "email": str,
    "phone_number": str,
    }
    """
    body_request = request.get_json()
    # CHECA SE OS 4 CAMPOS FORAM PASSADOS
    for i in list(body_request.keys()):
        if i not in ['nome', 'cpf', 'email', 'phone_number']:
            return "Campos faltantes", 400
    retorno = User().validar_campos(body_request)
    if not isinstance(retorno, dict):
        return retorno #que será uma mensagem de erro
    retorno["id"] = User().gerar_id_user()
    if User().cadastrar_user(retorno):
        return "Usuário Cadastrado com sucesso!", 200
    return "Usuário não Cadastrado. Problema no banco de dados.", 400


@app.route("/alterar_user/<id>/", methods=["PUT"])
def put_user(id):
    """
    Passar o id do usero na url e informar pelo menos uma
    das keys (que constam na descrição de 'criar_user' neste arquivo
    """
    if not User().checar_id_exists(id):
         return "Id do usuário inválido.", 400
    body_request = request.get_json()
    if len(body_request) < 1:
        return "Nenhum valor de atualização passado", 400
    retorno = User().validar_campos(body_request)
    if not isinstance(retorno, dict):
        return retorno #que será uma mensagem de erro
    if User().atualizar_user(id, retorno):
        return f"Usuário {id} alterado com sucesso!"
    return f"Ops, usuário {id} não foi alterado."


@app.route("/excluir_user/<id>/", methods=["DELETE"])
def delete_user(id):
    if not User().checar_id_exists(id):
         return "Id do usuário inválido.", 400
    if User().excluir_user(id):
        return f"Usuário {id} excluído com sucesso", 200
    return f"Ops, usuário {id} não foi excluído.", 400


app.run(debug=True, port=5001)

