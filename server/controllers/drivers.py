import os
from bottle import template, request
from server import app
from server.models import Data
from server.services import xlsParser

@app.route('/data/<driver_id>')
def index(driver_id):
  rows = Data.getRowsByDriverId(driver_id)
  return template('data.tpl', alpha=driver_id, lista=rows)

@app.route('/data', method='POST')
def do_upload():
  upload = request.files.get('drivers')
  name, ext = os.path.splitext(upload.filename)
  # if ext not in ('.png','.jpg','.jpeg'):
  #   return 'File extension not allowed.'
  
  dictArray = xlsParser(upload.file.read()).toDictArray()
  return 'OK'
