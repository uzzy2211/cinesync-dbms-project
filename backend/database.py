import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from mysql.connector.connection import MySQLConnection

load_dotenv(Path(__file__).resolve().with_name(".env"))


def get_connection() -> MySQLConnection:
    """Create a fresh connection for one operation; callers must close it."""
    password = os.getenv("DB_PASSWORD")
    if password is None:
        raise RuntimeError(
            "DB_PASSWORD is not set. Add it to the backend .env file."
        )

    raw_port = os.getenv("DB_PORT", "3306")
    try:
        port = int(raw_port)
    except ValueError as error:
        raise ValueError("DB_PORT must be an integer.") from error

    if not 1 <= port <= 65535:
        raise ValueError("DB_PORT must be between 1 and 65535.")

    # Do not share a connection between requests; each operation owns its connection.
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=port,
        user=os.getenv("DB_USER", "root"),
        password=password,
        database=os.getenv("DB_NAME", "cinesync_db"),
        connection_timeout=5,
    )