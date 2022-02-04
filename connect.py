import psycopg2 as p2

class DBHandler:
    def __init__(self):
        self.connection = p2.connect(user="admin",
                                    password="quest",
                                    host="127.0.0.1",
                                    port="8812",
                                    database="qdb")

    def query(self, q):
        with self.connection as c:
            cursor = c.cursor()
            res = cursor.execute(q)
            return res
    
    def __del__(self):
        print('Connections closed')
        self.connection.close()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()
if __name__ == '__main__':
    handler = DBHandler()
