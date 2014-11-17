from bottle import template, request,redirect
from server import app
from server.models import Data
from server.models import Driver
from server.models import Stage
from server.models import StartTime
from server.models import LastUpdate
from server.models import DateUpdate
from server.models import DateDriverUpdate
from time import mktime
from datetime import *
from server.services import dataFetch
@app.route('/resultado/<stage_id>')
def index(db,stage_id):
    
    drivers=db.query(StartTime.driver_group,StartTime.start_time).filter(StartTime.stage_id==stage_id).all() #Busco todos los driver_id que se generaron por el excel largadas.xls
    zones = db.query(Stage.zone).filter(Stage.stage_id==stage_id).all() #cambiar el stage_id cuando cambie de etapa
    start_times = drivers

    try:
        last_update = db.query(LastUpdate.time).filter(LastUpdate.id =="1").one() #Me trae la ultima fecha de actualizacion
    except:
        last_update= " "

    vector_driver = []
    vector_zone = []
    vector_time = []
    vector_timezone = []
    tiemporsultado = []
    zonaresultado = []
    tiempolastresultado = []
    zonalastresultado = []
    vector_start_time = []
    myArray = []
    starttimedr = []
    for start_time in start_times:
        vector_start_time.append(start_time.start_time)
    
    for zone in zones:    
        vector_zone.append(zone.zone)
        timename = "time" + zone.zone
        vector_timezone.append(timename)

    #con esto logre tener en vectores los alpha,drivers y las zonas dependiendo de la etapa    
    for i,driver in enumerate(drivers):
        
        vector_driver.append(driver.driver_group)
        #Agarra un alpha y pregunta por todas las zonas, sig alpha y pregunta de vuelta por todas las zonas
        vehicle_num = driver.driver_group
        
        start_time_tmp = datetime.strptime(vector_start_time[i], '%H:%M:%S') #Convierto en datetime para poder restar dsp
        vector_time.append(vector_start_time[i])
        vector_result = []
        vector_dateperzone = []
        for zone in zones:
            
                date_per_zones = db.query(Data.date).filter(Data.vehicle==vehicle_num, Data.zone==zone.zone).all() #Busco la hora por la que paso en la zona, si no esta, salta un except
                
                firstTime = ""
                for eachzone in date_per_zones:
                    firstTime = eachzone.date

                date_per_zones.reverse()

                lastTime = ""
                for eachzone in date_per_zones:
                    lastTime = eachzone.date
                
                try:
                    convertfirstTime = datetime.strptime(firstTime, '%Y-%m-%d %H:%M:%S')
                    firstHour = str(convertfirstTime.hour)
                    firstMinute = str(convertfirstTime.minute)
                    firstSeg = str(convertfirstTime.second)
                    if len(firstHour) == 1:
                        firstHour= "0" + firstHour
                    if len(firstMinute) == 1:
                        firstMinute= "0" + firstMinute
                    if len(firstSeg) == 1:
                        firstSeg= "0" + firstSeg
                    firstDate = firstHour + ":" + firstMinute + ":" + firstSeg    
                    firstResult = convertfirstTime - start_time_tmp
                    firstResult =  str(firstResult).split(",")
                    tiemporsultado.append(firstDate)
                    zonaresultado.append(firstResult[1])

                    convertlastTime = datetime.strptime(lastTime, '%Y-%m-%d %H:%M:%S')
                    lastHour = str(convertlastTime.hour)
                    lastMinute = str(convertlastTime.minute)
                    lastSeg = str(convertlastTime.second)
                    if len(lastHour) == 1:
                        lastHour= "0" + lastHour
                    if len(lastMinute) == 1:
                        lastMinute= "0" + lastMinute
                    if len(lastSeg) == 1:
                        lastSeg= "0" + lastSeg
                    lastDate = lastHour + ":" + lastMinute + ":" + lastSeg 
                    lastResultTime = convertlastTime - start_time_tmp
                    lastResultTime = str(lastResultTime).split(",")


                    convertResult = convertlastTime - convertfirstTime
                    lastResult = []
                    lastResult = str(convertResult).split(":")
                    
                    if lastResult[0] > '1':
                        
                        tiempolastresultado.append(lastDate)
                        zonalastresultado.append(lastResultTime[1])
                    elif lastResult[0] == '1' and lastResult[1] > '29':
                        
                        tiempolastresultado.append(lastDate)
                        zonalastresultado.append(lastResultTime[1])
                    else:
                        tiempolastresultado.append("-")
                        zonalastresultado.append("-")
                    
                    
                except:
                    tiemporsultado.append(' ')
                    tiempolastresultado.append(' ') # es a la hora en que llego
                    zonaresultado.append(' ')
                    zonalastresultado.append(' ') #es la diferencia de los tiempos
            
                    
                    
    
    count = db.query(Stage.stage_id).distinct().count()      
    return template('result.html', vehiculo=vector_driver, fecha=last_update[0],zonename = vector_zone,  zoneresult=zonaresultado,timeresult=tiemporsultado,startime=vector_time, stage_id=stage_id,count=count, flagloop = True,searching=0, tiempolast = tiempolastresultado, zonalast = zonalastresultado)
    #return "ok"
    
    

@app.route('/resultado/show', method='POST')
def refresh(db):
    stage_id = request.forms.get('stage')
    redirect('/resultado/%s'% stage_id)
    
@app.post('/resultado')
def searchData(db):
    dateFrom = request.forms.get('from')
    dateTo = request.forms.get('to')
    stage_id = request.forms.get('stage_id')

    fecha_desde = dateFrom + ' 00:00'
    t = datetime.strptime(fecha_desde, '%Y-%m-%d %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    fecha_desde = mktime(t.timetuple())

    fecha_hasta = dateTo + " " + ' 23:59'
    t = datetime.strptime(fecha_hasta, '%Y-%m-%d %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    fecha_hasta = mktime(t.timetuple())
    
    if fecha_desde == fecha_hasta:
        time_now = datetime.now().strftime("%H:%M")
        fecha_hasta = dateTo + " " + time_now
        t = datetime.strptime(fecha_hasta, '%Y-%m-%d %H:%M')
        t = t - timedelta(hours=3) #Convierto a UTC - 3
        fecha_hasta = mktime(t.timetuple())    
    
    #dataFetch(fecha_desde,fecha_hasta).firstFetch()
    firstdriver = db.query(StartTime.driver_group,StartTime.gid).filter(StartTime.stage_id==1,StartTime.gid==1).first()
    db.query(DateUpdate).delete()
    date = DateUpdate(id=1,firstDate= fecha_desde, secondDate=fecha_hasta,lastId=firstdriver.gid)
    db.add(date)
    db.commit()

    dataFetch(fecha_desde,fecha_hasta).firstnewFetch(firstdriver.driver_group)
    redirect('/resultado/loop')
    
@app.route('/result/deletall')
def deleteall(db):
    db.query(Data).delete()
    redirect('/resultado/1')

@app.post('/resultado/update/<stage_id>/<state>')
@app.route('/resultado/update/<stage_id>/<state>')
def updateData(db,stage_id,state):
    lastgid = db.query(StartTime.gid).filter(StartTime.stage_id==stage_id).order_by(StartTime.gid.desc()).first()
    lastDriver = db.query(DateDriverUpdate).first()
    
    if state == 'True':
        db.query(DateDriverUpdate).delete()
        firstId = db.query(StartTime.gid).filter(StartTime.stage_id == stage_id).first()
        date = DateDriverUpdate(id = 1,lastdriverId = firstId.gid)
        db.add(date)
        db.commit()
        driver = db.query(StartTime.driver_group).filter(StartTime.gid == 1).first()
        
        dataFetch("a","b").updateDriver(driver.driver_group)
        
        nextId = int(firstId.gid) + 1
        db.query(DateDriverUpdate).filter(DateDriverUpdate.id == 1).update({'lastdriverId':nextId})
        db.commit()
        
        redirect('/resultado/still/%s'% stage_id)

    else:
        lastDriver = db.query(DateDriverUpdate).first()
        if lastgid.gid == lastDriver.lastdriverId:
            db.query(DateDriverUpdate).delete()
            redirect('/resultado/%s'% stage_id)

        driver = db.query(StartTime.driver_group).filter(StartTime.gid == lastDriver.lastdriverId,StartTime.stage_id == stage_id).first()
        dataFetch("a","b").updateDriver(driver.driver_group)
        
        newid = lastDriver.lastdriverId + 1
        db.query(DateDriverUpdate).filter(DateDriverUpdate.id == 1).update({'lastdriverId':newid})
        db.commit()
        redirect('/resultado/still/%s'% stage_id)


@app.route('/resultado/loop')
def updateDataLoop(db):
    lastgid = db.query(StartTime.gid).filter(StartTime.stage_id==1).order_by(StartTime.gid.desc()).first()
    loopgid = db.query(DateUpdate).first()
    fecha_desde = loopgid.firstDate
    fecha_hasta = loopgid.secondDate
    if lastgid.gid == loopgid.lastId:
        flagloop = True
        redirect('/resultado/1')
    else:
        newGid = int(loopgid.lastId) + 1
        dates = db.query(DateUpdate.firstDate,DateUpdate.secondDate).first()
        driver = db.query(StartTime.driver_group).filter(StartTime.gid == newGid).first()
        dataFetch(dates.firstDate,dates.secondDate).firstnewFetch(driver.driver_group)
        db.query(DateUpdate).delete()
        searching = int(driver.driver_group) + 1

        date = DateUpdate(id=1,firstDate= fecha_desde, secondDate=fecha_hasta,lastId=newGid)
        db.add(date)
        db.commit()
        
   
@app.route('/resultado/still/<stage_id>')
def stillUpdate(db,stage_id):
    drivers=db.query(StartTime.driver_group,StartTime.start_time).filter(StartTime.stage_id==stage_id).all() #Busco todos los driver_id que se generaron por el excel largadas.xls
    zones = db.query(Stage.zone).filter(Stage.stage_id==stage_id).all() #cambiar el stage_id cuando cambie de etapa
    start_times = drivers

    try:
        last_update = db.query(LastUpdate.time).filter(LastUpdate.id =="1").one() #Me trae la ultima fecha de actualizacion
    except:
        last_update= " "

    vector_driver = []
    vector_zone = []
    vector_time = []
    vector_timezone = []
    tiemporsultado = []
    zonaresultado = []
    tiempolastresultado = []
    zonalastresultado = []
    vector_start_time = []
    myArray = []
    starttimedr = []
    for start_time in start_times:
        vector_start_time.append(start_time.start_time)

    for zone in zones:    
        vector_zone.append(zone.zone)
        timename = "time" + zone.zone
        vector_timezone.append(timename)
    #con esto logre tener en vectores los alpha,drivers y las zonas dependiendo de la etapa    
    for i,driver in enumerate(drivers):
        
        vector_driver.append(driver.driver_group)
        #Agarra un alpha y pregunta por todas las zonas, sig alpha y pregunta de vuelta por todas las zonas
        vehicle_num = driver.driver_group

        start_time_tmp = datetime.strptime(vector_start_time[i], '%H:%M:%S') #Convierto en datetime para poder restar dsp
        vector_time.append(vector_start_time[i])
        vector_result = []
        vector_dateperzone = []
        for zone in zones:
            
                date_per_zones = db.query(Data.date).filter(Data.vehicle==vehicle_num, Data.zone==zone.zone).all() #Busco la hora por la que paso en la zona, si no esta, salta un except
                
                firstTime = ""
                for eachzone in date_per_zones:
                    firstTime = eachzone.date

                date_per_zones.reverse()

                lastTime = ""
                for eachzone in date_per_zones:
                    lastTime = eachzone.date
                
                try:
                    convertfirstTime = datetime.strptime(firstTime, '%Y-%m-%d %H:%M:%S')
                    firstHour = str(convertfirstTime.hour)
                    firstMinute = str(convertfirstTime.minute)
                    firstSeg = str(convertfirstTime.second)
                    if len(firstHour) == 1:
                        firstHour= "0" + firstHour
                    if len(firstMinute) == 1:
                        firstMinute= "0" + firstMinute
                    if len(firstSeg) == 1:
                        firstSeg= "0" + firstSeg
                    firstDate = firstHour + ":" + firstMinute + ":" + firstSeg    
                    firstResult = convertfirstTime - start_time_tmp
                    firstResult =  str(firstResult).split(",")
                    tiemporsultado.append(firstDate)
                    zonaresultado.append(firstResult[1])

                    convertlastTime = datetime.strptime(lastTime, '%Y-%m-%d %H:%M:%S')
                    lastHour = str(convertlastTime.hour)
                    lastMinute = str(convertlastTime.minute)
                    lastSeg = str(convertlastTime.second)
                    if len(lastHour) == 1:
                        lastHour= "0" + lastHour
                    if len(lastMinute) == 1:
                        lastMinute= "0" + lastMinute
                    if len(lastSeg) == 1:
                        lastSeg= "0" + lastSeg
                    lastDate = lastHour + ":" + lastMinute + ":" + lastSeg 
                    lastResultTime = convertlastTime - start_time_tmp
                    lastResultTime = str(lastResultTime).split(",")


                    convertResult = convertlastTime - convertfirstTime
                    lastResult = []
                    lastResult = str(convertResult).split(":")
                    
                    if lastResult[0] > '1':
                        
                        tiempolastresultado.append(lastDate)
                        zonalastresultado.append(lastResultTime[1])
                    elif lastResult[0] == '1' and lastResult[1] > '29':
                        
                        tiempolastresultado.append(lastDate)
                        zonalastresultado.append(lastResultTime[1])
                    else:
                        tiempolastresultado.append("-")
                        zonalastresultado.append("-")
                    
                    
                except:
                    tiemporsultado.append(' ')
                    tiempolastresultado.append(' ') # es a la hora en que llego
                    zonaresultado.append(' ')
                    zonalastresultado.append(' ') #es la diferencia de los tiempos

            
                    
                    

    count = db.query(Stage.stage_id).distinct().count()
    lastgid = db.query(StartTime.gid).filter(StartTime.stage_id==stage_id).order_by(StartTime.gid.desc()).first()
    countDriver = lastgid.gid
    lastDriver = db.query(DateDriverUpdate).first()
    ultimoid = lastDriver.lastdriverId
    newid = int(ultimoid) + 1
    percent = float(newid)/float(countDriver)*100
    return template('result.html', vehiculo=vector_driver, fecha=last_update[0],zonename = vector_zone,  zoneresult=zonaresultado,timename = vector_timezone,timeresult=tiemporsultado,startime=vector_time, stage_id=stage_id,count=count, flagloop = "update",searching=int(percent), tiempolast = tiempolastresultado, zonalast = zonalastresultado)
    #return template('result.html', vehiculo=vector_driver, fecha=last_update[0],zonename = vector_zone,  zoneresult=zonaresultado,timeresult=tiemporsultado,startime=vector_time, stage_id=stage_id,count=count, flagloop = True,searching=int(percent), tiempolast = tiempolastresultado, zonalast = zonalastresultado)
    #return template('result.html', vehiculo=vector_driver, fecha=last_update[0],zonename = vector_zone,  zoneresult=zonaresultado,timename = vector_timezone,timeresult=tiemporsultado,startime=vector_time, stage_id=stage_id,count=count, flagloop = "update",searching=int(percent))