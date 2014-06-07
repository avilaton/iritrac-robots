#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import mktime
from datetime import *

from bottle import template, request
from server import app
from server.services import Iritrack

@app.route('/')
def index(db):
	return template('index.html')

@app.post('/')
def updateData():
	dateFrom = request.forms.get('from')
	dateTo = request.forms.get('to')
	print dateFrom, dateTo
	fecha_desde = dateFrom + ' 00:00'
	t = datetime.strptime(fecha_desde, '%Y-%m-%d %H:%M')
	t = t - timedelta(hours=3) #Convierto a UTC - 3
	timeunix = mktime(t.timetuple())
	print timeunix
	return template('index.html')
