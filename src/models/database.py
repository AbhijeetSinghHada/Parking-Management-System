import mysql.connector

from src.configurations import config
from src.controllers.slot import Slot


class Database:
    connection = None
    cursor = None

    def __init__(self):
        self.last = None
        if Database.connection is None:
            try:
                Database.connection = mysql.connector.connect(**config.connection_parameters)
                Database.cursor = Database.connection.cursor()
            except Exception as error:
                print(f"Error: Connection not established {error}")
            else:
                print("Connection established")

        self.connection = Database.connection
        self.cursor = Database.cursor
        self._last = None

    def get_item(self, query, *args):
        self.cursor.execute(query,*args)
        item = self.cursor.fetchone()
        return item

    def get_multiple_items(self, query, *args):
        self.cursor.execute(query,*args)
        items = self.cursor.fetchall()
        return items

    def update_item(self, query, *args):
        self.cursor.execute(query, *args)
        last = self.cursor.lastrowid
        self.connection.commit()
        return last



if __name__ == "__main__":
    he = Database()
    slot = Slot(he)
    slot.generate_bill('11')
