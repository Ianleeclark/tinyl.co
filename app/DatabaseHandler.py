import sqlite3

class DatabaseHandler:
    """
    """
    def __init__(self, db):
        self.db = db
        self.opened = False
        self.open_conn()

    def open_conn(self):
        try:
            self.conn = sqlite3.connect(self.db)
        except sqlite3.Error as e:
            print "Failed to open db: {} with error {}".format(self.db, e)

        if self.conn:
            self.opened = True
            return True
        else:
            self.opened = False
            return False

    def close_conn(self):
        self.conn.close()
        self.opened = False
        #TODO(ian): Error handling?

    def refresh_conn(self):
        if self.opened:
            #TODO(ian): try for self-made errors here to ensure connections refresh
            self.close_conn()
            self.open_conn()
        else:
            self.open_conn()

    def insert(self, values):
        if len(values) != 3:
            return None
            print values

        print [str(values[0]), values[1], values[2]]

        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO links (url, enc, fullenc) VALUES (?,?,?);', [values[0], values[1], values[2]])
            self.conn.commit()
            print cursor.fetchone()
        except sqlite3.Error as e:
            print "Failed to retrieve url: {} -- Error: {}".format(link, e)
            return None

        cursor.close()

    def query(self, value, to_find='url'):
        try:
            cursor = self.conn.cursor()
            if to_find == "url":
                cursor.execute('SELECT * FROM links WHERE url=?;', [value])#, [to_find, where, str(value)])
            else:
                cursor.execute('SELECT * FROM links WHERE enc=?;', [value])
            data = cursor.fetchone()
        except sqlite3.Error as e:
            print "Failed to retrieve url: {} -- Error: {}".format(link, e)
            return None

        cursor.close()

        if data:
            return data
        return None

