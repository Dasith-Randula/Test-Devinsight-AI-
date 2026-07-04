# database_utils.py - Database utilities with errors

import sqlite3

def connect_db():
    # ERROR: variable 'conn' not defined
    return conn

def query_db(query):
    # ERROR: variable 'cursor' not defined
    cursor.execute(query)
    return cursor.fetchall()

def main():
    # ERROR: undefined variable 'db_path'
    conn = connect_db(db_path)
    print(conn)

if __name__ == "__main__":
    main()