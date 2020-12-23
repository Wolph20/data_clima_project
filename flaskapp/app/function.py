import requests, json
from io import open
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
# from scipy.interpolate import interpld

# Esta función calcula la media de un conjunto de valor ingresado.
def get_mean(lista):
    try:
        sum = 0
        for i in lista:
            sum += i
        return sum/len(lista)
    except ZeroDivisionError:
        return None

# Esta función calcula la regresión lineal de un conjunto de datos ingresado y retorna la gráfica correspondiente.
def Get_regression(region, data, indepen, depen):
    x = np.array(list(range(1,len(data)+1)))
    y = np.array(data)
    plt.plot(x,y,'o', label = 'Data')
    plt.ylabel(indepen)
    plt.xlabel(depen)
    plt.title(region)
    coeficientes = np.polyfit(x,y,1)
    polinomio = np.poly1d(coeficientes)
    ys = polinomio(x)
    plt.plot(x,ys,)
    Show = plt.show()
    return Show

# y=[28.45068, 27.23785, 27.42493, 25.9657]

# print(Get_regression(y, 'Temperaturas', 'Días'))

url = "http://148.247.201.227:5200/Clustering"

lat1 = "26.29824"
lat2 = "25.5473"
lat3 = "21.64201"
long1 = "-105.14286"
long2 = "-98.68289"
long3 = "-97.97977"
fech_ini = "10/05/2019"
fech_fin = "15/05/2019"

# Esta función hace la extracción de los datos desde un Datawarehouse.
def ConsumGeoposData(url, lat1, lat2, lat3, long1, long2, long3, fech_ini, fech_fin):
    

    data = {"polygon":{"1":{"lat":lat1,"lon":long1},
    "2":{"lat":lat2,"lon":long2},
    "3":{"lat":lat3,"lon":long3}
    },
    "inicio":fech_ini,
    "fin":fech_fin,
    "K":2,
    "type":1,
    "fuentes":"EMASMAX,MERRA",
    "variables":"Temp_max_emas,Temp_min_emas",
    "group":"1"
    }
    token = "Bearer, asn,jdijijineen,dnadanancja"
    _headers = {'Content-Type': 'application/json', 'Authorization': token}
    response = requests.post(url, data=json.dumps(data), headers= _headers)
    Re = json.loads(response.content)
    return Re['results']

# data = ConsumGeoposData(url,lat1,lat2,lat3,long1,long2,long3,fech_ini,fech_fin) 
# print(data)
with open('json_wolph.json') as file:
    pre_data = json.load(file)
data = pre_data['results']
# print(data)

# Esta función etrae la información necesaria de las informaciones recogidas del geoportal.
def Extract_data(data):
    t = 0
    geo_data = []
    while(t<len(data)):
        for id, item in data[t].items():
            if item['Temp_mean_emas'] != 'Null' and item['Temp_mean_emas'] != 'NA':
                new_temp = item['Temp_mean_emas']
            else: new_temp = item['Temp_mean_merra']
            geo_data.append({
                'Antena' : item['Antena'],
                'Latitud' : item['Latitud'],
                'Longitud' : item['Longitud'],
                'Temp_mean_emas' : new_temp,
                'Humedad' : item['Humedad'],
                'Precipitacion' : item['Precipitacion']
            })
            
        t+=1
    return geo_data

geo_data = Extract_data(data)
# for i in geo_data:
#     print(i)

# Procesamiento y transformación de los datos
def Data_process(data):
    data_process = []
    res = set(list(map(itemgetter('Antena'), geo_data)))
    # print(res)
    region = list(res)
    # En estas listas se guardan la temperatura, humedad y precipitación media de cada región.
    listTemp = []
    listHumedad = []
    listPrecip =[]

    # En estas listas se guardan la evolución de la temperatura, la humedad y la precipitación respectivamente,
    # de acuerdo al tiempo, estos datos van a servir para sacar una regresión lineal de cada uno.
    Temp_evol = []
    Humid_evol = []
    Precip_evol = []

    r = 0
    while r < len(region):

        list_temp = []
        list_humidity = []
        list_precip = []
        
        for item in geo_data:
            if item['Antena'] == region[r]:
                # print(item)
            
                if item['Temp_mean_emas']!= 'Null' and item['Temp_mean_emas']!= 'NA':
                    list_temp.append(float(item['Temp_mean_emas']))
                else: list_temp.append(float(0))
                    
                if item['Humedad']!= 'Null' and item['Humedad']!= 'NA':
                    list_humidity.append(float(item['Humedad']))
                else: list_humidity.append(float(0))
                
                if item['Precipitacion']!= 'Null' and item['Precipitacion']!= 'NA':
                    list_precip.append(float(item['Precipitacion']))
                else: list_precip.append(float(0))
        
        listTemp.append(get_mean(list_temp))
        listHumedad.append(get_mean(list_humidity))
        listPrecip.append(get_mean(list_precip))
        new_temp = get_mean(list_temp)
        new_humi = get_mean(list_humidity)
        new_precip = get_mean(list_precip)
        for item in geo_data:
            if item['Antena'] == region[r]:
                data_process.append({
                            'Antena' : region[r],
                            'Latitud' : item['Latitud'],
                            'Longitud' : item['Longitud'],
                            'Temp_mean_emas' : new_temp,
                            'Humedad' : new_humi,
                            'Precipitacion' : new_precip
                        })
                Temp_evol.append({
                    'Antena' : region[r],
                    'Temp_values' : list_temp
                })
                Humid_evol.append({
                    'Antena' : region[r],
                    'Humid_values' : list_humidity
                })
                break
        r+=1
    return data_process, Temp_evol, Humid_evol

(dat, temp, hum) = Data_process(geo_data)
# print(dat)
# print(temp)
# for i in temp:
#     print(i['Temp_values'])
#     print(Get_regression(i['Antena'], i['Temp_values'], 'Temperaturas', 'Días'))

def compare_temp(tmp_mean, tmp_minCult, tmp_maxCult):
    if tmp_mean <= tmp_maxCult and tmp_mean >= tmp_minCult:
        return True
    else: return False

def compare_hum(hum_mean, hum_minCult, hum_maxCult):
    if hum_mean <= hum_maxCult and hum_mean >= hum_minCult:
        return True
    else: return False
    
def compare_precip(precip_mean, precip_minCult, precip_maxCult):
    if precip_mean <= precip_maxCult and precip_mean >= precip_minCult:
        return True
    else: return False
    


dataY = {
    'product_name' : 'Cafe',
    'planting_date' : '05/07/2019',
    'temp_min' : 18,
    'temp_max' : 28,
    'precip_min' : 4.2,
    'precip_max' : 5.5,
    'humidity_min' : 70,
    'humidity_max' : 80
}
# print(dataY['temp_min'])
def Sticker(dataX,dataY):
    
    if compare_temp(dataX['Temp_mean_emas'],dataY['temp_min'],dataY['temp_max']) and compare_hum(dataX['Humedad'],dataY['humidity_min'],dataY['humidity_max']) and compare_precip(dataX['Precipitacion'],dataY['precip_min'],dataY['precip_max']):
        return(0.99) 
    elif compare_temp(dataX['Temp_mean_emas'],dataY['temp_min'],dataY['temp_max']) and compare_hum(dataX['Humedad'],dataY['humidity_min'],dataY['humidity_max']) :
        return(0.67) 
    elif compare_temp(dataX['Temp_mean_emas'],dataY['temp_min'],dataY['temp_max']) and compare_precip(dataX['Precipitacion'],dataY['precip_min'],dataY['precip_max']):
        return(0.67) 
    elif compare_hum(dataX['Humedad'],dataY['humidity_min'],dataY['humidity_max']) and compare_precip(dataX['Precipitacion'],dataY['precip_min'],dataY['precip_max']):
        return(0.67)
    elif compare_temp(dataX['Temp_mean_emas'],dataY['temp_min'],dataY['temp_max']):
        return(0.33)
    elif compare_hum(dataX['Humedad'],dataY['humidity_min'],dataY['humidity_max']):
        return(0.33)
    elif compare_precip(dataX['Precipitacion'],dataY['precip_min'],dataY['precip_max']):
        return(0.33)
    else: return(0.01)

def knowledge(dataX,dataY):
    archive_knowledge  = []
    for item in dataX:
        archive_knowledge.append({
                            'Antena' : item['Antena'],
                            'Latitud' : item['Latitud'],
                            'Longitud' : item['Longitud'],
                            'Temperatura media' : item['Temp_mean_emas'],
                            'Humedad' : item['Humedad'],
                            'Precipitacion' : item['Precipitacion'],
                            'Cultivo' : dataY['product_name'],
                            'Fiabilidad de siembra' : Sticker(item,dataY)
                        })
    return archive_knowledge

dict_data = knowledge(dat,dataY)
# print (dict_data)
# for i in dict_data:
#     print(i['Fiabilidad de siembra'])

# import csv
# csv_columns = ['Antena','Latitud','Longitud','Temperatura media','Humedad','Precipitacion','Cultivo','Fiabilidad de siembra']

# csv_file = "procesdata.csv"
# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         for data in dict_data:
#             writer.writerow(data)
# except IOError:
#     print("I/O error")

