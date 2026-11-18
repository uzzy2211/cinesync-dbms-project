import logging

from fastapi import FastAPI, HTTPException
from mysql.connector import Error as MySQLError

from database import get_connection

logger = logging.getLogger(__name__)

app = FastAPI(title="CineSync API")


@app.get("/")
def api_status() -> dict[str, str]:
    return {"status": "CineSync API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        if cursor.fetchone() is None:
            raise RuntimeError("The database health query returned no result.")
    except (MySQLError, RuntimeError, ValueError) as error:
        logger.exception("Database health check failed.")
        raise HTTPException(
            status_code=503,
            detail="Database connectivity check failed.",
        ) from error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

    return {"status": "ok", "database": "connected"}