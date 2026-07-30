import json 

def get_db_connection_from_config(): 
    config_path = ".config"
    with open(config_path) as config: 
        return json.loads(config.read())['db']