import mysql.connector
from mysql.connector import Error


class Connection:

    def __init__(self):
        self.user_password = "bigchopfun"
        self.user_name = "root"
        self.host_name = "localhost"
        self.database = 'surfdb'

    def create_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                database=self.database
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection
