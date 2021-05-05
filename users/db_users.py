import MySQLdb
import pandas as pd

class DbUser:
    def __init__(self):
        self.HOST = "localhost"
        self.USER = "root"
        self.PASSWORD = ""
        self.PORT = 3306
        self.DB_NAME = "microservices_users_orders_db"
        self.conn = MySQLdb.connect(host=self.HOST, user=self.USER, password=self.PASSWORD,
                                    port=self.PORT, db=self.DB_NAME)
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()


    def persistir_no_db(self, query) -> bool:
        try:
            affected_rows = self.cursor.execute(query)
            if affected_rows > 0:
                return True
        except:
            return False

    def retornar_do_db(self, query)-> dict or bool:
        try:
            affected_rows = self.cursor.execute(query)
            if affected_rows > 0:
                columns = [i[0] for i in self.cursor.description]
                df = pd.DataFrame(self.cursor.fetchall(), columns=columns)
                dict_resposta = df.to_json(orient="records")
                return dict_resposta
        except:
            return False
