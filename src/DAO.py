

class DAO:

    def __init__(self):
        connection = Connection()
        self.connection = connection.create_connection()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")