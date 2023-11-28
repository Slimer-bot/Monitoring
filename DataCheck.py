import sqlite3
import requests
import logging
from datetime import datetime, timedelta

current_date = datetime.now().strftime('%d.%m.%Y')

format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/dataCheck/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")

#Определяет функцию sqlInput, которая принимает параметры S, K, C, R и conn. Функция преобразует K, C и R в строки, выполняет SQL-запрос для замены данных в таблице NewBases с использованием переданных параметров и сохраняет изменения в базе данных.
def sqlInput(S, K, C, R, Cook, DaterC, conn):
    K = str(K)
    C = str(C)
    R = str(R)
    
    sql = """replace INTO NewBases (HostPort, Actual, Chet, SUNTD)
VALUES (?, ?, ?, ?);
        """
    cursor = conn.cursor()
    cursor.execute(sql, (S, K, C, R))
    logging.info("Запрос к БД SUNTD: " + str((sql, (S, K, C, R))))
    conn.commit() 

#Определяет функцию url_ok, которая принимает URL в качестве параметра. Функция выполняет HEAD-запрос к переданному URL и проверяет статусный код ответа. Если статусный код равен 307, 303, 200 или 302, функция возвращает True, в противном случае - False. Если возникает ошибка при выполнении запроса, функция выполняет HEAD-запрос к "https://esia.gosuslugi.ru/" и возвращает False.
def url_ok(url):
    try: r = requests.head(url)
    
    except:
        r = requests.head("https://esia.gosuslugi.ru/")
        return False
    if r.status_code  in [307, 303, 200, 302]:
        return True
    else: return False

#Устанавливает соединение с базой данных "SUNTD.db" и создает курсор для выполнения SQL-запросов
conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
#Удаляет все записи из таблицы NewBases
cursor.execute('DELETE FROM NewBases')
#Выполняет SQL-запрос для выборки всех записей из таблицы Bases.
sqlite_select_query = """SELECT * from Bases"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
logging.info("\n\n\nВсего строк:  " + str(len(records)))
#Для каждой записи выполняет проверку доступности URL с помощью функции url_ok. Если URL доступен, устанавливает значение K равным 1 и вызывает функцию sqlInput для вставки записи в таблицу NewBases с переданными параметрами. Если URL недоступен, устанавливает значение K равным 0 и вызывает функцию sqlInput для вставки записи в таблицу NewBases с переданными параметрами.
for row in records:
    D = url_ok(row[0])
    if D == True:
        K = 1
        sqlInput(row[0], K, row[1], row[2], row[3], row[4], conn)
    else:
        K = 0
        sqlInput(row[0], K, row[1], row[2], row[3], row[4], conn)

#Закрывает курсор, сохраняет изменения в базе данных и закрывает соединение с базой данных.
cursor.close()
conn.commit() 
conn.close()
