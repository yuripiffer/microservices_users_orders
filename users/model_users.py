import uuid
from db_users import DbUser
from datetime import datetime
# datetime.strptime(datetime.now, "%d/%m/%Y - %H:%M:%S")
import cpf_tools


class User:

    def retornar_user(self, id=None) -> dict or bool:
        if id:
            if self.checar_id_exists(id):
                query = f"SELECT * from user WHERE id= '{id}'"
                retorno = DbUser().retornar_do_db(query)
                return retorno
        query = f"SELECT * from user"
        retorno = DbUser().retornar_do_db(query)
        return retorno

    def gerar_id_user(self):
        """
        Gera um id pelo uuid e pega os 8 primeiro números.
        Caso já exista este id no db, gera outro
        :return: id de 8 números
        """
        while True:
            id = str(uuid.uuid1())[0:8]
            query = f"SELECT * from user WHERE id={id}"
            if not DbUser().retornar_do_db(query):
                return id

    def validar_campos(self, body_request) -> dict or tuple:
        lista_keys = list(body_request.keys())
        final_dict = {}
        if "nome" in lista_keys:
            nome = (body_request["nome"]).upper()
            if len(nome) < 3:
                return "Nome inválido", 400
            final_dict["nome"] = nome
        if "cpf" in lista_keys:
            cpf = self.checar_cpf_valido(body_request["cpf"])
            if not cpf:
                return "CPF inválido", 400
            final_dict["cpf"] = cpf
        if "email" in lista_keys:
            email = body_request["email"]
            if not self.checar_email_valido(email):
                return "Email inválido", 400
            final_dict["email"] = email
        if "phone_number" in lista_keys:
            phone_number = body_request["phone_number"]
            if not self.checar_telefone_valido(phone_number):
                return "Telefone inválido", 400
            final_dict["phone_number"] = phone_number
        return final_dict


    def checar_id_exists(self, id) -> bool:
        query = f"SELECT * from user WHERE  id= '{id}' "
        if DbUser().retornar_do_db(query):
            return True

    def checar_cpf_valido(self, cpf) -> str or bool:
        cpf = str(cpf).replace(".", "").replace("-", "")
        if cpf_tools.cpf_str_validation(cpf):
            return cpf
        return False

    def checar_email_valido(self, email) -> str or bool:
        # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # if re.search(regex, email):
        #     return True
        # return False
        return email


    def checar_telefone_valido(self, phone_number) -> str or bool:
        #TENTAR ACHAR ALGO QUE FAÇA ISSO, #POR ENQUANTO SÓ RETORNA O NÚMERO DE TELEFONE
        return phone_number

    def cadastrar_user(self, dict) -> bool:
        created_at = datetime.now()
        query = f" INSERT INTO user (id, nome, cpf, email, phone_number, created_at) " \
                f" VALUES ('{dict['id']}', '{dict['nome']}', '{dict['cpf']}', '{dict['email']}', " \
                f" '{dict['phone_number']}',  '{created_at}' ) "
        if DbUser().persistir_no_db(query):
            return True
        return False

    def atualizar_user(self, id, dict_update):
        frase_sql_set = self.convert_dict_to_sql_string(dict_update, separator= ",")
        frase_sql_set += f" , updated_at = '{datetime.now()}'  "
        query = f"UPDATE user SET {frase_sql_set} WHERE id = '{id}' "
        if DbUser().persistir_no_db(query):
            return True
        return False

    def excluir_user(self, id):
        query = f"DELETE FROM user WHERE id = '{id}'"
        if DbUser().persistir_no_db(query):
            return True
        return False



####### /////////////////////////   AUXILIARES   /////////////////////////

    def convert_dict_to_sql_string(self, data: dict, separator=",") -> str:
        """
        Método utilizado no crud_update. Recebe dicionário e retonra parte
        da string do MySQL.
        :param data: dict com keys (colunas do db) e values (valores a
        serem atualizados)
        :return: string adaptada para a query do MySQL
        """
        converted_to_sql_data = []
        for key, value in data.items():
            if isinstance(value, str) and value.upper() != "DEFAULT" and value.upper() != "NULL":
                converted_to_sql_data.append(f"{key} = '{value}'")
            else:
                converted_to_sql_data.append(f"{key} = {value}")
        string_values = f"{separator}".join(converted_to_sql_data)
        return string_values

