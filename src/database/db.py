import sqlite3
from .models import create_tables
from config import settings

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(settings.DB_NAME)
        create_tables(self.conn)
        self.cursor = self.conn.cursor()

    def add_ticket(self, user_id, user_name, question):
        self.cursor.execute(
            "INSERT INTO tickets (user_id, user_name, question) VALUES (?, ?, ?)",
            (user_id, user_name, question)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_ticket(self, ticket_id):
        self.cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'user_id': row[1],
                'user_name': row[2],
                'question': row[3],
                'answer': row[4],
                'status': row[5]
            }
        return None

    def close_ticket(self, ticket_id, answer):
        self.cursor.execute(
            "UPDATE tickets SET answer = ?, status = 'closed' WHERE id = ?",
            (answer, ticket_id)
        )
        self.conn.commit()

db = Database()