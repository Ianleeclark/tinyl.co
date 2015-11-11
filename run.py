from app.app import app
from flask.ext.script import Manager, Server

manager = Manager(app)
manager.add_command('runserver', Server(
	host='0.0.0.0',
	port='80'
    )
)

manager.run()
