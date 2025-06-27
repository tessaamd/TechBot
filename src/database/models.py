from aiosqlite import Connection

async def create_tables(conn: Connection) -> None:
    await conn.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT,
        status TEXT DEFAULT 'open'
    )''')