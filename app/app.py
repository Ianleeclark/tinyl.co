from ConfigParser import SafeConfigParser
from flask import Flask, request, redirect, render_template
from datetime import datetime
from .form import UrlForm
import sqlite3
import md5

app = Flask(__name__)
Config = SafeConfigParser()
Config.read("./config.ini")
app.config['SECRET_KEY'] = "test"

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

db = DatabaseHandler('/home/tinyl_server/tinyl.co/data.db')


def encode_link(link):
    """
    I'm meaning for this to be super duper simple:
    it's just the first 6 characters in the md5 hash of the link and the
    current time. In case of a collision, we'll encode one extra character from
    the full md5 into the encoded value.
    """
    to_encode = ''.join([str(link), str(datetime.now())])
    to_encode = str(md5.new(to_encode).hexdigest())
    return to_encode


def validate_url(url):
    for i in ['http://', 'https://', 'ftp://']:
        if url.startswith(i):
            return url
    return ''.join(['http://', url])


def add_new_link(link, max_len=6):
    # md5 the link + datetime
    fullenc = encode_link(link)
    enc = fullenc[0:max_len]

    # Insert the new url/enc/full into the db
    try:
        db.insert([link, enc, fullenc])
    except sqlite3.Error as e:
        print "Failed to execute Insert with {}: {}".format(link, e)

    return enc

@app.route('/<link>', methods=['GET', 'POST'])
def redir(link):
    if request.method == 'GET':
        target_url = db.query(link, 'enc')[0] # Returns the triple of url/enc/fullenc
        target_url = validate_url(target_url)
        if target_url:
            return redirect(target_url, code=302)
        return render_template('404.html')


@app.route('/add', methods=['GET', 'POST'])
def add_link():
    if request.method == 'POST':
        link = request.form['link']
        print link

        # Ensure no duplicate entries
        enc = db.query(link, 'url')
        if enc:
            if link != enc[0]:
                add_new_link(link, len(enc[1]) + 1)
            return render_template('index.html', href=enc[1], url=enc[0])

        enc = add_new_link(link)

        return render_template('index.html', href=enc[1], url=enc[0])
    else:
        return render_template('index.html')


@app.route('/')
def index():
    form = UrlForm()
    return render_template('index.html', form=form)
