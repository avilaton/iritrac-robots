import sys
import atexit
from time import sleep
from apscheduler.scheduler import Scheduler
from server import engine
from sqlalchemy.orm import sessionmaker

from server.models import Driver
from server.models import Data
from server.services import Iritrack
from server.services import xlsParser

Session = sessionmaker(bind=engine)


sched = Scheduler(daemon=True)
# sched = Scheduler()
atexit.register(lambda: sched.shutdown(wait=False))

iri = Iritrack()
iri.login('ruta2', 'DESAFIO')

headers = ['alpha', 'date', 'lat', 'lon', 'speed', 'altitude', 'event', 'zone']

@sched.interval_schedule(seconds=30)
def updateDrivers():
	# for driver in session.query(Driver).all():
	#     updateDriver(connection, driver.driver_id)
	vehicle = '4'
	xlsFileObject = iri.getData(1388793600, 1401926399, vehicle)
	rows = xlsParser(xlsFileObject, headers=headers).toDictArray()
	db = Session()
	for r in rows:
		data = Data(date=r['date'], lat=r['lat'], lon=r['lon'])
		data.alpha = r['alpha']
		data.speed = r['speed']
		data.altitude = r['altitude']
		data.event = r['event']
		data.zone = r['zone']
		data.vehicle = vehicle
		db.add(data)
	db.close()
	# results = db.query(Driver).all()
	# for r in results:
	# 	print r
	# db.close()

# sched.start()
