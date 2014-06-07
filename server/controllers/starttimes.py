from bottle import template, request, redirect
from server import app
from server.models import StartTime

@app.route('/starttimes')
def index(db):
	rows = db.query(StartTime).all()
	return template('starttimes.html', rows=rows)

@app.route('/starttimes', method='POST')
def set_start_time(db):
	name = request.forms.get('name')
	driver_id = request.forms.get('driver_id')
	db.add(Driver(driver_id=driver_id, name=name))
	redirect('/starttimes')
