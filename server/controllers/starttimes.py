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
		rows = db.query(StartTime).filter(StartTime.stage_id==1).all()
		count = db.query(StartTime.stage_id).distinct().count()
	except:
		pass
	return template('starttimes.html', rows=rows, stage=1, count=count,flagFile=True)

@app.route('/starttimes', method='POST')
def set_start_time(db):
	name = request.forms.get('name')
	driver_id = request.forms.get('driver_id')
	db.add(Driver(driver_id=driver_id, name=name))
	redirect('/starttimes')

@app.route('/starttimes/upload', method='POST')
def do_upload(db):
	addtime = request.forms.get('addtime')
	stage_id = request.forms.get('stage_id')
	session=db
	upload = request.files.get('starttimes')
	try:

		headers = ['orden', 'driver_id', 'name', 'country', 'starttime']
		doc = xlsParser(upload.file.read(), headers=headers).toStartTime()
		try:
			db.query(StartTime).filter(StartTime.stage_id==stage_id).delete()
		except:
			flag = 0
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
			minute = minute + int(addtime)
			timedr = timedelta(hours=hour,minutes=minute ,seconds=second)
			#timedr = timedr + timedelta(minutes=int(addtime))
			if timedr == timetmp:
				timedr=timedelta(hours=hour,minutes=minute,seconds=30)

			timerun = StartTime(id = i,driver_group=int(id_group.value), name=name_driver.value,start_time= str(timedr),stage_id=str(stage_id))
			timetmp = timedr
			session.add(timerun)
			
		session.commit()
		
		
	except:
		
		return template('starttimes.html', rows="", stage=1, count="",flagFile=False)

	redirect('/starttimes')
	# rows = db.query(StartTime).filter(StartTime.stage_id==stage_id).all()
	# count = db.query(StartTime.stage_id).distinct().count()
	# return template('starttimes.html', rows=rows, stage=stage_id,count=count)
	
@app.route('/starttimes/show', method='POST')
def do_show(db):
	stage_id = request.forms.get('stage')
	try:
		rows = db.query(StartTime).filter(StartTime.stage_id==stage_id).all()
		count = db.query(StartTime.stage_id).distinct().count()
	except:
		flag=1
	return template('starttimes.html', rows=rows, stage=stage_id,count=count,flagFile=True)

@app.route('/starttimes/editar/<stage>/<driver_id>')
def edit_driver(db,stage,driver_id):
	start_times = db.query(StartTime).filter(StartTime.driver_group==driver_id,StartTime.stage_id==stage).first() #busco el start time del alpha indicado
	return template('editar.html', drivers = start_times)

@app.route('/starttimes/update', method='POST')
def update_edit_driver(db):
	driver_id = request.forms.get('driverid')
	name = request.forms.get('name')
	startime = request.forms.get('startime')
	stage = request.forms.get('stage')
	#update(StartTime).where(StartTime.driver_id == driver_id).values(driver_id=driver_id,start_time=startime,name=name)
	db.query(StartTime).filter(StartTime.driver_group == driver_id,StartTime.stage_id == stage).update({'driver_group':driver_id,'start_time':startime,'name':name,'stage_id':stage})
	db.commit()
	redirect('/starttimes')
	

@app.route('/starttimes/deletall')
def deleteall(db):
	db.query(StartTime).delete()

	redirect('/starttimes')
	
