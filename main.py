
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from Connection import Connection

if __name__ == '__main__':
    connection = Connection("localhost", "root", "bigchopfun")
    connection.create_connection()


