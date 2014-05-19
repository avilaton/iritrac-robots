from bottle import template, request
from server import app
from server.models import Data

@app.route('/reports/<driver_id>')
def index(db, driver_id):
  data = db.query(Data).all()
  return template('data.tpl', driver_id=driver_id, data=data)
