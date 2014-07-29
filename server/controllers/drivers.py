import os
from bottle import template, request, redirect
from server import app
from server.models import Driver
from server.services import xlsParser

@app.route('/drivers')
def index(db):
	try:
		rows = db.query(Driver).filter(Driver.stage_id==1).all()
	except:
		flag=1
	return template('drivers.html', drivers=rows,stage_id=1)

@app.route('/drivers', method='POST')
def add_driver(db):
	name = request.forms.get('name')
	driver_id = request.forms.get('driver_id')
	db.add(Driver(driver_id=driver_id, name=name))
	rows = db.query(Driver).filter(Driver.stage_id==1).all()
	return template('drivers.html', drivers=rows, stage_id=stage_id)

@app.route('/drivers/upload', method='POST')
def do_upload(db):
	upload = request.files.get('drivers')
	stage_id =request.forms.get('stage_id')
	
	name, ext = os.path.splitext(upload.filename)

	headers = ['orden', 'driver_id', 'name', 'country', 'starttime']
	dictArray = xlsParser(upload.file.read(), headers=headers).toDictArray()
	# Empty dable before loading drivers
	try:
		db.query(Driver).filter(Driver.stage_id==stage_id).delete()
	except:
		flag = 0
	drivers = []
	for item in dictArray:
		drivers.append(Driver(id=int(item['orden']),driver_id=int(item['driver_id']),name=item['name'],	country=item['country'],stage_id=stage_id))
	db.add_all(drivers)
	db.flush()
	rows = db.query(Driver).filter(Driver.stage_id==stage_id).all()
	return template('drivers.html', drivers=rows, stage_id=stage_id)