import json
import oracledb

# --- CONFIGURATION ---
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_DSN = "localhost:1521/XEPDB1"  # hostname:port/service_name

JSON_FILE = "data.json"

# SQL parameterized statement
INSERT_SQL = """
    INSERT INTO EMPLOYEES (EMP_ID, FIRST_NAME, LAST_NAME, EMAIL, SALARY)
    VALUES (:1, :2, :3, :4, :5)
"""


def load_json_to_oracle():
    # 1. Read JSON file
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Convert dictionary objects to tuple lists for database insertion
    records = [
        (
            item.get("id"),
            item.get("first_name"),
            item.get("last_name"),
            item.get("email"),
            item.get("salary"),
        )
        for item in data
    ]

    # 3. Connect and bulk insert into Oracle
    connection = None
    try:
        connection = oracledb.connect(
            user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN
        )

        with connection.cursor() as cursor:
            # High-performance bulk insert
            cursor.executemany(INSERT_SQL, records)
            connection.commit()
            print(f"Successfully inserted {len(records)} records into Oracle.")

    except oracledb.Error as e:
        print(f"Database error: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    load_json_to_oracle()
