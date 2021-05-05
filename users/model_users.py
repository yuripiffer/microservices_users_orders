import uuid
from users.db_users import DbUser
from datetime import datetime
# datetime.strptime(datetime.now, "%d/%m/%Y - %H:%M:%S")


class User:


    def retornar_user(self, id=None) -> dict or bool:
        if id:
            if self.checar_id_exists(id):
                query = f"SELECT * from user WHERE id={id}"
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
            id = uuid.uuid1()
            id = id[0:8]
            query = f"SELECT * from user WHERE id={id}"
            if not DbUser().retornar_do_db(query):
                return id

    def checar_id_exists(self, id) -> bool:
        query = f"SELECT * from user WHERE id={id}"
        if DbUser().retornar_do_db(query):
            return True

    def checar_cpf_valido(self, cpf) -> str or bool:
        cpf = str(cpf).replace(".", "").replace("-", "")
        if cpf_tools.cpf_str_validation(cpf):
            return cpf
        return False

    def checar_email_valido(self, email) -> str or bool:
        #retorna o email validado ou false
        pass

    def checar_telefone_valido(self, phone_number) -> str or bool:
        #recebe o str phone_number e retorna ele validado/formatado ou False
        pass

    def cadastrar_user(self, dict) -> bool:
        created_at = datetime.now()
        query = f" INSERT INTO user (id, nome, cpf, email, phone_number, created_at) " \
                f" VALUES ({dict['id']}, {dict['nome']}, {dict['cpf']}, {dict['email']}, " \
                f" {dict['phone_number']},  {created_at} ) "
        if DbUser().persistir_no_db(query):
            return True
        return False

    def atualizar_user(self, id, dict_update):
        frase_sql_set = self.convert_dict_to_sql_string(dict_update, separator= ",")
        query = f"UPDATE user SET {frase_sql_set} WHERE id = {id} "
        if DbUser().persistir_no_db(query):
            return True
        return False

    def excluir_user(self, id):
        query = f"DELETE FROM user WHERE id = {id}"
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

