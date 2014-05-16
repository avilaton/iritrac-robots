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
    doc = xlrd.open_workbook(file_contents=xlsFileObject) #abro el .xls
    sheet = doc.sheet_by_index(0) #Genera el objeto
    
    tipos_datos = {0: 'TEXT',
                 1: 'TEXT',
                 2: 'REAL',
                 3: 'REAL',
                 4: 'INTEGER',
                }
   
    headers = []
    for i in range(sheet.ncols):
        name = sheet.cell_value(0,i)
        headers.append(str(name.split(' ')[0]))

    # extrae todas las filas
    rows = []
    for i in range(sheet.nrows-1):
        row = [sheet.cell_value(i+1,j) for j in range(8)] #El antes estaba len(header). El len header total es de 9, pero agrego 8 + 1 manual en la siguiente linea
        row = row
        rows.append(row)
    
    # convierte headers + rows en un array de diccionarios
    dictArray = []
    for row in rows:
        dictionary = {k:row[j] for j,k in enumerate(headers)}
        dictArray.append(dictionary)
        
    return dictArray

def createDb(filename):
    #Trata de crear la tabla y si ya está creada, sigue
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    try:
        cursor.execute (''' CREATE TABLE data
                (Alpha TEXT,
                DATE TEXT,
                LATITUD TEXT,
                LONG  TEXT,
                SPEED TEXT,
                ALTITUD TEXT,
                EVENT TEXT,
                ZONE TEXT,
                VEHICLE TEXT)''')
        print "Tabla creada"
        conn.commit()
    except:
        print "Tabla ya creada"

    return conn

def insertRows(rows, vehicle):
    headers = rows[0].keys()
    for r in rows:
        data = Data(date=r['Date'], lat=r['Latitude'], lon=r['Longitude'])
        data.alpha = r['Alpha']
        data.speed = r['Speed']
        data.altitude = r['Altitude']
        data.event = r['Event']
        data.zone = r['Zone']
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
    print "Buscando datos....."
    query = {'page':'positions.xl','name':'positions-1','vehicle':vehiculo,
    'date_from':fecha_desde,'date_to':fecha_hasta,'time_from':fecha_desde,'time_to':fecha_hasta}
    #vehicle = '603'
    #query = {'page':'positions.xl','name':'positions-1','vehicle': vehiculo,
    #   'date_from':1363910400,'date_to':1395532799,'time_from':1363910400,'time_to':1395532799}
    data = urllib.urlencode(query)
    excelResponse = opener.open('http://tracking.iritrack.com/index.php?'+data)
    #print excelResponse.info().getheader('Set-Cookie')
    try: 
        xls = excelResponse.read()
    except:
        print "No se pudo leer o generar el archivo."
    return xls

def Update(opener,corredor):
    for vehiculo in corredor:
        # query = "SELECT max(DATE) FROM data WHERE VEHICLE='%s'"%(vehiculo) #EN ESTE SELECT HAY QUE MODIFICARLO POR "SELECT max(DATE) from data WHERE 
        # cursor.execute(query)
        # ultima_fecha = cursor.fetchone()
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

def roll():
    opener = login()
    drivers =[1,2,3,4,5,7,8,9,10,11,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,31,33,34,35,36,37,38,39,40,41,42,43,44,45,101,102,103,104,105,106,107,109,110,111,112,114,115,116,117,118,119,120,123,124,125,126,127,301,302,303,304,305,306,307,308,309,310,311,312,313,314,316,319,321]
    flag= raw_input("Desea introducir una nueva fecha (s/n): ") #ACA SE PUEDE PONER QUE SI YA EXISTE UN BD Y QUE NO ESTE VACIA, DIRECTAMENTE HAGA UN UPDATE
    if flag == 's':
        #vehiculo = raw_input("Ingrese numero de vehiculo: ")
        fecha_desde = FechaDesde()
        fecha_hasta = FechaHasta()
        for vehiculo in drivers:
            print vehiculo
            xls = downloadXls(opener,fecha_desde,fecha_hasta,vehiculo)
            rows = parseXls(xls)
            insertRows(rows, vehiculo)
    else:
        Update(opener,drivers)

def test_parsing():
    vehiculo = 1
    fecha_desde = 1388534400.0 # FechaDesde()
    fecha_hasta = 1400198400.0 # FechaHasta()
    connection = login()
    xlsFileObject = downloadXls(connection, fecha_desde, fecha_hasta, vehiculo)
    rows = parseXls(xlsFileObject)
    insertRows(rows, vehiculo)

def test_query():
    result = session.query(func.max(Data.date)).filter_by(alpha='ALY')
    print result.first()[0]

def test_update():
    connection = login()
    Update(connection, [1])

if __name__ == '__main__':
    # roll()
    test_parsing()
    # test_query()
    test_update()