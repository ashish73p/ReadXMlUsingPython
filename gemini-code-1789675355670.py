import xml.etree.ElementTree as ET
import oracledb

# --- DATABASE CONFIGURATION ---
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_DSN = "localhost:1521/XEPDB1"  # Replace with hostname:port/service_name

# --- XML FILE CONFIGURATION ---
XML_FILE = "employees.xml"

# --- SQL QUERY ---
# Assuming table target: EMPLOYEES (EMP_ID, FIRST_NAME, LAST_NAME, EMAIL)
INSERT_SQL = """
    INSERT INTO EMPLOYEES (EMP_ID, FIRST_NAME, LAST_NAME, EMAIL)
    VALUES (:1, :2, :3, :4)
"""


def parse_xml_data(file_path):
    """Parses the XML file and extracts records into a list of tuples."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    records = []
    # Adjust 'employee' tag to match your XML structure
    for emp in root.findall("employee"):
        emp_id = emp.findtext("id")
        first_name = emp.findtext("first_name")
        last_name = emp.findtext("last_name")
        email = emp.findtext("email")

        records.append((int(emp_id), first_name, last_name, email))

    return records


def load_to_oracle(records):
    """Inserts records into Oracle SQL using batch insertion."""
    connection = None
    try:
        # Establish connection
        connection = oracledb.connect(
            user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN
        )

        with connection.cursor() as cursor:
            # executemany performs high-performance bulk insertion
            cursor.executemany(INSERT_SQL, records)
            connection.commit()
            print(f"Successfully inserted {len(records)} rows into Oracle.")

    except oracledb.Error as e:
        print(f"Database error occurred: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    # 1. Parse XML
    data_to_insert = parse_xml_data(XML_FILE)

    # 2. Load into Oracle SQL
    if data_to_insert:
        load_to_oracle(data_to_insert)
    else:
        print("No records found in the XML file.")