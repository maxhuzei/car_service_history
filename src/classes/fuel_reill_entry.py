from __future__ import annotations
from typing import Self
from src.classes.db_record import Record
from datetime import datetime

class FuelRefillEntry(Record):
    def __init__(self, refuel_date:datetime, current_mileage:int, refuel_amount:int, refuel_cost:float, avg_consumption:float|None=None, id:int|None=None):
        super().__init__()
        self.id = id
        self.refuel_date = refuel_date
        self.current_mileage = current_mileage
        self.refuel_amount = refuel_amount
        self.refuel_cost = refuel_cost
        self.avg_consumption = avg_consumption

    def __str__(self) -> str:
        return f"id:{self.id}, refuel date:{self.refuel_date}, current_mileage:{self.current_mileage}, refuel_amount:{self.refuel_amount}, refuel_cost:{self.refuel_cost}"

    def __repr__(self) -> str:
        return f"FuelRefillEntry({self.refuel_date}, {self.refuel_amount})"

    @classmethod
    def get_by_id(cls, id): 
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT 
                id, 
                refuel_date, 
                current_mileage,
                refuel_amount, 
                refuel_cost
            FROM fuel_refill_entries
            WHERE id = ? 
            """, 
            (id, )
        )

        extracted = cursor.fetchone()
        return cls(
            id = extracted['id'],
            refuel_date = datetime.fromisoformat(extracted.get('refuel_date')), 
            current_mileage = int(extracted.get('current_mileage')),
            refuel_amount = int(extracted.get('refuel_amount')),
            refuel_cost = float(extracted.get('refuel_cost'))
        )

    @classmethod
    def get_all(cls): 
        cursor = cls.get_db_cursor()
        cursor.execute(
            """
            SELECT 
                id,
                refuel_date, 
                current_mileage, 
                refuel_amount, 
                refuel_cost
            FROM fuel_refill_entries
            """
        )

        extracted = cursor.fetchall()
        fuel_refill_entries = []
        for row in extracted: 
            fuel_refill_entries.append(
                cls(
                    id=int(row.get('id')), 
                    refuel_date = datetime.fromisoformat(row.get('refuel_date')),
                    current_mileage = int(row.get('current_mileage')),
                    refuel_amount = int(row.get('refuel_amount')), 
                    refuel_cost = float(row.get('refuel_cost'))
                )
            )
        return fuel_refill_entries

    def save(self): 
        if self.id is None:
            self.cursor.execute(
                """
                INSERT INTO fuel_refill_entries (
                    refuel_date, 
                    current_mileage, 
                    refuel_amount,
                    refuel_cost
                ) VALUES (
                ?, ?, ?, ?
                )
                RETURNING id
                """, (
                    datetime.isoformat(self.refuel_date),
                    self.current_mileage,
                    self.refuel_amount,
                    self.refuel_cost
                )
            )
            extracted = self.cursor.fetchone()
            self.connection.commit()
            self.id = extracted["id"]

        elif self.id is not None: 
            self.cursor.execute(
                """
                UPDATE fuel_refill_entries SET
                    refuel_date = ?,
                    current_mileage = ?, 
                    refuel_amount = ?, 
                    refuel_cost = ?
                WHERE id = ?
                """,
                (
                    datetime.isoformat(self.refuel_date),
                    self.current_mileage, 
                    self.refuel_amount,
                    self.refuel_cost,
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
                DELETE FROM fuel_refill_entries
                WHERE id = ? 
                """, 
                (self.id, )
            )
            self.connection.commit()
            self.__dict__.clear()
        else: 
            self.__dict__.clear()

