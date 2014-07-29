from bottle import template, request
from server import app
from server.models import Data
from server.models import Driver
from server.models import Stage
from server.models import StartTime
from server.models import LastUpdate
from time import mktime
from datetime import *
@app.route('/resultado')
def index(db):
    driver=db.query(Driver.driver_id).filter(Driver.stage_id==1).all() #Busco todos los driver_id que se generaron por el excel largadas.xls
    zone = db.query(Stage.zone).filter(Stage.stage_id==1).all() #cambiar el stage_id cuando cambie de etapa
    #alpha = db.query(Data.alpha).distinct().filter(Data.vehicle==Driver.driver_id).all()
    alpha = db.query(Data.alpha).distinct().all()
    
    try:
        last_update = db.query(LastUpdate.time).filter(LastUpdate.id =="1").one() #Me trae la ultima fecha de actualizacion
    except:
        
        last_update= " "
    vector_driver = []
    vector_zone = []
    vector_alpha = []
    vector_time = []
    vector_timezone = []
    tiemporsultado = []
    zonaresultado = []
    myArray = []
    starttimedr = []
    for i in range (len(alpha)) :
        alph=str(alpha[i]).split("'")
        vector_alpha.append(alph[1]) #Guardo en un vector todos los alpha

    for i in range (len(driver)) : 
        dri=str(driver[i]).split("'")
        vector_driver.append(dri[1])#Guardo en un vector todos los drivers

    for i in range(len(zone)):    
        Stagezone = str(zone[i]).split("'")
        vector_zone.append(Stagezone[1])
        timename = "time" + Stagezone[1]
        vector_timezone.append(timename)
    #con esto logre tener en vectores los alpha,drivers y las zonas dependiendo de la etapa    
    for i in range (len(vector_driver)):
        #Agarra un alpha y pregunta por todas las zonas, sig alpha y pregunta de vuelta por todas las zonas
        vehicle_num = vector_driver[i]
        start_time = db.query(StartTime.start_time).filter(StartTime.driver_group == vector_driver[i], StartTime.stage_id==1).all() #busco el start time del alpha indicado
        start_time = str(start_time).split("'")
        start_time_tmp = datetime.strptime(start_time[1], '%H:%M:%S') #Convierto en datetime para poder restar dsp
        vector_time.append(start_time[1])
        vector_result = []
        vector_dateperzone = []
        for j in range (len(vector_zone)):
            
                zone_name = vector_zone[j]
                date_per_zone = db.query(Data.date).filter(Data.vehicle==vehicle_num, Data.zone==zone_name).first() #Busco la hora por la que paso en la zona, si no esta, salta un except
                
                if date_per_zone == None: #Si me da none es porque no paso por esa zona
                    vector_result.append(' ')
                    vector_dateperzone.append(' ')
                    tiemporsultado.append(' ')
                    zonaresultado.append(' ')
                else:
                    date_per_zone=str(date_per_zone[0]).split("'")
                    date_per_zone = datetime.strptime(date_per_zone[0], '%Y-%m-%d %H:%M:%S')
                    hora_zona = str(date_per_zone.hour)
                    minuto_zona = str(date_per_zone.minute)
                    segundo_zona = str(date_per_zone.second)
                    if len(hora_zona) == 1:
                        hora_zona= "0" + hora_zona
                    if len(minuto_zona) == 1:
                        minuto_zona= "0" + minuto_zona
                    if len(segundo_zona) == 1:
                        segundo_zona= "0" + segundo_zona
                    date_zone = hora_zona + ":" + minuto_zona + ":" + segundo_zona    
                    vector_dateperzone.append(date_zone)
                    result = date_per_zone - start_time_tmp
                    result =  str(result).split(",")
                    vector_result.append(result[1])
                    tiemporsultado.append(date_zone)
                    zonaresultado.append(result[1])

        #myArray.append({'alpha':alpha_name,'startt':start_time[1],'timeBIVLC':vector_dateperzone[0],'BIVLC':vector_result[0],'timeK96':vector_dateperzone[1],'K96':vector_result[1]})
        
        #myArray.append({'vehicle':vehicle_num,'startt':start_time[1],'timeE4K47':vector_dateperzone[0],'E4K47':vector_result[0],'timeE4K101':vector_dateperzone[1],'E4K101':vector_result[1],'timeE4CP1':vector_dateperzone[2],'E4CP1':vector_result[2],'timeE4K133':vector_dateperzone[3],'E4K133':vector_result[3],'timeASS4':vector_dateperzone[4],'ASS4':vector_result[4]})
           
    return template('data.tpl', vehiculo=vector_driver, fecha=last_update[0],zonename = vector_zone,  zoneresult=zonaresultado,timename = vector_timezone,timeresult=tiemporsultado,startime=vector_time, stage_id=1)
    #return "ok"
    
    

@app.route('/resultado', method='POST')
def refresh(db):
    stage_id = request.forms.get('stage')
    driver=db.query(Driver.driver_id).filter(Driver.stage_id==stage_id).all() #Busco todos los driver_id que se generaron por el excel largadas.xls
    zone = db.query(Stage.zone).filter(Stage.stage_id==stage_id).all() #cambiar el stage_id cuando cambie de etapa
    #alpha = db.query(Data.alpha).distinct().filter(Data.vehicle==Driver.driver_id).all()
    alpha = db.query(Data.alpha).distinct().all()
    
    try:
        last_update = db.query(LastUpdate.time).filter(LastUpdate.id =="1").one() #Me trae la ultima fecha de actualizacion
    except:
        
        last_update= " "
    vector_driver = []
    vector_zone = []
    vector_alpha = []
    vector_time = []
    vector_timezone = []
    tiemporsultado = []
    zonaresultado = []
    myArray = []
    starttimedr = []
    for i in range (len(alpha)) :
        alph=str(alpha[i]).split("'")
        vector_alpha.append(alph[1]) #Guardo en un vector todos los alpha

    for i in range (len(driver)) : 
        dri=str(driver[i]).split("'")
        vector_driver.append(dri[1])#Guardo en un vector todos los drivers

    for i in range(len(zone)):    
        Stagezone = str(zone[i]).split("'")
        vector_zone.append(Stagezone[1])
        timename = "time" + Stagezone[1]
        vector_timezone.append(timename)
    #con esto logre tener en vectores los alpha,drivers y las zonas dependiendo de la etapa    
    for i in range (len(vector_driver)):
        #Agarra un alpha y pregunta por todas las zonas, sig alpha y pregunta de vuelta por todas las zonas
        vehicle_num = vector_driver[i]
        start_time = db.query(StartTime.start_time).filter(StartTime.driver_group == vector_driver[i],StartTime.stage_id==stage_id).all() #busco el start time del alpha indicado
        start_time = str(start_time).split("'")
        start_time_tmp = datetime.strptime(start_time[1], '%H:%M:%S') #Convierto en datetime para poder restar dsp
        vector_time.append(start_time[1])
        vector_result = []
        vector_dateperzone = []
        for j in range (len(vector_zone)):
            
                zone_name = vector_zone[j]
                date_per_zone = db.query(Data.date).filter(Data.vehicle==vehicle_num, Data.zone==zone_name).first() #Busco la hora por la que paso en la zona, si no esta, salta un except
                
                if date_per_zone == None: #Si me da none es porque no paso por esa zona
                    vector_result.append(' ')
                    vector_dateperzone.append(' ')
                    tiemporsultado.append(' ')
                    zonaresultado.append(' ')
                else:
                    date_per_zone=str(date_per_zone[0]).split("'")
                    date_per_zone = datetime.strptime(date_per_zone[0], '%Y-%m-%d %H:%M:%S')
                    hora_zona = str(date_per_zone.hour)
                    minuto_zona = str(date_per_zone.minute)
                    segundo_zona = str(date_per_zone.second)
                    if len(hora_zona) == 1:
                        hora_zona= "0" + hora_zona
                    if len(minuto_zona) == 1:
                        minuto_zona= "0" + minuto_zona
                    if len(segundo_zona) == 1:
                        segundo_zona= "0" + segundo_zona
                    date_zone = hora_zona + ":" + minuto_zona + ":" + segundo_zona    
                    vector_dateperzone.append(date_zone)
                    result = date_per_zone - start_time_tmp
                    result =  str(result).split(",")
                    vector_result.append(result[1])
                    tiemporsultado.append(date_zone)
                    zonaresultado.append(result[1])

        #myArray.append({'alpha':alpha_name,'startt':start_time[1],'timeBIVLC':vector_dateperzone[0],'BIVLC':vector_result[0],'timeK96':vector_dateperzone[1],'K96':vector_result[1]})
        
        #myArray.append({'vehicle':vehicle_num,'startt':start_time[1],'timeE4K47':vector_dateperzone[0],'E4K47':vector_result[0],'timeE4K101':vector_dateperzone[1],'E4K101':vector_result[1],'timeE4CP1':vector_dateperzone[2],'E4CP1':vector_result[2],'timeE4K133':vector_dateperzone[3],'E4K133':vector_result[3],'timeASS4':vector_dateperzone[4],'ASS4':vector_result[4]})
           
    return template('data.tpl', vehiculo=vector_driver, fecha=last_update[0],zonename = vector_zone,  zoneresult=zonaresultado,timename = vector_timezone,timeresult=tiemporsultado,startime=vector_time, stage_id=stage_id)
    #return "ok"