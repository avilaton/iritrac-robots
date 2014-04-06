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
      
def parseXls(filename):

    doc = xlrd.open_workbook(filename) #abro el .xls
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
        row = [sheet.cell_value(i+1,j) for j in range(len(headers))]
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
                ZONE TEXT)''')
        print "Tabla creada"
        conn.commit()
    except:
        print "Tabla ya creada"

    return conn

def insertRows(db, rows):
    
    cursor = db.cursor()
    try:
        headers = rows[0].keys()
        print "Almacenando datos....."
        for row in rows:
            insert_query = """INSERT INTO data 
                VALUES ('{Alpha}',
                    '{Date}',
                    '{Latitude}',
                    '{Longitude}',
                    '{Speed}',
                    '{Altitude}',
                    '{Event}',
                    '{Zone}')""".format(**row)
            cursor.execute(insert_query)

        db.commit()
        print "Datos guardados en BD"
    except:
        print "No se encotro informacion"
    
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
        with open('data'+vehiculo+'.xls','wb') as f:
            f.write(xls)   
    except:
        print "No se pudo leer o generar el archivo."
        #exit()
def Update(db,opener):
    vehiculo = raw_input("Ingrese numero de vehiculo: ")
    cursor = db.cursor()
    query = "SELECT max(DATE) from data" #EN ESTE SELECT HAY QUE MODIFICARLO POR "SELECT max(DATE) from data WHERE 
    cursor.execute(query)
    ultima_fecha = cursor.fetchone()
    if ultima_fecha[0] is not None:
        fecha_desde = datetime.strptime(ultima_fecha[0], '%Y-%m-%d %H:%M:%S')
        fecha_desde = fecha_desde - timedelta(hours=3)
        fecha_desde = fecha_desde + timedelta(seconds=1) #LE SUMO UN SEGUNDO PARA QUE BUSQUE UN SEGUNDO DPS DEL ULTIMO DATO
        fecha_hasta = fecha_desde + timedelta(hours=1)
        fecha_desde_unix = mktime(fecha_desde.timetuple())
        fecha_hasta_unix = mktime(fecha_hasta.timetuple())
        try:
            downloadXls(opener,fecha_desde_unix,fecha_hasta_unix,vehiculo)
            rows = parseXls('data'+vehiculo+'.xls')
            insertRows(db, rows)
        except:
            print "No se registraron nuevos datos"
    else:
        print "Base de datos vacia"
    db.close()
        #exit()
if __name__ == '__main__':
    db = createDb('tabla.sqlite')
    opener = login()
    flag= raw_input("Desea introducir una nueva fecha (s/n): ") #ACA SE PUEDE PONER QUE SI YA EXISTE UN BD Y QUE NO ESTE VACIA, DIRECTAMENTE HAGA UN UPDATE
    if flag == 's':
        vehiculo = raw_input("Ingrese numero de vehiculo: ")
        fecha_desde = FechaDesde()
        fecha_hasta = FechaHasta()
        downloadXls(opener,fecha_desde,fecha_hasta,vehiculo)
        rows = parseXls('data'+vehiculo+'.xls')
        insertRows(db, rows)
    else:
        Update(db,opener)
    db.close()
