from __future__ import annotations
from typing import Self 
from src.classes.db_record import Record


class MaintenanceType(Record): 
    def __init__(self, maintenance_type:str, description:str, id:int|None=None):
        super().__init__()
        self.id = id 
        self.maintenance_type = maintenance_type 
        self.description = description

    def __str__(self) -> str:
        return f"id: {self.id}\nerror_code: {self.maintenance_type}\ndescription: {self.description}"
    
    def __repr__(self) -> str:
        return(f"MaintenanceType({self.maintenance_type})")

    @classmethod
    def get_by_name(cls, maintenance_type:str) -> Self|ValueError:
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT
                id, 
                maintenance_type,
                description
            FROM maintenance_types 
            WHERE maintenance_type = ?
            """, 
            (maintenance_type, )
        )
        extracted = cursor.fetchone()
        return cls(maintenance_type=extracted['maintenance_type'], 
                   description=extracted['description'], 
                   id=extracted['id']) if extracted else ValueError("Maintenance type is not found!") 
    
    @classmethod
    def get_by_id(cls, id:int) -> Self|ValueError:
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT id, maintenance_type, description FROM maintenance_types 
            WHERE id = ? 
            """, 
            (id, ) 
        )
        extracted = cursor.fetchone()

        return cls(maintenance_type=extracted['maintenance_type'], 
                   description=extracted['description'], 
                   id=extracted['id']) if extracted else ValueError("Maintenance type is not found!") 

    def save(self): 
        if self.id is None and isinstance(MaintenanceType.get_by_name(self.maintenance_type), ValueError): 
            self.cursor.execute(
                """
                INSERT INTO maintenance_types(maintenance_type, description)
                VALUES(?, ?)
                RETURNING id
                """,
                (self.maintenance_type, self.description)
            )
           
            extracted = self.cursor.fetchone()
            self.connection.commit()
            self.id = extracted['id']

        elif self.id:
            self.cursor.execute(
                """
                UPDATE maintenance_types  
                SET maintenance_type = ?, 
                    description = ?
                WHERE id = ?
                """,
                (self.maintenance_type, self.description, self.id)
            )
            self.connection.commit()
        else: 
            raise ValueError("Record is already present in the database! Use MaintenanceType.get_by_name instead")
        
    def delete(self) -> None: 
        self.cursor.execute(
            """
            DELETE FROM maintenance_types WHERE id=? 
            """,
            (self.id, )
        )
        self.connection.commit()
        self.__dict__.clear()
    
    @classmethod    
    def get_all(cls) -> list[Self]:
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT id, maintenance_type, description FROM maintenance_types
            """
        )
        extracted = cursor.fetchall()
        maintenance_types = []
        for row in extracted:
            maintenance_type_instance = cls(maintenance_type=row['maintenance_type'], description=row['description'], id=row['id'])
            maintenance_types.append(maintenance_type_instance)
        return maintenance_types
