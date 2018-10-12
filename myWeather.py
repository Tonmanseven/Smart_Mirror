import json
import sys
import requests
import os
import time, locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from desWeather import *

from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap

#api key Open Weather Mapx
appid = "982f4d4efd2cef497588658a85c4d309"

#адрес получения текущей геопозиции
url = "http://ip-api.com/json"

#Импортируем наш интерфейс
class desWeather(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self.DomainCheck()
        
        # Здесь прописываем событие нажатия на кнопку                     
        self.ui.pushButton_2.clicked.connect(self.DomainCheck)

    # Определение текущего местоположения
    def request_location(self,url):
        try:
            lc = requests.get(url, params={'lang': 'ru'})
            data_lc = lc.json()                        #получаем данные с json
            cityIs =  data_lc["city"]
            lat = data_lc["lat"] # Ширина 
            lon = data_lc["lon"] # Долгота

        except Exception as e:
            print("Exception (location):", e)
            pass
        
        return lat, lon

    # Запрос текущей погоды
    def request_current_weather(self,lat, lon):
        try:
            # res = requests.get("http://api.openweathermap.org/data/2.5/weather",
            #              params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                          params={'lat': lat, 'lon': lon , 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()                        #получаем данные с json
            cond = data['weather'][0]['description'] #ясно, пасмурно, дождь ...
            tempr =  data['main']['temp']            #значение темп
            hum =  data['main']['humidity']          #влажность
            windSpeed =  data['wind']['speed']          #скорость ветра
            windDeg =   data['wind']['deg']
            iCon = data['weather'][0]['icon']        #номер иконки 
            Deg2South = self.get_wind_direction(windDeg) #преобразуем углы в направления 

            #time 
            a = datetime.today()
            self.ui.label.setText(a.strftime("%H:%M:%S"))

            self.ui.todayIs.setText(a.strftime("%A %d %B"))
            self.ui.humidityLabel.setText("%d %%" % hum)
            self.ui.windLabel.setText("%d м/c" % windSpeed)
            self.ui.Temp.setText("%d °C" % tempr)
            self.ui.weathIs.setText("Сейчас {} °C, {}, ветер:{} м/с {}".format(tempr, cond, windSpeed, Deg2South))
            self.set_weather_icon(self.ui.TempIc, data['weather'][0]['icon'])
        except Exception as e:
            print("Exception (weather):", e)
            pass


    #Зашрузим нужную иконку
    def set_weather_icon(self, label, weather):    
        pixmap = QPixmap(os.path.join('images', "%s.png" % weather))
        label.setPixmap(pixmap)
    
    #Функция перевода с градуса напр ветра в напр
    def get_wind_direction(self, deg):
        l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
        for i in range(0,8):
            step = 45.
            min = i*step - 45/2.
            max = i*step + 45/2.
            if i == 0 and deg > 360-45/2.:
                deg = deg - 360
            if deg >= min and deg <= max:
                result = l[i]
                break
        return result

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку                  
    def DomainCheck(self):
        #self.request_location(url)
        self.request_current_weather(self.request_location(url), self.request_location(url))  

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = desWeather()
    myapp.show()
    sys.exit(app.exec_())
   

# Проверка наличия в базе информации о нужном населенном пункте
# def get_city_id(s_city_name):
#     try:
#         res = requests.get("http://api.openweathermap.org/data/2.5/find",
#                      params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
#         data = res.json()
#         cities = ["{} ({})".format(d['name'], d['sys']['country'])
#                   for d in data['list']]
#         print("city:", cities)
#         city_id = data['list'][0]['id']
#         print('city_id=', city_id)
#     except Exception as e:
#         print("Exception (find):", e)
#         pass
#     assert isinstance(city_id, int)
#     return city_id

# #Проверка в случае если назавние городов совпадают, но они с разных стран
# if len(sys.argv) == 2:
#     s_city_name = sys.argv[1]
#     print("city:", s_city_name)
#     city_id = get_city_id(s_city_name)
# elif len(sys.argv) > 2:
#     print('Enter name of city as one argument. For example: Petersburg,RU')
#     sys.exit()    




# Прогноз на 5 дней
# def request_forecast(city_id):
#     try:
#         res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
#                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
#         data = res.json()
#         print('city:', data['city']['name'], data['city']['country'])
#         for i in data['list']:
#             print( (i['dt_txt'])[:16], '{0:+3.0f}'.format(i['main']['temp']),
#                    '{0:2.0f}'.format(i['wind']['speed']) + " м/с",
#                    get_wind_direction(i['wind']['deg']),
#                    i['weather'][0]['description'] )
#     except Exception as e:
#         print("Exception (forecast):", e)
#         pass

#request_forecast(city_id)
#request_current_weather(city_id)