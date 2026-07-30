import sqlite3
from src.classes.db_record import Record

class GeneralSettings(Record):
    def __init__(self, car_model:str|None=None, max_fuel_ammount:str|None=None) -> None:
        super().__init__()
        self.cursor.execute(
            """
            SELECT key, value FROM general_settings
            """
        )
        records = dict(self.cursor.fetchall())
        self.car_model = records['car_model']
        self.max_fuel_ammount = records['max_fuel_ammount']
    
        
    def __str__(self) -> str:
        return f"car_model: {self.car_model}\nmax_fuel_ammount:{self.max_fuel_ammount}"

    def __repr__(self) -> str:
       return f"GeneralSettings({self.car_model, self.max_fuel_ammount})"

    def save(self) -> None: 
        _db_entries = [item for item in self.__dict__.keys() if item not in Record().__dict__.keys()]
        for item in _db_entries:
            self.cursor.execute(
                """
                UPDATE general_settings 
                SET value = ? 
                WHERE key = ? 
                """, 
                (self.__dict__.get(item), item)
            )

        self.connection.commit()
