import sqlite3
from .models import create_tables
from config import settings

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(settings.DB_NAME)
        create_tables(self.conn)
    
    def add_ticket(self, user_id: int, user_name: str, question: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tickets (user_id, user_name, question) VALUES (?, ?, ?)",
            (user_id, user_name, question)
        )
        ticket_id = cursor.lastrowid
        self.conn.commit()
        return ticket_id
    
    def close_ticket(self, ticket_id: int, answer: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tickets SET answer=?, status='closed' WHERE id=?",
            (answer, ticket_id)
        )
        self.conn.commit()
    
    def get_ticket(self, ticket_id: int):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
        return cursor.fetchone()
    
    def __del__(self):
        self.conn.close()
        
db = Database()