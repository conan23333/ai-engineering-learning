import sqlite3
import os

DB_PATH = os.getenv("DB_PATH","analysis.db")
def get_connection():
    return sqlite3.connect(DB_PATH)
def init_db():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_file TEXT NOT NULL,
            model TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()
def save_analysis(
    report_file: str,
    model: str,
    content: str,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_records (
            report_file,
            model,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            report_file,
            model,
            content,
        ),
    )

    connection.commit()
    connection.close()

def get_analysis_records(limit: int ):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            report_file,
            model,
            content,
            created_at
        FROM analysis_records
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]

def get_analysis_by_id(record_id: int):
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            report_file,
            model,
            content,
            created_at
        FROM analysis_records
        WHERE id = ?
        """,
        (record_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)

def del_analysis_by_id(record_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM analysis_records
        WHERE id = ?
        """,
        (record_id,),
    )
    deleted = cursor.rowcount>0

    connection.commit()
    connection.close()

    return deleted