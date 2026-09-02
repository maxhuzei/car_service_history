from __future__ import annotations
from typing import Self
from src.classes.db_record import Record
from datetime import datetime

class MaintenanceEntry(Record):
    def __init__(self, maintenance_event:str, dtc_code:str, symptoms:str, comment:str, cost:float, date_created:datetime|None=None, id:int|None=None):
        super().__init__()

        self.id = id
        self.maintenance_event = maintenance_event
        self.dtc_code = dtc_code
        self.symptoms = symptoms
        self.comment = comment
        self.cost = cost
        if date_created is None: 
            date_created = datetime.now()
        self.date_created = date_created

    def __str__(self) -> str:
        return f"id:{self.id}, maintenance_event:{self.maintenance_event}, dtc_code:{self.dtc_code}, symptoms:{self.symptoms}, comment:{self.comment}, cost:{self.cost}, date_created:{self.date_created}"

    def __repr__(self) -> str:
        return f"MaintenanceEntry({self.maintenance_event}, {self.dtc_code})"

    @classmethod
    def get_by_id(cls, id): 
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT 
                id, 
                maintenance_event, 
                dtc_code,
                symptoms, 
                comment,
                cost,
                date_created
            FROM maintenance_entries
            WHERE id = ? 
            """, 
            (id, )
        )

        extracted = cursor.fetchone()
        return cls(
            id = extracted['id'],
            maintenance_event = extracted['maintenance_event'], 
            dtc_code = extracted['dtc_code'],
            symptoms = extracted['symptoms'],
            comment = extracted['comment'],
            cost = float(extracted['cost']),
            date_created = datetime.fromisoformat(extracted['date_created'])
        )

    @classmethod
    def get_all(cls): 
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT 
                id,
                maintenance_event, 
                dtc_code, 
                symptoms, 
                comment,
                cost,
                date_created
            FROM maintenance_entries
            ORDER BY date_created DESC
            """
        )

        extracted = cursor.fetchall()
        maintenance_entries = []
        for row in extracted: 
            maintenance_entries.append(
                cls(
                    id=int(row['id']), 
                    maintenance_event = row['maintenance_event'],
                    dtc_code = row['dtc_code'],
                    symptoms = row['symptoms'],
                    comment = row['comment'],
                    cost = float(row['cost']),
                    date_created = datetime.fromisoformat(row['date_created'])
                )
            )
        return maintenance_entries

    def save(self): 
        if self.id is None:
            self.cursor.execute(
                """
                INSERT INTO maintenance_entries (
                    maintenance_event, 
                    dtc_code, 
                    symptoms,
                    comment,
                    cost,
                    date_created
                ) VALUES (
                ?, ?, ?, ?, ?, ?
                )
                RETURNING id
                """, (
                    self.maintenance_event,
                    self.dtc_code,
                    self.symptoms,
                    self.comment,
                    self.cost,
                    datetime.isoformat(self.date_created)
                )
            )
            extracted = self.cursor.fetchone()
            self.connection.commit()
            self.id = extracted["id"]

        elif self.id is not None: 
            self.cursor.execute(
                """
                UPDATE maintenance_entries SET
                    maintenance_event = ?,
                    dtc_code = ?, 
                    symptoms = ?, 
                    comment = ?,
                    cost = ?,
                    date_created = ?
                WHERE id = ?
                """,
                (
                    self.maintenance_event,
                    self.dtc_code, 
                    self.symptoms,
                    self.comment,
                    self.cost,
                    datetime.isoformat(self.date_created),
                    self.id
                )
            )
            self.connection.commit()
        else: 
            raise ValueError("Object exists, but is not found in the database. Restart application or check the data integrity.")

    def delete(self): 
        if self.id is not None: 
            self.cursor.execute(
                """
                DELETE FROM maintenance_entries
                WHERE id = ? 
                """, 
                (self.id, )
            )
            self.connection.commit()
            self.__dict__.clear()
        else: 
            self.__dict__.clear()
