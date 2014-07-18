import os
import xlrd
from bottle import template, request, redirect
from server import app
from server.models import StartTime
from server.services import xlsParser
from time import mktime
from datetime import *
@app.route('/starttimes')
def index(db):
	try:
		rows = db.query(StartTime).all()
	except:
		flag=1
	return template('starttimes.html', rows=rows)

@app.route('/starttimes', method='POST')
def set_start_time(db):
	name = request.forms.get('name')
	driver_id = request.forms.get('driver_id')
	db.add(Driver(driver_id=driver_id, name=name))
	redirect('/starttimes')

@app.route('/starttimes/upload', method='POST')
def do_upload(db):
	session=db
	upload = request.files.get('starttimes')
	#name, ext = os.path.splitext(upload.filename)
	headers = ['orden', 'driver_id', 'name', 'country', 'starttime']
	doc = xlsParser(upload.file.read(), headers=headers).toStartTime()

	db.query(StartTime).delete()
	sheet= doc.sheet_by_index(0)
	nrows = sheet.nrows
	book_datemode = doc.datemode
	timetmp = time(0,0,0) #Tiempo temporal, es para hacer la comparacion
	for i in range(nrows):
		id_driver = sheet.cell(i,0)
		id_group = sheet.cell(i,1)
		name_driver = sheet.cell(i,2)
		county_driver =  sheet.cell(i,3)
		time_driver = sheet.cell(i,4)
		year, month, day, hour, minute, second = xlrd.xldate_as_tuple(time_driver.value, book_datemode) #separo la fecha de la celda del excel
		timedr = timedelta(hours=hour,minutes=minute,seconds=second)
		if timedr == timetmp:
			timedr=timedelta(hours=hour,minutes=minute,seconds=30)
		timerun = StartTime(id = i,driver_group=int(id_group.value), name=name_driver.value,start_time= str(timedr))
		timetmp = timedr
		session.add(timerun)
		
	session.commit()
	redirect('/starttimes')