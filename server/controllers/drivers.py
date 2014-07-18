import os
from bottle import template, request, redirect
from server import app
from server.models import Driver
from server.services import xlsParser

@app.route('/drivers')
def index(db):
	try:
		rows = db.query(Driver).all()
	except:
		flag=1
	return template('drivers.html', drivers=rows)

@app.route('/drivers', method='POST')
def add_driver(db):
	name = request.forms.get('name')
	driver_id = request.forms.get('driver_id')
	db.add(Driver(driver_id=driver_id, name=name))
	redirect('/drivers')

@app.route('/drivers/upload', method='POST')
def do_upload(db):
	upload = request.files.get('drivers')
	name, ext = os.path.splitext(upload.filename)

	headers = ['orden', 'driver_id', 'name', 'country', 'starttime']
	dictArray = xlsParser(upload.file.read(), headers=headers).toDictArray()
	# Empty dable before loading drivers
	db.query(Driver).delete()
	drivers = []
	for item in dictArray:
		drivers.append(Driver(
			id=int(item['orden']),
			driver_id=int(item['driver_id']), 
			name=item['name'],
			country=item['country']))
	db.add_all(drivers)
	db.flush()
	redirect('/drivers')