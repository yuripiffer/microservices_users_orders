from orders.db_orders import DbOrder
from datetime import datetime


class Orders:

    def retornar_order(self, id_qualquer):
        if id_qualquer:
            if self.checar_id_user_exists(id_qualquer):
                query = f"SELECT * from user WHERE id= '{id_qualquer}'"
                retorno = DbOrder().retornar_do_db(query)
                return retorno

            else:
                if self.checar_id_order_exists(id_qualquer):
                    query = f"SELECT * from orders WHERE id= '{id_qualquer}'"
                    retorno = DbOrder().retornar_do_db(query)
                    return retorno

        else:
            query = f"SELECT * from orders"
            print(query)
            retorno = DbOrder().retornar_do_db(query)
            return retorno


    def validar_campos(self, body_request) ->tuple or dict:
        lista_keys = list(body_request.keys())
        final_dict = {}
        if 'user_id' in lista_keys:
            if not self.checar_id_user_exists(body_request["user_id"]):
                return "User_id inválido", 400
            final_dict["user_id"] = body_request["user_id"]
        if 'item_description' in lista_keys:
            if len('item_description') <5:
                return "Descrição do item inválida", 400
            final_dict["item_description"] = body_request["item_description"]
        if 'item_quantity' in lista_keys:
            if not (isinstance(body_request['item_quantity'], int) and
                    body_request['item_quantity']>0):
                return "Quantidade de itens inválida", 400
            final_dict["item_quantity"] = body_request["item_quantity"]
        if 'item_price' in lista_keys:
            if not body_request['item_price'] > 0:
                return "Preço por item inválido", 400
            final_dict["item_price"] = body_request["item_price"]
        if 'total_value' in lista_keys:
            if body_request['item_price'] * body_request['item_quantity'] != body_request['total_value']:
                return "Valor total não confere com preço por unidade e número de itens", 400
            final_dict['total_value'] = body_request['total_value']
        return final_dict

    def checar_id_user_exists(self, id) -> bool:
        query = f"SELECT * from user WHERE  id= '{id}' "
        if DbOrder().retornar_do_db(query):
            return True

    def checar_id_order_exists(self, id) -> bool:
        query = f"SELECT * from orders WHERE  id= '{id}' "
        if DbOrder().retornar_do_db(query):
            return True

    def cadastrar_orders(self, dict):
        created_at = datetime.now()
        query = f" INSERT INTO orders (user_id, item_description, item_quantity, item_price, total_value, created_at) " \
                f" VALUES ('{dict['user_id']}', '{dict['item_description']}', '{dict['item_quantity']}', '{dict['item_price']}', " \
                f" '{dict['total_value']}',  '{created_at}' ) "
        if DbOrder().persistir_no_db(query):
            return True
        return False


    def atualizar_order(self, id, dict_update):
        frase_sql_set = self.convert_dict_to_sql_string(dict_update, separator= ",")
        frase_sql_set += f" , updated_at = '{datetime.now()}'  "
        query = f"UPDATE orders SET {frase_sql_set} WHERE id = '{id}' "
        if DbOrder().persistir_no_db(query):
            return True
        return False

    def excluir_order(self, id):
        query = f"DELETE FROM orders WHERE id = '{id}'"
        if DbOrder().persistir_no_db(query):
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