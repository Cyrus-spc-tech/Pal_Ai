import sqlite3
from pathlib import Path
from typing import List, Dict


DB_PATH = Path(__file__).parent / "dr_pal.db"


def get_db_connection():
   
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message_count INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()


def get_or_create_session(session_id: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sessions WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    if result:
        session_db_id = result["id"]
        # Update last_active
        cursor.execute(
            "UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE id = ?",
            (session_db_id,)
        )
    else:
        cursor.execute(
            "INSERT INTO sessions (session_id) VALUES (?)",
            (session_id,)
        )
        session_db_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_db_id


def save_message(session_id: str, role: str, content: str):  
    conn = get_db_connection()
    cursor = conn.cursor()
    session_db_id = get_or_create_session(session_id)
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    cursor.execute(
        "UPDATE sessions SET message_count = message_count + 1, last_active = CURRENT_TIMESTAMP WHERE id = ?",
        (session_db_id,)
    )
    conn.commit()
    conn.close()


def get_session_messages(session_id: str) -> List[Dict[str, str]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp",
        (session_id,)
    )
    messages = [{"role": row["role"], "content": row["content"]} for row in cursor.fetchall()]
    conn.close()
    return messages


def get_all_sessions() -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT session_id, created_at, last_active, message_count FROM sessions ORDER BY last_active DESC"
    )
    sessions = [
        {
            "session_id": row["session_id"],
            "created_at": row["created_at"],
            "last_active": row["last_active"],
            "message_count": row["message_count"]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return sessions


def clear_session(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute(
        "UPDATE sessions SET message_count = 0, last_active = CURRENT_TIMESTAMP WHERE session_id = ?",
        (session_id,)
    )
    conn.commit()
    conn.close()


def delete_session(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


# Initialize database on import
init_db()
