

import sqlite3
from bottle import route, run, template

class Database(object):
	"""docstring for db"""
	def __init__(self, filename):
		self.filename = filename
		self.connection = sqlite3.connect(filename)
		self.connection.row_factory = sqlite3.Row
		self.cursor = self.connection.cursor()


db = Database('../tabla.sqlite')

@route('/times/<name>')
def index(name):
	db.cursor.execute("SELECT * FROM data WHERE Alpha=?",(name,))
	lista = []
	for r in db.cursor.fetchall():
		lista.append(dict(r))

	return template('data.tpl', alpha=name, lista=lista)

@route('/vehicles/')
def vehicles():
	return 'Create this page'

if __name__ == '__main__':
	run(host='localhost', port=8000, debug=True, reloader=True)