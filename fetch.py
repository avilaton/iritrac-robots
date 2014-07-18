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

def FechaDesde():
    #dia_desde = raw_input("Dia Desde en ""dd"": ")
    #mes_desde = raw_input("Mes Desde en ""MM"": ")
    #ano_desde = raw_input("Ano Desde en ""YYYY"": ")
    #hora_desde = raw_input("Hora Desde en ""HH"": ")
    #minuto_desde = raw_input("Minuto Desde en ""mm"": ")
    dia_desde='07'
    mes_desde='06'
    ano_desde='2014'
    hora_desde = '00'
    minuto_desde='00'
    fecha_desde = dia_desde + '/' + mes_desde + '/' + ano_desde + " " + hora_desde + ':' + minuto_desde
    t = datetime.strptime(fecha_desde, '%d/%m/%Y %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    timeunix = mktime(t.timetuple())
    print "########### Desde",timeunix
    return timeunix

def FechaHasta():
    #dia_hasta = raw_input("Dia Hasta en ""dd"": ")
    #mes_hasta = raw_input("Mes Hasta en ""MM"": ")
    #ano_hasta = raw_input("Ano Hasta en ""YYYY"": ")
    #hora_hasta = raw_input("Hora Hasta en ""HH"": ")
    #minuto_hasta = raw_input("Minuto Hasta ""mm"": ")
    dia_hasta='07'
    mes_hasta='06'
    ano_hasta='2014'
    hora_hasta = '17'
    minuto_hasta='23'
    fecha_hasta = dia_hasta+ '/' + mes_hasta + '/' + ano_hasta + " " + hora_hasta + ':' + minuto_hasta
    t = datetime.strptime(fecha_hasta, '%d/%m/%Y %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    timeunix = mktime(t.timetuple())
    print "################# hasta",timeunix
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
   
    #headers = rows[0].keys()
    for r in rows:
        data = Data(date=r['date'], lat=r['lat'], lon=r['lon'])
        data.alpha = r['alpha']
        data.speed = r['speed']
        data.altitude = r['altitude']
        data.event = r['event']
        data.zone = r['zone']
        data.vehicle = vehicle
        print "##########3",data
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
        try:
            print "Corredor: ",driver.driver_id
            xls = downloadXls(connection,fecha_desde,fecha_hasta, driver.driver_id)
            rows = parseXls(xls)
            insertRows(rows, driver.driver_id)
        except:
            print "Corredor: ",driver.driver_id, "no esta en la pagina"
        

def updateAll():
    connection = login()
    for driver in session.query(Driver).all():
        updateDriver(connection, driver.driver_id)

def createDrivers():
    db = session
    headers = ['orden', 'driver_id', 'name', 'country', 'starttime']
    dictArray = xlsParser(file('largada.xlsx').read(), headers=headers).toDictArray()
    # Empty dable before loading drivers
    db.query(Driver).delete()
    drivers = []
    for item in dictArray:
        drivers.append(Driver(
            id=int(item['orden']),
            driver_id=int(item['driver_id']), 
            name=item['name'],
            country=item['country']))
    db.add_all(drivers)
    db.flush()

def create_stage():
    zone_name_1 = ["K30","K54","K112","CP1","DZ186","K230","ASS1"]#vector que luego se cargaria desde un excel
    zone_name_2 = ["DZ35","K64","K104","K123","ASS2"]
    zone_name_prueba = ["BIVLC","K96"]

    for i, zone in enumerate(zone_name_1):
        stage = Stage(stage_id=1,zone=zone)
        session.add(stage)
    for i, zone in enumerate(zone_name_2):
        stage = Stage(stage_id=2,zone=zone)
        session.add(stage)
    session.commit()

def time_of_drivers():
    doc = xlrd.open_workbook("largada.xlsx") #abro el .xls
    sheet = doc.sheet_by_index(0) #Selecciono la hoja uno

    ncols = sheet.ncols
    nrows = sheet.nrows

    book_datemode = doc.datemode
    timetmp = time(0,0,0) #Tiempo temporal, es para hacer la comparacion
    for i in range(nrows):
        
        group = sheet.cell (i,1)
        name = sheet.cell (i,2)
        timecell = sheet.cell (i,4)

        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(timecell.value, book_datemode) #separo la fecha de la celda del excel
        
        #timedr = time(hour, minute, second) 
        timedr = timedelta(hours=hour,minutes=minute,seconds=second)
        
        if timedr == timetmp:
            #timedr = timedr + timedelta(seconds=30) no se xq no funciona, asi que hice la chanchada de abajo
            timedr = timedelta(hours=hour,minutes=minute,seconds=30) #si hay dos tiempos iguales, sumo 30 seg al segundo
        
        timerun = StartTime(id = i,driver_group=int(group.value), name=name.value,start_time= str(timedr))
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
    iri = Iritrack()
    iri.login('ruta2', 'DESAFIO')

    xls = iri.getData(1363910400, 1395532799, '4')
    print xls

def time_stage_zone():
    db = session
    print "Entre"
    driver=db.query(Driver.driver_id).all() #Busco todos los driver_id que se generaron por el excel largadas.xls
    zone = db.query(Stage.zone).filter(Stage.stage_id=="1").all() #cambiar el stage_id cuando cambie de etapa
    #alpha = db.query(Data.alpha).distinct().filter(Data.vehicle==Driver.driver_id).all()
    alpha = db.query(Data.alpha).distinct().all()
    
    vector_driver = []
    vector_zone = []
    vector_alpha = []
    vector_time = []
    
    
    myArray = []
    for i in range (len(alpha)) :
        alph=str(alpha[i]).split("'")
        vector_alpha.append(alph[1]) #Guardo en un vector todos los alpha

    for i in range (len(driver)) : 
        dri=str(driver[i]).split("'")
        vector_driver.append(dri[1])#Guardo en un vector todos los drivers

    for i in range(len(zone)):    
        Stagezone = str(zone[i]).split("'")
        vector_zone.append(Stagezone[1])
    #con esto logre tener en vectores los alpha,drivers y las zonas dependiendo de la etapa    
    print vector_alpha, " ", vector_driver, " ", vector_zone
    for i in range (len(vector_driver)):
        #Agarra un alpha y pregunta por todas las zonas, sig alpha y pregunta de vuelta por todas las zonas
        vehicle_num = vector_driver[i]
        start_time = db.query(StartTime.start_time).filter(StartTime.driver_group == vector_driver[i]).all() #busco el start time del alpha indicado
        start_time = str(start_time).split("'")
        start_time_tmp = datetime.strptime(start_time[1], '%H:%M:%S') #Convierto en datetime para poder restar dsp
        vector_time.append(start_time[1])
        vector_result = []
        vector_dateperzone = []
        for j in range (len(vector_zone)):
            
                zone_name = vector_zone[j]
                date_per_zone = db.query(Data.date).filter(Data.vehicle==vehicle_num, Data.zone==zone_name).first() #Busco la hora por la que paso en la zona, si no esta, salta un except
                
                if date_per_zone == None: #Si me da none es porque no paso por esa zona
                    vector_result.append('Unknow')
                    vector_dateperzone.append('Unknow')
                else:
                    date_per_zone=str(date_per_zone[0]).split("'")
                    date_per_zone = datetime.strptime(date_per_zone[0], '%Y-%m-%d %H:%M:%S')
                    date_zone = str(date_per_zone.hour) + ":" + str(date_per_zone.minute) + ":" + str(date_per_zone.second)  
                    vector_dateperzone.append(date_zone)
                    result = date_per_zone - start_time_tmp
                    result =  str(result).split(",")
                    vector_result.append(result[1])
        #myArray.append({'alpha':alpha_name,'startt':start_time[1],'timeK30':vector_dateperzone[0],'K30':vector_result[0],'timeK54':vector_dateperzone[1],'K54':vector_result[1],'timeK112':vector_dateperzone[2],'K112':vector_result[2],'timeCP1':vector_dateperzone[3],'CP1':vector_result[3],'timeDZ186':vector_dateperzone[4],'DZ186':vector_result[4],'timeK230':vector_dateperzone[5],'K230':vector_result[5],'timeASS1':vector_dateperzone[6],'ASS1':vector_result[6]})        
        print "Vehicle:",vehicle_num,"; Start Time:", start_time[1], ";Time Arrive K30:",vector_result[0] ,"; Result K30:",vector_result[0], "; Time Arrive K54:",vector_dateperzone[1],"; Result K54:",vector_result[1], ";Time Arrive K112:",vector_result[2] ,"; Result K112:",vector_result[2], ";Time Arrive CP1:",vector_result[3] ,"; Result CP1:",vector_result[3], ";Time Arrive DZ186:",vector_result[4] ,"; Result DZ186:",vector_result[4], ";Time Arrive K230:",vector_result[5] ,"; Result K230:",vector_result[5], ";Time Arrive ASS1:",vector_result[6] ,"; Result ASS1:",vector_result[6]
        #myArray.append({'alpha':alpha_name,'startt':start_time[1],'timeBIVLC':vector_dateperzone[0],'BIVLC':vector_result[0],'timeK96':vector_dateperzone[1],'K96':vector_result[1]})
        #print "Vehicle:",vehicle_num,"; Start Time:", start_time[1], "; Time Arrive BIVLC:",vector_dateperzone[0],"; Result BIVLC:",vector_result[0], ";Time Arrive K96:",vector_result[1] 

if __name__ == '__main__':
    # Cargar datos
    print "Creando drivers"
    #createDrivers()
    print "Fin. Creando StartTime"
    #time_of_drivers()
    print "Fin. Creando Stage"
    create_stage()
    print "Fin. First firstFetch"
    
    # Correr updates
    #firstFetch()
    #updateAll()

    # pruebas
    print "Fin. Creoando Stage"
    # time_stage_zone()
    #test_parsing()
    #test_query()
