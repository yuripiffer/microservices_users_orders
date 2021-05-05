from model_users import User
from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "MICROSERVICES - USERS"


@app.route("/listar/<id>/", methods=["GET"])
@app.route("/listar/", methods=["GET"])
def get_users(id=None):
    response = User().retornar_user(id)
    if response:
        return response
    return "Nenhum valor foi encontrado", 400


@app.route("/criar/", methods=["POST"])
def post_user():
    """
    recebe no corpo um dicionário:
    {"nome" = nome, "cpf" = cpf, "email" = email, "phone_number"= phone_number},
    Depois valida e manipula os campos, gera id e persiste os dados.
    :return: mensagem de sucesso ou erro.
    """
    body_request = request.get_json()

    nome = body_request["nome"]
    if nome is None:
        return "Nome inválido", 400
    cpf = User().checar_cpf_valido(body_request["cpf"])
    if not cpf:
        return "CPF inválido", 400
    email = body_request["email"]
    if not User().checar_email_valido(email):
        return "Email inválido", 400
    phone_number = body_request["phone_number"]
    if not User().checar_telefone_valido(phone_number):
        return "Telefone inválido", 400
    id = User().gerar_id_user()

    if User().cadastrar_user(dict(id=id, nome=nome, cpf=cpf, email=email, phone_number=phone_number)):
        return "Usuário Cadastrado com sucesso!", 200
    return "Usuário não Cadastrado. Problema no banco de dados.", 400


@app.route("/alterar/<id>", methods=["PUT"])
def put_user(id):
    if not User().checar_id_exists(id):
         return "Id do usuário inválido.", 400
    body_request = request.get_json()
    if not body_request:
        return "Nenhum valor de atualização passado", 400
    if User().atualizar_user(id, body_request):
        return f"Usuário {id} alterado com sucesso!"
    return f"Ops, usuário {id} não foi alterado."


@app.route("/excluir/<id>/", methods=["DELETE"])
def delete_user(id):
    if not User().checar_id_exists(id):
         return "Id do usuário inválido.", 400
    if User().excluir_user(id):
        return f"Usuário {id} excluído com sucesso"
    return f"Ops, usuário {id} não foi excluído."


app.run(debug=True)

