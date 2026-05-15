
import sqlite3

conn = sqlite3.connect(
    "legal_edit_memory.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS edits (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    original_text TEXT,

    edited_text TEXT,

    edit_summary TEXT,

    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

def save_edit(
    original_text,
    edited_text,
    edit_summary
):

    cursor.execute(
        """
        INSERT INTO edits (
            original_text,
            edited_text,
            edit_summary
        )
        VALUES (?, ?, ?)
        """,
        (
            original_text,
            edited_text,
            edit_summary
        )
    )

    conn.commit()

def get_all_edits():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            original_text,
            edited_text,
            edit_summary,
            timestamp
        FROM edits
    """)

    rows = cursor.fetchall()

    conn.close()

    edits = []

    for row in rows:

        edits.append({

            "id": row[0],

            "original_text": row[1],

            "edited_text": row[2],

            "edit_summary": row[3],

            "timestamp": row[4]
        })

    return edits
