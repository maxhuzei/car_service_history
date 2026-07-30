from __future__ import annotations
from typing import Self
from src.classes.db_record import Record

class ErrorCode(Record):
    def __init__(self, error_code:str, description:str, id:int|None=None,) -> None:
        super().__init__()
        self.id = id 
        self.error_code = error_code
        self.description = description
    
    def __str__(self) -> str:
        return f"id: {self.id}\nerror_code: {self.error_code}\ndescription: {self.description}"
    
    def __repr__(self) -> str:
        return(f"ErrorCode({self.error_code})")

    @classmethod
    def get_by_name(cls, error_code:str) -> Self|ValueError:
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT
                id, 
                error_code,
                description
            FROM error_codes 
            WHERE error_code = ?
            """, 
            (error_code, )
        )
        extracted = cursor.fetchone()
        return cls(error_code=extracted['error_code'], 
                   description=extracted['description'], 
                   id=extracted['id']) if extracted else ValueError("Error code is not found!") 
    
    @classmethod
    def get_by_id(cls, id:int) -> Self|ValueError:
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT id, error_code, description FROM error_codes 
            WHERE id = ? 
            """, 
            (id, ) 
        )
        extracted = cursor.fetchone()

        return cls(error_code=extracted['error_code'], 
                   description=extracted['description'], 
                   id=extracted['id']) if extracted else ValueError("Error code is not found!") 

    def save(self): 
        if self.id is None and isinstance(ErrorCode.get_by_name(self.error_code), ValueError): 
            self.cursor.execute(
                """
                INSERT INTO error_codes(error_code, description)
                VALUES(?, ?)
                RETURNING id
                """,
                (self.error_code, self.description)
            )
           
            extracted = self.cursor.fetchone()
            self.connection.commit()
            self.id = extracted['id']
        elif self.id:
            self.cursor.execute(
                """
                UPDATE error_codes 
                SET error_code = ?, 
                    description = ?
                WHERE id = ?
                """,
                (self.error_code, self.description, self.id)
            )
            self.connection.commit()
        else: 
            raise ValueError("Record is already present in the database! Use ErrorCode.get_by_name instead")
        
    def delete(self) -> None: 
        self.cursor.execute(
            """
            DELETE FROM error_codes WHERE id=? 
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
            SELECT id, error_code, description FROM error_codes
            """
        )
        extracted = cursor.fetchall()
        error_codes = []
        for row in extracted:
            error_code_instance = cls(error_code=row['error_code'], description=row['description'], id=row['id'])
            error_codes.append(error_code_instance)
        return error_codes
