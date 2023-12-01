import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
import psycopg2
from psycopg2 import Error
import requests
from geopy.geocoders import Nominatim
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import math

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather Data Table')
        self.setGeometry(100, 100, 900, 600)

        # Добавляем QLabel для отображения надписи
        self.city_label = QLabel('Город: Киров', self)
        self.city_label.setGeometry(50, 20, 150, 20)

        self.btn_Temp = QPushButton('Температура', self)
        self.btn_Temp.setGeometry(140, 20, 90, 25)
        self.btn_Temp.clicked.connect(self.Kolab_Temp)

        self.btn_Davl = QPushButton('Давление', self)
        self.btn_Davl.setGeometry(230, 20, 90, 25)
        self.btn_Davl.clicked.connect(self.Kolab_Davl)

        self.btn_vlahonst = QPushButton('Влажность', self)
        self.btn_vlahonst.setGeometry(320, 20, 90, 25)
        self.btn_vlahonst.clicked.connect(self.Kolab_vlahnost)

        self.btn_veter = QPushButton('Ветер', self)
        self.btn_veter.setGeometry(410, 20, 90, 25)
        self.btn_veter.clicked.connect(self.Kolab_veter)

        self.table_button = QPushButton('Облачность', self)
        self.table_button.setGeometry(500, 20, 90, 25)
        self.cloudiness_table_dialog_widget = None
        self.table_button.clicked.connect(self.show_cloudiness_table)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(50, 50, 800, 400)
        self.tableWidget.setColumnCount(11)

        try:
            connection = psycopg2.connect(user="postgres",
                                          password="qwerty",
                                          host="127.0.0.1",
                                          port="5435",
                                          database="postgres")
            with connection.cursor() as cursor:
                cursor.execute("SELECT CHISLO, TEMPERATYRA, DAVLENIE, YAVL, VETER, VLAHNOST FROM weather ORDER BY ID;")
                records = cursor.fetchall()
                for a in range(math.ceil(len(records) / 2) + 2):
                    self.tableWidget.insertRow(a)
                    if a >= 0:
                        record_1 = records[a * 2-4]
                        record_2 = records[a * 2 - 3]
                        for col_index, value in enumerate(record_1[:6]):
                            item_1 = QTableWidgetItem(str(value))
                            self.tableWidget.setItem(a, col_index, item_1)
                        for col_index, value in enumerate(record_2[1:6], start=6):
                            item_2 = QTableWidgetItem(str(value))
                            self.tableWidget.setItem(a, col_index, item_2)

            # Скрыть сетку и индексы строк
            # self.tableWidget.setShowGrid(False)
            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.horizontalHeader().setVisible(False)

            # Добавление заголовков и объединение ячеек
            self.tableWidget.setSpan(0, 1, 1, 5)
            self.tableWidget.setSpan(0, 6, 1, 5)
            self.tableWidget.setSpan(0, 0, 2, 1)
            new_item = QTableWidgetItem("Число")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("День")
            self.tableWidget.setItem(0, 1, new_item)
            new_item = QTableWidgetItem("Вечер")
            self.tableWidget.setItem(0, 6, new_item)
            new_item = QTableWidgetItem("Температура")
            self.tableWidget.setItem(1, 1, new_item)
            new_item = QTableWidgetItem("Давление")
            self.tableWidget.setItem(1, 2, new_item)
            new_item = QTableWidgetItem("Облачность")
            self.tableWidget.setItem(1, 3, new_item)
            new_item = QTableWidgetItem("Ветер")
            self.tableWidget.setItem(1, 4, new_item)
            new_item = QTableWidgetItem("Влажность")
            self.tableWidget.setItem(1, 5, new_item)
            new_item = QTableWidgetItem("Температура")
            self.tableWidget.setItem(1, 6, new_item)
            new_item = QTableWidgetItem("Давление")
            self.tableWidget.setItem(1, 7, new_item)
            new_item = QTableWidgetItem("Облачность")
            self.tableWidget.setItem(1, 8, new_item)
            new_item = QTableWidgetItem("Ветер")
            self.tableWidget.setItem(1, 9, new_item)
            new_item = QTableWidgetItem("Влажность")
            self.tableWidget.setItem(1, 10, new_item)

            # Выравнивание столбцов по содержимому
            self.tableWidget.resizeColumnsToContents()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def Kolab_Temp(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="qwerty",
                                          host="127.0.0.1",
                                          port="5435",
                                          database="postgres")
            with connection.cursor() as cursor:
                cursor.execute("SELECT chislo, temperatyra FROM weather")
                records = cursor.fetchall()

                dates = [datetime.strptime(record[0], "%d-%m-%Y") for record in records]
                temperatures = [float(record[1]) for record in records]

                plt.plot(dates, temperatures)
                plt.xlabel('Дата')
                plt.ylabel('Температура')
                plt.title('Колебание температуры')
                plt.show()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def Kolab_Davl(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                            password="qwerty",
                                            host="127.0.0.1",
                                            port="5435",
                                            database="postgres")
            with connection.cursor() as cursor:
                cursor.execute("SELECT chislo, davlenie FROM weather")
                records = cursor.fetchall()

                dates = [datetime.strptime(record[0], "%d-%m-%Y") for record in records]
                temperatures = [float(record[1]) for record in records]

                plt.plot(dates, temperatures)
                plt.xlabel('Дата')
                plt.ylabel('Давление')
                plt.title('Коллебание давления')
                plt.show()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def Kolab_vlahnost(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                            password="qwerty",
                                            host="127.0.0.1",
                                            port="5435",
                                            database="postgres")
            with connection.cursor() as cursor:
                cursor.execute("SELECT chislo, vlahnost FROM weather")
                records = cursor.fetchall()

                dates = [datetime.strptime(record[0], "%d-%m-%Y") for record in records]
                temperatures = [float(record[1]) for record in records]

                plt.plot(dates, temperatures)
                plt.xlabel('Дата')
                plt.ylabel('Влажность')
                plt.title('Коллебание влажности')
                plt.show()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def Kolab_veter(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                            password="qwerty",
                                            host="127.0.0.1",
                                            port="5435",
                                            database="postgres")
            with connection.cursor() as cursor:
                cursor.execute("SELECT chislo, veter FROM weather")
                records = cursor.fetchall()

                dates = [datetime.strptime(record[0], "%d-%m-%Y") for record in records]
                temperatures = [float(record[1]) for record in records]

                plt.plot(dates, temperatures)
                plt.xlabel('Дата')
                plt.ylabel('Скорость ветра')
                plt.title('Коллебание скорости ветра')
                plt.show()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def show_cloudiness_table(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="qwerty",
                                          host="127.0.0.1",
                                          port="5435",
                                          database="postgres")

            with connection.cursor() as cursor:
                date_limit = datetime.now().date() - timedelta(days=4)
                print(f"Дата-лимит: {date_limit}")
                cursor.execute("SELECT chislo, yavl FROM weather WHERE TO_DATE(chislo::text, 'DD-MM-YYYY') >= %s ORDER BY chislo DESC LIMIT 5",
                               (date_limit,))
                records = cursor.fetchall()

                print(f"Записи: {records}")


                if not self.cloudiness_table_dialog_widget:
                    self.cloudiness_table_dialog_widget = CloudinessTableDialog(records)
                self.cloudiness_table_dialog_widget.show()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")


class CloudinessTableDialog(QWidget):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle('Таблица Облачности')
        self.setGeometry(200, 200, 400, 300)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(50, 50, 300, 200)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Число','Облачность'])

        for row_index, record in enumerate(data):
            self.tableWidget.insertRow(row_index)
            for col_index, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_index, col_index, item)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

if __name__ == '__main__':
    # Подключение к базе данных
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="qwerty",
                                    host="127.0.0.1",
                                    port="5435",
                                    database="postgres")

        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = '''CREATE TABLE IF NOT EXISTS Weather
                            (ID SERIAL PRIMARY KEY,
                            CHISLO VARCHAR NOT NULL,
                            TEMPERATYRA VARCHAR NOT NULL,
                            DAVLENIE VARCHAR NOT NULL,
                            YAVL VARCHAR NOT NULL,
                            VETER VARCHAR NOT NULL,
                            VLAHNOST VARCHAR NOT NULL); '''
        cursor.execute(create_table_query)
        print("Таблица успешно создана в PostgreSQL")

        def get_weather(api_key, latitude, longitude):
            global Temperature, Pressure, Humidity, Wind_speed, Cloudy
            url = f'https://api.weather.yandex.ru/v2/informers?lat={latitude}&lon={longitude}&lang=ru_RU'

            headers = {
                'X-Yandex-API-Key': api_key,
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:

                weather_data = response.json()

                # Извлекаем интересующие нас данные на русском языке
                Temperature = weather_data['fact']['temp']
                Pressure = weather_data['fact']['pressure_mm']
                Humidity = weather_data['fact']['humidity']
                Wind_speed = weather_data['fact']['wind_speed']

                if weather_data['fact']['condition'] == 'clear':
                    Cloudy = 'ясно'
                elif weather_data['fact']['condition'] == 'partly-cloudy':
                    Cloudy = 'малооблачно'
                elif weather_data['fact']['condition'] == 'cloudy':
                    Cloudy = 'облачно с прояснениями'
                elif weather_data['fact']['condition'] == 'overcast':
                    Cloudy = 'пасмурно'
                elif weather_data['fact']['condition'] == 'light-rain':
                    Cloudy = 'небольшой дождь'
                elif weather_data['fact']['condition'] == 'rain':
                    Cloudy = 'дождь'
                elif weather_data['fact']['condition'] == 'heavy-rain':
                    Cloudy = 'сильный дождь'
                elif weather_data['fact']['condition'] == 'showers':
                    Cloudy = 'ливень'
                elif weather_data['fact']['condition'] == 'wet-snow':
                    Cloudy = 'дождь со снегом'
                elif weather_data['fact']['condition'] == 'light-snow':
                    Cloudy = 'небольшой снег'
                elif weather_data['fact']['condition'] == 'snow':
                    Cloudy = 'снег'
                elif weather_data['fact']['condition'] == 'snow-showers':
                    Cloudy = 'снегопад'
                elif weather_data['fact']['condition'] == 'hail':
                    Cloudy = 'град'
                elif weather_data['fact']['condition'] == 'thunderstorm':
                    Cloudy = 'гроза'
                elif weather_data['fact']['condition'] == 'thunderstorm-with-rain':
                    Cloudy = 'дождь с грозой'
                elif weather_data['fact']['condition'] == 'thunderstorm-with-hail':
                    Cloudy = 'гроза с градом'

                # Выводим результат на русском языке
                print(f"Temperature: {Temperature}°C")
                print(f"Pressure: {Pressure} мм рт. ст.")
                print(f"Cloudy: {Cloudy}")
                print(f"Wind_speed: {Wind_speed} м/с")
                print(f"Humidity: {Humidity}%")
            else:
                # Выводим сообщение об ошибке, если запрос неудачен
                print(f"Ошибка {response.status_code}: {response.text}")

        api_key = '187493ab-46ba-4a2e-9b36-24e6d15a6afe'

        geolocator = Nominatim(user_agent="my_app")

        # Определяем координаты города
        location = geolocator.geocode("Киров")

        # Выводим найденные координаты
        if location:
            latitude = location.latitude
            longitude = location.longitude

        get_weather(api_key, latitude, longitude)
        create_date_query = '''INSERT INTO weather (chislo, temperatyra, davlenie, yavl, veter, vlahnost) VALUES (%s,%s,%s,%s,%s,%s);'''
        date = datetime.now().strftime("%d-%m-%Y")
        date_query = (date, Temperature, Pressure, Cloudy, Wind_speed, Humidity)
        cursor.execute(create_date_query, date_query)

        print('Строки успешно созданы')
        connection.commit()
        print("Таблица успешно создана в PostgreSQL")
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM weather"""
            )
            print(cursor.fetchone())

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")

    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    ui = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())