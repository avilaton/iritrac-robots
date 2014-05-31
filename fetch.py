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
from server.models import StartTime

Session = sessionmaker(bind=engine)
session = Session()

def FechaDesde():
    dia_desde = raw_input("Dia Desde en ""dd"": ")
    mes_desde = raw_input("Mes Desde en ""MM"": ")
    ano_desde = raw_input("Ano Desde en ""YYYY"": ")
    hora_desde = raw_input("Hora Desde en ""HH"": ")
    minuto_desde = raw_input("Minuto Desde en ""mm"": ")
    #dia_inicial='05'
    #mes_inicial='04'
    #ano_inicial='2014'
    #minuto_inicial='00'
    fecha_desde = dia_desde + '/' + mes_desde + '/' + ano_desde + " " + hora_desde + ':' + minuto_desde
    t = datetime.strptime(fecha_desde, '%d/%m/%Y %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    timeunix = mktime(t.timetuple())
    return timeunix

def FechaHasta():
    dia_hasta = raw_input("Dia Hasta en ""dd"": ")
    mes_hasta = raw_input("Mes Hasta en ""MM"": ")
    ano_hasta = raw_input("Ano Hasta en ""YYYY"": ")
    hora_hasta = raw_input("Hora Hasta en ""HH"": ")
    minuto_hasta = raw_input("Minuto Hasta ""mm"": ")
    #dia_final='05'
    #mes_final='04'
    #ano_final='2014'
    #minuto_final='00'
    fecha_hasta = dia_hasta+ '/' + mes_hasta + '/' + ano_hasta + " " + hora_hasta + ':' + minuto_hasta
    t = datetime.strptime(fecha_hasta, '%d/%m/%Y %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    timeunix = mktime(t.timetuple())
    return timeunix

def FechaUpdate():
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
    
def parseXls(xlsFileObject):
    headers = ['alpha', 'date', 'lat', 'lon', 'speed', 'altitude', 'event', 'zone']
    rows = xlsParser(xlsFileObject, headers=headers).toDictArray()
    return rows

def insertRows(rows, vehicle):
    headers = rows[0].keys()
    for r in rows:
        data = Data(date=r['date'], lat=r['lat'], lon=r['lon'])
        data.alpha = r['alpha']
        data.speed = r['speed']
        data.altitude = r['altitude']
        data.event = r['event']
        data.zone = r['zone']
        data.vehicle = vehicle
        session.add(data)
    session.commit()
    
def login():
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

def downloadXls(opener,fecha_desde,fecha_hasta,vehiculo):
    query = {'page':'positions.xl','name':'positions-1','vehicle':vehiculo,
    'date_from':fecha_desde,'date_to':fecha_hasta,'time_from':fecha_desde,'time_to':fecha_hasta}
    data = urllib.urlencode(query)
    excelResponse = opener.open('http://tracking.iritrack.com/index.php?'+data)
    try: 
        xls = excelResponse.read()
    except:
        print "No se pudo leer o generar el archivo."
    return xls

def updateDriver(opener, driver_id):
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
            xlsFileObject = downloadXls(opener,fecha_desde_unix,fecha_hasta_unix,vehiculo)
            rows = parseXls(xlsFileObject)
            insertRows(rows, vehiculo)
        except:
            print "No se registraron nuevos datos"
    else:
        print "Base de datos vacia"
        fechas = []
        fechas=FechaUpdate() #Si no tiene nada en la BD, busca en internet con la fecha de hoy desde las 0 hs hasta la hora actual
        
        fecha_desde_unix= fechas[0]
        fecha_hasta_unix=fechas[1]
        try:
            xlsFileObject = downloadXls(opener,fecha_desde_unix,fecha_hasta_unix,vehiculo)
            rows = parseXls(xlsFileObject)
            insertRows(rows, vehiculo)
        except:
            print "No se encotro informacion"

def firstFetch():
    connection = login()
    fecha_desde = FechaDesde()
    fecha_hasta = FechaHasta()
    for driver in session.query(Driver).all():
        xls = downloadXls(connection,fecha_desde,fecha_hasta, driver.driver_id)
        rows = parseXls(xls)
        insertRows(rows, driver.driver_id)

def updateAll():
    connection = login()
    for driver in session.query(Driver).all():
        updateDriver(connection, driver.driver_id)

def createDrivers():
    #drivers = [1,2,3,4,5,7,8,9,10,11,14,15,16,17,18,19,20,21,22,23,24,26,
        #27,28,29,31,33,34,35,36,37,38,39,40,41,42,43,44,45,101,102,103,104,
        #105,106,107,109,110,111,112,114,115,116,117,118,119,120,123,124,125,
        #126,127,301,302,303,304,305,306,307,308,309,310,311,312,313,314,316,319,321]
    doc = xlrd.open_workbook("largada.xlsx") #abro el .xls
    sheet = doc.sheet_by_index(0) #Selecciono la hoja uno

    ncols = sheet.ncols
    nrows = sheet.nrows

    for i in range(nrows):
        id_corr = sheet.cell(i,0)
        group = sheet.cell (i,1)
        name = sheet.cell (i,2)
        country = sheet.cell (i,3)
        timecell = sheet.cell (i,4)
        #print id_corr.value, " ", grupo.value, " ", nombre.value," ", pais.value, " ", tiempo.value
        driver = Driver(id=int(id_corr.value), driver_id=int(group.value), name=name.value)
        session.merge(driver)
    session.commit()

def time_of_drivers():
    doc = xlrd.open_workbook("largada.xlsx") #abro el .xls
    sheet = doc.sheet_by_index(0) #Selecciono la hoja uno

    ncols = sheet.ncols
    nrows = sheet.nrows

    book_datemode = doc.datemode
    timetmp = time(0,0,0) #Tiempo temporal, es para hacer la comparacion
    for i in range(nrows):
        id_corr = sheet.cell(i,0)
        group = sheet.cell (i,1)
        name = sheet.cell (i,2)
        timecell = sheet.cell (i,4)

        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(timecell.value, book_datemode) #separo la fecha de la celda del excel
        
        #timedr = time(hour, minute, second) 
        timedr = timedelta(hours=hour,minutes=minute,seconds=second)
        
        if timedr == timetmp:
            #timedr = timedr + timedelta(seconds=30) no se xq no funciona, asi que hice la chanchada de abajo
            timedr = timedelta(hours=hour,minutes=minute,seconds=30) #si hay dos tiempos iguales, sumo 30 seg al segundo
        
        timerun = StartTime(id = int(id_corr.value),name=name.value,start_time= str(timedr))
        timetmp = timedr #Actualizo el temportal
        try:
            session.add(timerun) #si no existe lo agrega
        except:
            session.merge(timerun) #si salta error es porque existe, entonces le hace un merge

    session.commit()
def test_parsing():
    vehiculo = 1
    fecha_desde = 1388534400.0 # FechaDesde()
    fecha_hasta = 1400198400.0 # FechaHasta()
    connection = login()
    xlsFileObject = downloadXls(connection, fecha_desde, fecha_hasta, vehiculo)
    headers = ['alpha', 'date', 'lat', 'lon', 'speed', 'altitude', 'event', 'zone']
    rows = xlsParser(xlsFileObject, headers=headers).toDictArray()
    insertRows(rows, vehiculo)

def test_query():
    connection = login()
    xls = downloadXls(connection, 1363910400, 1395532799, '603')
    print xls
if __name__ == '__main__':
    #flag= raw_input("Desea introducir una nueva fecha (s/n): ") #ACA SE PUEDE PONER QUE SI YA EXISTE UN BD Y QUE NO ESTE VACIA, DIRECTAMENTE HAGA UN UPDATE
    #if flag == 's':
    #firstFetch()
    #else:
        #updateAll()
    createDrivers()    
    time_of_drivers()
    #test_parsing()
    #test_query()
