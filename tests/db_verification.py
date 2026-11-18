import sys
from pathlib import Path

from mysql.connector import Error as MySQLError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import get_connection


def main() -> int:
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        row = cursor.fetchone()
        expected_database = "cinesync_db"

        if row is None or row[0] != expected_database:
            raise RuntimeError(
                f"Connected database is not {expected_database!r}."
            )

        print(f"Connected to MySQL database {expected_database}.")
        return 0
    except (MySQLError, RuntimeError, ValueError) as error:
        print(f"Database verification failed: {error}", file=sys.stderr)
        return 1
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
