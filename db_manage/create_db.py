import sqlite3

db_name = "data.db"
schema = "links.sql"

with sqlite3.connect(db_name) as conn:
    with open(schema, 'rt') as f:
        schema = f.read()
    conn.executescript(schema)

    conn.execute("""INSERT INTO links (url, enc, full, hits) VALUES 
    ('http://google.com', '1', '1', 0)""")

    conn.execute("""INSERT INTO links (url, enc, full, hits) VALUES 
    ('http://facebook.com', '2', '2', 0)""")

