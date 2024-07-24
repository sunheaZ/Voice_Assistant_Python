import os, webbrowser, sys, requests, subprocess, pyttsx3 # Подключение всех нужных библиотек

engine = pyttsx3.init() # Инициализация голосового движка
engine.setProperty('rate', 180) # Установка скорости речи ассистента

def speaker(text): # Функция для озвучивания текста с помощью голосового движка, принимает аргумент text
    engine.say(text) # Передача аргумента text в голосовой движок для озвучивания
    engine.runAndWait() # Запуск голосового движка

def browser(): # Функция запуска браузера
    webbrowser.open('https://www.google.com', new=2)
    # print('браузер запускается')

def youtube(): # Функция запуска браузера
    webbrowser.open('https://www.youtube.com', new=2)
    # print('ютуб запускается')

def game(): # Функция запуска игр
    subprocess.Popen('C:/Program Files (x86)/Steam/steam.exe')
    # print('игра запускается')

def offpc(): # Функция отключения компьютера
    os.system('shutdown /s')
    # print('компьютер выключается')

def weather(): # Функция вывода информации о погоде
    try:
        params = {'q': 'Novotroitsk, RU', 'units': 'metric', 'lang': 'ru', 'appid': 'f41563937c41bb492132b564cc440b94'}
        # Создание словаря параметров для запроса к API
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        # Отправка запроса к API с указанными параметрами
        if not response: # Если ответ не получен
            raise # то генерируется исключение
        w = response.json() # Преобразовывание ответа в формат json
        print(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")  # Выводим информацию о погоде на экран
        speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов") # Вывод информации о погоде

    except: # Иначе выводит ошибку
        print('Произошла ошибка. Проверьте качество вашего интернет-соединения.')
        speaker('Произошла ошибка. Проверьте качество вашего интернет-соединения.')


def offBot(): # Функция отключения ассистента
    sys.exit() # Завершение работы приложения

def passive(): # Функция заглушка при обычном текстовом ответе ассистента
    pass