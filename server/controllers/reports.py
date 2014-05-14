from bottle import template, request
from server import app
from server.models import Entity


@app.route('/reports/')
def index(db):
  entity = db.query(Entity)
  print entity.first()
  return ''
  # return template('data.tpl', alpha=driver_id, lista=rows)
