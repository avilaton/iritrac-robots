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
from datetime import datetime
COOKIEFILE = 'cookies.lwp'
def FechaInicial():
        
	dia_inicial = raw_input("Dia Desde en ""dd"": ")
	mes_inicial = raw_input("Mes Desde en ""MM"": ")
	ano_inicial = raw_input("Ano Desde en ""YYYY"": ")
	hora_inicial = raw_input("Hora Desde en ""HH"": ")
	minuto_inicial = raw_input("Minuto Desde en ""mm"": ")
	fecha_inicial = dia_inicial + '/' + mes_inicial + '/' + ano_inicial + " " + hora_inicial + ':' + minuto_inicial
	t = datetime.strptime(fecha_inicial, '%d/%m/%Y %H:%M')
	timeunix = mktime(t.timetuple())
	return timeunix

def FechaFinal():
	dia_final = raw_input("Dia Hasta en ""dd"": ")
	mes_final = raw_input("Mes Hasta en ""MM"": ")
	ano_final = raw_input("Ano Hasta en ""YYYY"": ")
	hora_final = raw_input("Hora Hasta en ""HH"": ")
	minuto_final = raw_input("Minuto Hasta ""mm"": ")
	fecha_final = dia_final+ '/' + mes_final + '/' + ano_final + " " + hora_final + ':' + minuto_final
	t = datetime.strptime(fecha_final, '%d/%m/%Y %H:%M')
	timeunix = mktime(t.timetuple())
	return timeunix
      
def parseXls(filename):
    global ncols
    global nrows
    global columnas_vacias
    global sheet
    global columnas
    global sim
    doc = xlrd.open_workbook(filename) #abro el .xls
    sheet = doc.sheet_by_index(0) #Genera el objeto
    nrows = sheet.nrows #Guarda en nrows la cantidad de Filas
    ncols = sheet.ncols #Guarda en ncols la cantidad de Columnas
    tipos_datos = {0: 'TEXT',
                 1: 'TEXT',
                 2: 'REAL',
                 3: 'REAL',
                 4: 'INTEGER',
                }
    #Obtener la estructura de la tabla
    
    tabla = {}
    nombre_de_columnas=[]
    columnas = []
    sim = []
    columnas_vacias = []
    for i in range(ncols):
        nombre = sheet.cell_value(0,i)
        if str(nombre) != '':
            ctype = sheet.cell_type(1,i)
            columnas.append(str(nombre))
            nombre_de_columnas.append('%s %s'%(str(nombre), tipos_datos[ctype]))
            sim.append('?')
        else:
            columnas_vacias.append(i)

    headers = []
    for i in range(ncols):
        name = sheet.cell_value(0,i)
        headers.append(name.split(' ')[0])
        
    rows = []

    for i in range(nrows-1):
        row = [sheet.cell_value(i+1,j) for j in range(len(headers))]
        rows.append(row)
        
    dictArray = []
    
    for row in rows:
        dictArray = {k:row[j] for j,k in enumerate(headers)}
        
    return dictArray

def createDb(filename):
    #Trata de crear la tabla y si ya está creada, sigue
    global cursor
    global conn
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute (''' CREATE TABLE data
                (Alpha TEXT,
                DATE TEXT,
                LATITUD TEXT,
                LONG  TEXT,
                SPEED TEXT,
                ALTITUD TEXT,
                EVENT TEXT,
                ZONE TEXT)''')
        print "Tabla creada con Ã©xito"
        conn.commit()
    except:
        print "Tabla ya creada"

    return conn

def insertRows(rows):
    
    # headers = rows[0].keys()

    for row in rows:
        print row
    print nrows , " #########" 
    #insert_query = """INSERT INTO data 
    #    VALUES ({Alpha},{Datetime},{lat})""".format(Alpha=1, Datetime=21341, lat=123312)
    insert_query = 'insert into data values %s'%str(tuple(sim)).replace("'","")

    print insert_query
       
    for i in range(nrows):
        valores = []
        for j in range(ncols):
            if j not in columnas_vacias:
                valor = sheet.cell_value(i,j)
                if str(valor) not in columnas:
                    valores.append(str(valor))
                else:
                    break;
        print valores
        if valores != []:
             cursor.execute(insert_query,tuple(valores))
             conn.commit()
    
    
    
def downloadXls():
    # cj = cookielib.CookieJar()
    # this cookie jar stores the login cookie to a file. Should be checked for existence, 
    # and validity and if it is not valid, ask the user to login again.
    cj = cookielib.LWPCookieJar(COOKIEFILE)
    if os.path.isfile(COOKIEFILE):
        cj.load()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    username = raw_input("Please enter your username: ")
    password = raw_input("Please enter your password: ")
    query = {'username': username,'password': password,'valid': 'OK'}
    data = urllib.urlencode(query) 
    response = opener.open('http://tracking.iritrack.com/index.php', data)
    html = response.read()
    cj.save()
    fecha_inicial = FechaInicial()
    fecha_final = FechaFinal()
    vehiculo = raw_input("Ingrese numero de vehiculo: ")
    query = {'page':'positions.xl','name':'positions-1','vehicle':vehiculo,
    'date_from':fecha_inicial,'date_to':fecha_final,'time_from':fecha_inicial,'time_to':fecha_final}
    data = urllib.urlencode(query)
    excelResponse = opener.open('http://tracking.iritrack.com/index.php?'+data)
    xls = excelResponse.read()
    with open('data.xls','wb') as f:
        f.write(xls)

if __name__ == '__main__':
        
        downloadXls()
        #db = createDb('tabla.sqlite')
        #rows = parseXls('data.xls')
        #insertRows(rows)
