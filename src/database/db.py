import aiosqlite
from .models import create_tables
from config import settings

class Database:
    def __init__(self):
        self.conn = None

    async def init_db(self):
        self.conn = await aiosqlite.connect(settings.DB_NAME)
        await create_tables(self.conn)

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def add_ticket(self, user_id, user_name, question):
        if not self.conn:
            await self.init_db()
        cursor = await self.conn.execute(
            "INSERT INTO tickets (user_id, user_name, question) VALUES (?, ?, ?)",
            (user_id, user_name, question)
        )
        ticket_id = cursor.lastrowid
        await self.conn.commit()
        return ticket_id

    async def get_ticket(self, ticket_id):
        if not self.conn:
            await self.init_db()
        async with self.conn.execute(
            "SELECT * FROM tickets WHERE id = ?",
            (ticket_id,)
        ) as cursor:
            row = await cursor.fetchone()
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

    async def close_ticket(self, ticket_id, answer):
        if not self.conn:
            await self.init_db()
        await self.conn.execute(
            "UPDATE tickets SET answer = ?, status = 'closed' WHERE id = ?",
            (answer, ticket_id)
        )
        await self.conn.commit()

db = Database()