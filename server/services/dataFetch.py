#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xlrd
import os
import urllib
import urllib2
import cookielib
import sqlite3
from time import mktime
from datetime import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from server import engine
from server.models import Data
from server.models import Driver
from server.services import xlsParser
from server.services import Iritrack
from server.models import StartTime
from server.models import Stage
Session = sessionmaker(bind=engine)
session = Session()

class dataFetch(object):
    """docstring for Parser"""

    def __init__(self, fecha_desde, fecha_hasta):
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta

    def parseXls(self,xlsFileObject):
        headers = ['alpha', 'date', 'lat', 'lon', 'speed', 'altitude', 'event', 'zone']
        rows = xlsParser(xlsFileObject, headers=headers).toDictArray()
        return rows

    def insertRows(self,rows, vehicle):
       
        #headers = rows[0].keys()
        for r in rows:
            data = Data(date=r['date'], lat=r['lat'], lon=r['lon'])
            data.alpha = r['alpha']
            print "#############3ELLL ALLPHAAA",data.alpha
            data.speed = r['speed']
            data.altitude = r['altitude']
            data.event = r['event']
            data.zone = r['zone']
            data.vehicle = vehicle
            session.add(data)
        session.commit()
        
    def login(self):
        COOKIEFILE = 'cookies.lwp'
        # cj = cookielib.CookieJar()
        # this cookie jar stores the login cookie to a file. Should be checked for existence, 
        # and validity and if it is not valid, ask the user to login again.
        cj = cookielib.LWPCookieJar(COOKIEFILE)
        if os.path.isfile(COOKIEFILE):
            cj.load()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        #username = raw_input("Please enter your username: ")
        #password = raw_input("Please enter your password: ")
        username = 'ruta2'
        password = 'DESAFIO'
        query = {'username': username,'password': password,'valid': 'OK'}
        data = urllib.urlencode(query) 
        response = opener.open('http://tracking.iritrack.com/index.php', data)
        html = response.read()
        cj.save()
        
        return opener

    def downloadXls(self,opener,fecha_desde,fecha_hasta,vehiculo):
        query = {'page':'positions.xl','name':'positions-1','vehicle':vehiculo,
        'date_from':fecha_desde,'date_to':fecha_hasta,'time_from':fecha_desde,'time_to':fecha_hasta}
        data = urllib.urlencode(query)
        excelResponse = opener.open('http://tracking.iritrack.com/index.php?'+data)
        try: 
            xls = excelResponse.read()
        except:
            print "No se pudo leer o generar el archivo."
        return xls



    def firstFetch(self):
        
        connection = self.login()
        fecha_desde = self.fecha_desde
        fecha_hasta = self.fecha_hasta
        session.query(Data).delete()
        
        for driver in session.query(Driver).all():
            try:
                print "Corredor: ",driver.driver_id
                xls = self.downloadXls(connection,fecha_desde,fecha_hasta, driver.driver_id)
                rows = self.parseXls(xls)
                print "######################",rows
                self.insertRows(rows, driver.driver_id)
            except:
                print "Corredor: ",driver.driver_id, "no esta en la pagina"


    def updateAll(self):
        connection = self.login()
        for driver in session.query(Driver).all():
            self.updateDriver(connection, driver.driver_id)


    def updateDriver(self,opener, driver_id):
        vehiculo = driver_id
        ultima_fecha = session.query(func.max(Data.date)).filter_by(vehicle=vehiculo).first()
        print vehiculo, ultima_fecha
        if ultima_fecha[0] is not None:
            fecha_desde = datetime.strptime(ultima_fecha[0], '%Y-%m-%d %H:%M:%S')
            fecha_desde = fecha_desde - timedelta(hours=3)
            fecha_desde = fecha_desde + timedelta(seconds=1) #LE SUMO UN SEGUNDO PARA QUE BUSQUE UN SEGUNDO DPS DEL ULTIMO DATO
            fecha_hasta = fecha_desde + timedelta(hours=5)
            fecha_desde_unix = mktime(fecha_desde.timetuple())
            fecha_hasta_unix = mktime(fecha_hasta.timetuple())
            try:
                xlsFileObject = self.downloadXls(opener,fecha_desde_unix,fecha_hasta_unix,vehiculo)
                rows = self.parseXls(xlsFileObject)
                self.insertRows(rows, vehiculo)
            except:
                print "No se registraron nuevos datos"
        else:
            print "Base de datos vacia"
            fechas = []
            fechas=self.FechaUpdate() #Si no tiene nada en la BD, busca en internet con la fecha de hoy desde las 0 hs hasta la hora actual
            
            fecha_desde_unix= fechas[0]
            fecha_hasta_unix=fechas[1]
            try:
                xlsFileObject = self.downloadXls(opener,fecha_desde_unix,fecha_hasta_unix,vehiculo)
                rows = self.parseXls(xlsFileObject)
                self.insertRows(rows, vehiculo)
            except:
                print "No se encotro informacion"

    def FechaUpdate(self):
        newfecha = []
        current_date = date.today() #Fecha de hoy
        current_date=str(current_date) #convierto en string
        inicial_date = current_date + ' 00:00:00' #Le agrego la hora 00
        inicial_date = datetime.strptime(inicial_date,'%Y-%m-%d %H:%M:%S') #Convierto formato Fecha
        timeunix1 = mktime(inicial_date.timetuple()) #convierto formato Unix
        newfecha.append(timeunix1)
        
        fecha =datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Fecha y hora actual
        fecha = datetime.strptime(fecha,'%Y-%m-%d %H:%M:%S')
        timeunix2 = mktime(fecha.timetuple())
        newfecha.append(timeunix2)
        return newfecha

        
            

