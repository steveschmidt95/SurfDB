import mysql.connector
from mysql.connector import Error

class Connection:

    def __init__(self, host_name, user_name, user_password):
        self.user_password = user_password
        self.user_name = user_name
        self.host_name = host_name

    def create_connection(self, ):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection
