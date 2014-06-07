import os
from bottle import template, request, redirect
from server import app
from server.models import Data
from server.models import Driver
from server.services import xlsParser

@app.route('/drivers')
def index(db):
	rows = db.query(Driver).all()
	return template('drivers.html', drivers=rows)

@app.route('/drivers', method='POST')
def add_driver(db):
	name = request.forms.get('name')
	driver_id = request.forms.get('driver_id')
	db.add(Driver(driver_id=driver_id, name=name))
	redirect('/drivers')
