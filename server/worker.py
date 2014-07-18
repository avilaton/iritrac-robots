from server import engine
from sqlalchemy.orm import sessionmaker

from server.models import Driver
from server.models import Data
from server.services import Iritrack
from server.services import xlsParser

Session = sessionmaker(bind=engine)

iri = Iritrack()
iri.login('ruta2', 'DESAFIO')

headers = ['alpha', 'date', 'lat', 'lon', 'speed', 'altitude', 'event', 'zone']

def updateDrivers():
	vehicle = 'ACY'
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

if __name__ == '__main__':
	updateDrivers()
# sched.start()
