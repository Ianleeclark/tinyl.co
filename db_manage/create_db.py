import sqlite3

db_name = "data.db"
schema = "links.sql"

with sqlite3.connect(db_name) as conn:
    with open(schema, 'rt') as f:
        schema = f.read()
    conn.executescript(schema)
