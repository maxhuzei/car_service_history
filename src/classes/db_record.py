import sqlite3
from src.helpers import get_db_connection_from_config

class Record:
    _connection = None

    def __init__(self):
        if Record._connection is None: 
            Record._connection = sqlite3.connect(get_db_connection_from_config())

        self.connection = Record._connection
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    @classmethod
    def get_db_cursor(cls): 
        if Record._connection is None: 
            Record._connection = sqlite3.connect(get_db_connection_from_config())
        connection = Record._connection 
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return cursor