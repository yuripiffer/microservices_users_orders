from db_orders import DbOrder
from datetime import datetime
import requests

class Orders:

    # Tenta utilizar o id passado, ou retorna todos os pedidos
    def retornar_order(self, id_qualquer):
        if id_qualquer:
            retorno = self.retornar_pedido_por_id_pedido(id_qualquer)
            if retorno:
                return retorno
            retorno = self.retornar_pedidos_do_user(id_qualquer)
            if retorno:
                return retorno
        else:
            return self.retornar_todos_pedidos()

    # Lista com dicionário de pedido com nome do cliente,
    # 'id_qualquer' se comporta como id do pedido
    def retornar_pedido_por_id_pedido(self, id_pedido):
       if self.checar_id_order_exists(id_pedido):
           print("DEU AQUI")
           query = f"SELECT * from orders WHERE id= '{id_pedido}'"
           lista_dicts_retorno = DbOrder().retornar_do_db(query)
           return self.adicionar_nome_cliente_nos_pedidos(lista_dicts_retorno)

    # Lista de dicionários de pedidos do user com nome do cliente,
    # 'id_qualquer' se comporta como id_user
    def retornar_pedidos_do_user(self, id_user):
        nome_user_api = self.checar_id_user_exists(id_user)
        if nome_user_api:
            query = f"SELECT * from orders WHERE user_id= '{id_user}'"
            lista_dicts_retorno = DbOrder().retornar_do_db(query)
            return self.adicionar_nome_cliente_nos_pedidos(lista_dicts_retorno)

    # Lista com dicionários de todos os pedidos com nome do cliente,
    def retornar_todos_pedidos(self):
        query = f"SELECT * from orders"
        lista_dicts_retorno = DbOrder().retornar_do_db(query)
        return self.adicionar_nome_cliente_nos_pedidos(lista_dicts_retorno)

    # Percorre a lista de pedidos e adiciona a key 'nome_cliente' chamando API externa
    def adicionar_nome_cliente_nos_pedidos(self, lista_dict_pedidos):
        for dict_pedido in lista_dict_pedidos:
            user_id = dict_pedido["user_id"]
            dict_pedido["nome_cliente"] = self.checar_id_user_exists(user_id)
        return {"Resultado": lista_dict_pedidos}

    # Checa se todos os itens obrigatórios existem como key
    def pedido_completo(self, body_request):
        for i in list(body_request.keys()):
            if i not in ['user_id', 'item_description',
                         'item_quantity', 'item_price', 'total_value']:
                return False
        return True

    # Cria a string e chama todas as funções de validação
    # Funciona tanto para post quanto put
    def validar_campos(self, body_request) ->tuple or dict:
        lista_keys = list(body_request.keys())
        final_dict = {}
        lista_campos_db = ['user_id', 'item_description','item_quantity','item_price','total_value']
        for i in lista_campos_db:
            if i in lista_keys:
                nome_func = getattr(self, "validar_" + str(i))
                retorno = nome_func(body_request)
                if retorno[0] == False:
                    return retorno[1:]
                final_dict[str(i)] = retorno[1]
        return final_dict

    # Função chamada em 'validar_campos()'
    def validar_user_id(self, body_request):
        user_id = body_request['user_id']
        if not self.checar_id_user_exists(user_id):
            return False, "User_id inválido", 400
        return True, user_id

    # Função chamada em 'validar_campos()'
    def validar_item_description(self, body_request):
        item_description = body_request['item_description']
        if len(item_description) < 5:
            return False,"Descrição do item inválida", 400
        return True, item_description

    # Função chamada em 'validar_campos()'
    def validar_item_quantity(self, body_request):
        item_quantity = body_request['item_quantity']
        if not (isinstance(item_quantity, int) and item_quantity > 0):
            return False, "Quantidade de itens inválida", 400
        return True, item_quantity

    # Função chamada em 'validar_campos()'
    def validar_item_price(self, body_request):
        item_price = body_request['item_price']
        if not item_price > 0:
            return False, "Preço por item inválido", 400
        return True, item_price

    # Função chamada em 'validar_campos()'
    def validar_total_value(self, body_request):
        item_quantity = body_request['item_quantity']
        item_price =  body_request['item_price']
        total_value = body_request['total_value']
        if item_price * item_quantity != total_value:
            return False, "Valor total não confere com preço por unidade e número de itens", 400
        return True, total_value

    # USO DE API EXTERNA
    # Chega se o id_user existe e retonra o nome do cliente
    def checar_id_user_exists(self, id) -> bool:
        query = f"SELECT * from user WHERE  id= '{id}' "
        resultado_api_user = requests.get(f"http://localhost:5001/listar_user/{id}/").json()
        if len(resultado_api_user) == 1:
            return resultado_api_user[0]["nome"]

    def checar_id_order_exists(self, id) -> bool:
        query = f"SELECT * from orders WHERE  id= '{id}' "
        if DbOrder().retornar_do_db(query):
            return True

    # Constrói a query e persiste
    def cadastrar_orders(self, dict):
        created_at = datetime.now()
        query = f" INSERT INTO orders (user_id, item_description, item_quantity, item_price, total_value, created_at) " \
                f" VALUES ('{dict['user_id']}', '{dict['item_description']}', '{dict['item_quantity']}', '{dict['item_price']}', " \
                f" '{dict['total_value']}',  '{created_at}' ) "
        if DbOrder().persistir_no_db(query):
            return True
        return False

    # Constrói a query e persiste
    def atualizar_order(self, id, dict_update):
        frase_sql_set = self.convert_dict_to_sql_string(dict_update, separator= ",")
        frase_sql_set += f" , updated_at = '{datetime.now()}'  "
        query = f"UPDATE orders SET {frase_sql_set} WHERE id = '{id}' "
        if DbOrder().persistir_no_db(query):
            return True
        return False

    # Constrói a query e persiste
    def excluir_order(self, id):
        query = f"DELETE FROM orders WHERE id = '{id}'"
        if DbOrder().persistir_no_db(query):
            return True
        return False

####### /////////////////////////   AUXILIARES   /////////////////////////

    def convert_dict_to_sql_string(self, data: dict, separator=",") -> str:
        converted_to_sql_data = []
        for key, value in data.items():
            if isinstance(value, str) and value.upper() != "DEFAULT" and value.upper() != "NULL":
                converted_to_sql_data.append(f"{key} = '{value}'")
            else:
                converted_to_sql_data.append(f"{key} = {value}")
        string_values = f"{separator}".join(converted_to_sql_data)
        return string_values