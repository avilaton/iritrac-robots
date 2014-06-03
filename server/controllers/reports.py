from bottle import template, request
from server import app
from server.models import Data
from server.models import Driver

@app.route('/reports/<driver_id>')
def index(db, driver_id):

  allDrivers = db.query(Driver).filter(Data.alpha == driver_id).all()
  for driver in allDrivers:
    db.query(Data)

  return template('data.tpl', driver_id=driver_id, data=data)


@app.route('/mariano')
def index(db):
  driver_id = "ALY"
  zonas = ["ASS5", "K201"]
  db.query(StartTime)
  results = db.query(Data).filter(Data.alpha == "ALY", Data.zone == "ASS5").one()
  for item in results:
    print item.date
  return results[0].date
  # return template('data.tpl', driver_id=driver_id, data=data)
