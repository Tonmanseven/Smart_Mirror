import json
import pandas as pd
import sys
import requests
import os
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

from datetime import datetime
from desWeather import *

from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QTime 
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
        #Функция отображения времени
        #Timer 
        self.timer = QTimer()
        #Connect timer 
        self.timer.timeout.connect(self._update)
        #Start
        self.timer.start(1000)
        # Здесь прописываем событие нажатия на кнопку                     
        self.ui.pushButton_2.clicked.connect(self.DomainCheck)
        
    def _update(self):
        # Обновление каждую сек
        time = QTime.currentTime().toString()
        self.ui.label.setText(time)

    # Запрос текущей погоды
    def request_current_weather(self,url):
        try:
            lc = requests.get(url) #  params={'lang': 'ru'}
            data_lc = lc.json()                        #получаем данные с json
            cityIs =  data_lc["city"]            
            cuntrCode = data_lc["countryCode"]
            lat = data_lc["lat"] # Ширина 
            lon = data_lc["lon"] # Долгота
            lc_ru = requests.get(url, params={'lang': 'ru'})
            data_lc_ru = lc_ru.json() # Для русскоязчн. раскл
            cityRu = data_lc_ru["city"]

        except Exception as e:
            print("Exception (location):", e)
            pass

        #служба не работает, если есть ` на конце слова (Example: Kazan`). Поэтому проверяем название города
        l_str = len(cityIs)
        i = l_str - 1
        step = 1
        if cityIs[i] == "’":
            cityNow = cityIs[0:i:step] # Срезаем ` если таковой имеется
        else:
            print("(((0(")    

        c_city = "{},{}".format(cityNow,cuntrCode)
        
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'q':c_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()                        #получаем данные с json
            cityID = data["id"]
            cond = data['weather'][0]['description'] #ясно, пасмурно, дождь ...
            tempr =  data['main']['temp']            #значение темп
            hum =  data['main']['humidity']          #влажность
            windSpeed =  data['wind']['speed']          #скорость ветра
            windDeg =   data['wind']['deg']
            iCon = data['weather'][0]['icon']        #номер иконки 
            Deg2South = self.get_wind_direction(windDeg) #преобразуем углы в направления 

            #today is: 
            a = datetime.today()
            
            self.ui.inCountry.setText(cityRu)
            self.ui.todayIs.setText(a.strftime("%A %d %B"))
            self.ui.humidityLabel.setText("%d %%" % hum)
            self.ui.windLabel.setText("{} м/c {} ".format(windSpeed, Deg2South))
            self.ui.Temp.setText("%d °C" % tempr)
            self.ui.weathIs.setText("Сейчас {} °C, {}".format(tempr, cond))
            self.set_weather_icon(self.ui.TempIc, iCon)



        except Exception as e:
            print("Exception (weather):", e)
            pass
  
        return cityID    

    #Зашрузим нужную иконку
    def set_weather_icon(self, label, weather):
        pixmap = QPixmap(os.path.join('images', "%s.png" % weather))
        label.setPixmap(pixmap)

    def request_forecast(self, idCity):
        try:
            resuLT = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': idCity, 'units': 'metric', 'APPID': appid})
            dataIS = resuLT.json()

            dan = dataIS['list']

            dandtime= pd.DataFrame(dan)
            myDataTime = dandtime['dt']

            i = 0
            while i < 8:
                listTime = datetime.fromtimestamp(myDataTime.loc[i]).strftime(
                    '%I:%M %p %b. %d.%y')
                self.ui.label_2.setText(datetime.fromtimestamp(myDataTime.loc[0]).strftime(
                    '%I:%M %p %b. %d.%y'))
                self.ui.label_3.setText(datetime.fromtimestamp(myDataTime.loc[1]).strftime(
                    '%I:%M %p %b. %d.%y'))
                self.ui.label_4.setText(datetime.fromtimestamp(myDataTime.loc[2]).strftime(
                    '%I:%M %p %b. %d.%y'))
                self.ui.label_5.setText(datetime.fromtimestamp(myDataTime.loc[3]).strftime(
                    '%I:%M %p %b. %d.%y'))
                self.ui.label_6.setText(datetime.fromtimestamp(myDataTime.loc[4]).strftime(
                    '%I:%M %p %b. %d.%y'))
                self.ui.label_7.setText(datetime.fromtimestamp(myDataTime.loc[5]).strftime(
                    '%I:%M %p %b. %d.%y'))
                self.ui.label_8.setText(datetime.fromtimestamp(myDataTime.loc[6]).strftime(
                    '%I:%M %p %b. %d.%y'))
                self.ui.label_9.setText(datetime.fromtimestamp(myDataTime.loc[7]).strftime(
                    '%I:%M %p %b. %d.%y'))
                i += 1

        except Exception as e:
            print("Exception (forecast):", e)
            pass

    def set_new_icon(self, label):
        pixmapy = QPixmap(os.path.join('ic', "01.svg"))
        label.setPixmap(pixmapy)

    #Функция перевода с градуса напр ветра в напр
    def get_wind_direction(self, deg):
        l = ['Северный','Северо-Восточный',' Восточный','Юго-Восточный','Южный ','Юго-Западный',' Западный','Северо-Западный']
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
        IDc = self.request_current_weather(url)
        self.request_forecast(IDc)
        #self.request_current_weather(url)  

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = desWeather()
    myapp.show()
    sys.exit(app.exec_())
   
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
