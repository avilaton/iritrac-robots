#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import mktime
from datetime import *
import cookielib
import os
import urllib
import urllib2
import sys
from bottle import template, request, redirect
from server import app
from server.models import Driver
from server.services import Iritrack
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from server import engine
from server.services import dataFetch
Session = sessionmaker(bind=engine)
session = Session()



@app.route('/')
def index(db):
	return template('index.html')

@app.post('/')
def updateData():
	dateFrom = request.forms.get('from')
	dateTo = request.forms.get('to')
	
	fecha_desde = dateFrom + ' 00:00'
	t = datetime.strptime(fecha_desde, '%Y-%m-%d %H:%M')
	t = t - timedelta(hours=3) #Convierto a UTC - 3
	fecha_desde = mktime(t.timetuple())
	print "############### inicio",fecha_desde
	time_now = datetime.now().strftime("%H:%M")
	fecha_hasta = dateTo + " " + time_now
	t = datetime.strptime(fecha_hasta, '%Y-%m-%d %H:%M')
	t = t - timedelta(hours=3) #Convierto a UTC - 3
	fecha_hasta = mktime(t.timetuple())
	print "############### finnn",fecha_hasta
	dataFetch(fecha_desde,fecha_hasta).firstFetch()
	return template('index.html')

@app.post('/update')
def updateDataDriver():
	dataFetch("q","e").updateAll()
	return template('index.html')