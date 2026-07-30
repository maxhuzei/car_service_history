import json 
import os 
import sqlite3

def get_db_path(config_path:str) -> str:
    """
    Checks if config file is provided and can be read. 
    Parameters: 
        config path:str - path to the application config
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError #TODO: add some aguments to make it clear which file does not exists
    else: 
        with open(config_path) as config: 
            config_text = json.loads(config.read())

            return config_text['db']

def check_if_table_exists(connection:sqlite3.Connection, table:str) -> bool:
    """ 
    Check if the table already exists in the database. 
    Parameters: 
        connection - connection to the sqlite database 
        table:str - name of the table to check for existence
    """
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT count(name)
        FROM sqlite_master
        WHERE type='table' AND name = ?
        """, 
        (table, )
    )
    return cursor.fetchone()[0]==1

# 
def create_general_settings(connection:sqlite3.Connection) -> None: 
    params_for_general_settings = {'car_model', 'max_fuel_ammount'}
    cursor = connection.cursor()
    # check if table already exists 
    if check_if_table_exists(connection, "general_settings"): 
        # check if the parameters are set
        cursor.execute(
            """
            SELECT key
            FROM general_settings
            """
        )
        available_keys = set([item for tpl in cursor.fetchall() for item in tpl])
        test = params_for_general_settings.difference(available_keys)
        for key in params_for_general_settings.difference(available_keys):
            try: 
                cursor.execute(
                    """
                    INSERT INTO general_settings
                    VALUES(?, NULL)
                    """, 
                    (key,)
                )
                connection.commit()
                print(f"{key} was missing and has been successfully initialized!")
            except: 
                raise
    else:
        try:
            cursor.execute(
                """
                CREATE TABLE general_settings(
                    key NVARCHAR NOT NULL,
                    value NVARCHAR
                )
                """
            )
            print("Table general_settings has been successfully initialized!")
            for key in params_for_general_settings:
                cursor.execute(
                    """
                    INSERT INTO general_settings
                    VALUES(?, NULL)
                    """, 
                    (key, )
                )
                connection.commit()
                print(f"{key} has been successfully added!")
        except:
            raise

def create_error_codes(connection:sqlite3.Connection) -> None:
    try:
        if not check_if_table_exists(connection, 'error_codes'): 
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE error_codes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    error_code NVARCHAR NOT NULL, 
                    description NVARCHAR
                )
                """
            )
            print("Table error_codes has been successfully initialized!")
    except: 
        raise

def create_maitenance_types(connection:sqlite3.Connection) -> None:
    try:
        if not check_if_table_exists(connection, 'maintenance_types'):
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE maintenance_types(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    maintenance_type NVARCHAR NOT NULL, 
                    description NVARCHAR
                )
                """
            )
            print("Table maintenance_types has been succesfully initialized!")
    except:
        raise

def create_fuel_refill_entries(connection:sqlite3.Connection) -> None: 
    try: 
        if not check_if_table_exists(connection, 'fuel_refill_entries'): 
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE fuel_refill_entries(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    refuel_date TEXT, 
                    current_mileage INT, 
                    refuel_amount INT, 
                    refuel_cost REAL
                )
                """
            )
            connection.commit()
            print("Table fuel_refill_entires has been successfully initialized!")
    except:
        raise

def intialize_db() -> None: 
    db_path = get_db_path(r".config")
    connection = sqlite3.connect(db_path)
    create_general_settings(connection)
    create_error_codes(connection)
    create_maitenance_types(connection)
    create_fuel_refill_entries(connection)

intialize_db()