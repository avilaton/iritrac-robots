from bottle import template, request
from server import app
from server.models import Data


@app.route('/reports/')
def index(db):
  data = db.query(Data)
  print data.first()
  return ''
  # return template('data.tpl', alpha=driver_id, lista=rows)
