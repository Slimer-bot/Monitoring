import os
import requests
import urllib.request
from datetime import datetime, timedelta
import sqlite3
#Текущая дата
current_date = datetime.now().strftime('%d.%m.%Y')
#Логин и пароли
username = "kodeks"
#username1
password1 = "skedoks"
password2 = "skedok"
password = "kodeks"
#User-agent
headers1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
#Перевод даты в строку
strdate = datetime.strptime(current_date, '%d.%m.%Y')

#Функция добавления данных в основную таблицу БД
def Adder(line, current_date, text):
    text = str(text)
    text = text.replace("{","4443444").replace("}","333433").replace(":","221222").replace("'","112111").replace(",","000100").replace(" ","555455").replace("==","777677")
    #print(text)
    current_date = current_date.replace(".",",")
    #print(current_date)
    conn = sqlite3.connect("SUNTD.db", timeout=500)
    #SQL запрос для добавления куки
    sql = """UPDATE Bases set Cook = '""" + text + """'WHERE HostPort ='""" + line + """';
    """
    #print(sql)
    #SQL-запрос для добавления даты куки
    sql1 = """UPDATE Bases set DataCook = '""" + current_date + """'WHERE HostPort ='""" + line + """';
    """
    cursor = conn.cursor()
    #Выполнение запросов
    cursor.execute(sql)
    cursor.execute(sql1)
    #Сохранение изменений
    conn.commit() 
    conn.close()

#Функция аутенфикации на службе
def aunt(line, headers1, username, password, password1, password2):
    session = requests.Session()
    try:
        #Устанавливаем соединение с URL, используя USer-agent и проговаривая, что соединение должно отключиться
        r = session.get(line, headers = {'User-Agent': headers1, 'Connection':'close'})
        # Указываем referer. Иногда , если не указать , то приводит к ошибкам. 
        session.headers.update({'Referer':line})
        session.headers.update({'User-Agent':headers1})
        #Процесс аутенфикации на службе    
        session.auth = (username, password)
        response = session.get(line, headers = {'User-Agent': headers1, 'Connection':'close'})
        #Если соединение в норме, тогда записываем куки и закрываем соединение
        if response.ok:
            text = session.cookies.get_dict()
            response = session.close()
            return text
        else:
            #Иначе пробуем другие пароли и по аналогии ^
            try:
                session.auth = (username, password1)
                response = session.get(line, headers = {'User-Agent': headers1, 'Connection':'close'})
                if response.ok:
                    text = session.cookies.get_dict()
                    return text
            except:
                session.auth = (username, password2)
                response = session.get(line, headers = {'User-Agent': headers1, 'Connection':'close'})
                if response.ok:
                    text = session.cookies.get_dict()
                    return text
        r.close()
    except:
        text = ""
        return text
    #print(session.cookies.get_dict())

#Устанавливаем соединение с БД
conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
#Достаем все данные из основной таблицы
sqlite_select_query = """SELECT * from Bases"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
text=""
#Для каждой строки таблицы
for row in records:
    #Записываем URLку
    line = row[0]
    line4 = line.rstrip() + "/admin"
    try:
        #Считываем данные о времени и приводим их в формат даты
        timers = row[4].replace(",",".")
        timers = datetime.strptime(timers, '%d.%m.%Y')
        #Прибавляем день ко времени
        timers = timers + timedelta(days=1)
        #print(timers)
        if strdate >= timers:
            #Записываем куки сессии
            text = aunt(line4, headers1, username, password, password1, password2)
            #Добавляем данные о сессии в БД
            Adder(line, current_date, text)
    except: timers = row[4]
    if timers == None:
        #Если данные еще не были заполнены
        text = aunt(line4, headers1, username, password, password1, password2)
        Adder(line, current_date, text)
    #print(timers)
    line4 = line.rstrip() + "/admin"
    #print(text)
    
