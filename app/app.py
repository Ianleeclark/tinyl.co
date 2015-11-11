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

conn = sqlite3.connect('data.db')


def lookup_encoded(link):
    cursor = conn.cursor()
    cursor.execute('select url from links where enc={}'.format(str(link)))
    data = cursor.fetchone()
    return str(data[0])


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


@app.route('/<link>', methods=['GET', 'POST'])
def redir(link):
    if request.method == 'GET':
        target_url = lookup_encoded(link)
        return redirect(target_url, code=302)
    return '404 Niet Gevonden'


@app.route('/add/', methods=['GET', 'POST'])
def add_link():
    link = request.form['link']
    if request.method == 'POST':
        fullenc = encode_link(link)
        enc = fullenc[0:6]
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO links(url, enc, full) VALUES (?, ?,?);', (link, enc, fullenc))
        except sqlite3.Error as e:
            print "Failed to execute Insert with {}: {}".format(link, e)

        return render_template('index.html', href=enc)
    else:
        return redirect('/')


@app.route('/')
def index():
    form = UrlForm()
    return render_template('index.html', form=form)
