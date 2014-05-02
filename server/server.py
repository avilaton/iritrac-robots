
import os
import sqlite3
from bottle import route, run, template, post, request

class Database(object):
	"""docstring for db"""
	def __init__(self, filename):
		self.filename = filename
		self.connection = sqlite3.connect(filename)
		self.connection.row_factory = sqlite3.Row
		self.cursor = self.connection.cursor()


db = Database('./tabla.sqlite')

@route('/times/<name>')
def index(name):
	db.cursor.execute("SELECT * FROM data WHERE Alpha=?",(name,))
	lista = []
	for r in db.cursor.fetchall():
		lista.append(dict(r))

	return template('data.tpl', alpha=name, lista=lista)

@route('/vehicles/', method='GET')
def vehicles():
	vehicles = range(1,100)
	return template('vehicles.tpl', vehicles=vehicles)

@route('/vehicles', method='POST')
def do_upload():
	upload     = request.files.get('file')
	name, ext = os.path.splitext(upload.filename)
	# if ext not in ('.png','.jpg','.jpeg'):
	# 	return 'File extension not allowed.'

	upload.save('uploads') # appends upload.filename automatically
	return 'OK'

if __name__ == '__main__':
	run(host='localhost', port=8000, debug=True, reloader=True)