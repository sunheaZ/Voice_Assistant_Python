import queue # Подключение библиотеки queue
import sounddevice as sd # Подключение библиотеки sounddevice
import vosk # Подключение библиотеки vosk
import json # Подключение библиотеки json
import words # Подключение исполнительного файла words.py
from sklearn.feature_extraction.text import CountVectorizer # Импортирование класса CountVectorizer из библиотеки Scikit-learn
from sklearn.linear_model import LogisticRegression # Импортирование класса LogisticRegression из библиотеки Scikit-learn
from skills import * # Импортирование всех имен, определенных в файле skills.py,
# то есть если в файле skills.py определены какие-то функции, классы или переменные,то в текущем файле они также будут доступны

q = queue.Queue() # Создание очереди для обмена данными между потоками

model = vosk.Model('model_small') # Загрузка модели для распознавания речи

device = sd.default.device # Выбор устройств входа и выхода звука. В данном случае используются устройства по умолчанию
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate']) # Получаем частоту дискретизации звука, используя устройство входа звука,
# указанное в `device[0]`, и извлекаем значение поля 'default_samplerate' из ответа.



def callback(indata, frames, time, status): # Функция callback, которая вызывается для каждого блока аудиоданных
    # indata - массив байтов с аудиоданными
    # frames - количество фреймов в indata
    # time - время, связанное с данными
    # status - статус (например, ошибка)

    q.put(bytes(indata)) # Помещаем аудиоданные в очередь для дальнейшей обработки


def recognize(data, vectorizer, clf): # Функция распознавания речи
    trg = words.TRIGGERS.intersection(data.split()) # Находим имя ассистента в запросе пользователя
    if not trg: # Если имя ассистента не звучало,
        return # то ничего не происходит

    data.replace(list(trg)[0], '') # Удаляем имя ассистента из данных
    text_vector = vectorizer.transform([data]).toarray()[0] # Преобразуем текст в вектор
    answer = clf.predict([text_vector])[0] # Предсказываем ответ с помощью классификатора
    func_name = answer.split()[0] # Извлекаем имя функции из ответа

    print("Крот:", answer.replace(func_name, ''))  # Выводим ответ на экран
    speaker(answer.replace(func_name, '')) # Вызываем голосового ассистента для чтения ответа
    exec(func_name + '()')  # Выполняем функцию, имя которой было извлечено из ответа

def main(): # Основная функция приложения голосового ассистента
    print('Слушаем') # Выводим пользователю информацию о том, что программа запущена и готова к приему запросов
    vectorizer = CountVectorizer() # Создаем экземпляр векторизатора CountVectorizer для преобразования текстовых данных в векторы
    vectors = vectorizer.fit_transform(list(words.data_set.keys())) # Преобразуем ключи словаря data_set в векторы с использованием векторизатора

    clf = LogisticRegression() # Создаем экземпляр классификатора LogisticRegression для обучения модели
    clf.fit(vectors, list(words.data_set.values())) # Обучаем модель на векторах и соответствующих значениях из словаря data_set

    del words.data_set # Удаляем словарь data_set из памяти, так как он больше не нужен

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=callback): # Прописываем параметры микрофона

        rec = vosk.KaldiRecognizer(model, samplerate) # Создание экземпляра распознавателя Vosk с загруженным моделью и частотой дискретизации
        while True: # Бесконечный цикл для непрерывного приема аудиоданных
            data = q.get()  # Получение данных из очереди
            if rec.AcceptWaveform(data): # Если распознаватель успешно принял аудиоволну
                data = json.loads(rec.Result())['text'] # Извлечение текста из результата распознавания
                recognize(data, vectorizer, clf) # Вызов функции распознавания с полученным текстом, векторизатором и классификатором


if __name__ == '__main__': # Вызываем главную функцию программы, если скрипт запущен напрямую
    main()