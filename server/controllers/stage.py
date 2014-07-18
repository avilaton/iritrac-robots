import os
from bottle import template, request, redirect
from server import app
from server.models import Stage


@app.route('/stage')
def index(db):
	try:
		zones = db.query(Stage).all()
	except:
		flag=1
	return template('stage.html', zones=zones)

@app.route('/stage', method='POST')
def add_stage(db):
	stage_id = request.forms.get('stage_id')
	zone = request.forms.get('zone')
	db.add(Stage(stage_id=stage_id, zone=zone))
	redirect('/stage')