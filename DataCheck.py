import sqlite3
import requests
import logging
from datetime import datetime, timedelta

#Текущая дата и время
current_date = datetime.now().strftime('%d.%m.%Y')
#Формат логов
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/dataCheck/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")

#Функция замены данных в таблице с актуальными базами
def sqlInput(S, K, C, R, Cook, DaterC, conn):
    K = str(K)
    C = str(C)
    R = str(R)
    #SQL запрос к таблице
    sql = """replace INTO NewBases (HostPort, Actual, Chet, SUNTD, Cook, DataCook)
VALUES ('""" + S + """',""" + K +  """,'""" + C +  """',""" + R +  """, '""" + Cook + """', '""" + DaterC + """');
        """
    logging.info("Запрос к БД SUNTD: " + sql)
    #print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit() 

#Функция проверки получаемого кода от URL
def url_ok(url):
    try: r = requests.head(url)

    except:
        r = requests.head("https://www.google.com")
        return False
    if r.status_code == (307 or 303 or 200 or 302):
        return True
    else: return False

#Подключение к БД
conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
#Выборка всех данных из основной таблицы БД
sqlite_select_query = """SELECT * from Bases"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
#Запись общего количества строк в основной таблице
logging.info("\n\n\nВсего строк:  " + str(len(records)))
#Для каждой строки в записях таблицы
for row in records:
    #Проверяем URL. Если активна, то записываем в таблицу, что Actual = 1, 0 - не активна
    D = url_ok(row[0])
    if D == True:
        K = 1
        sqlInput(row[0], K, row[1], row[2], row[3], row[4], conn)
    else:
        K = 0
        sqlInput(row[0], K, row[1], row[2], row[3], row[4], conn)

#Закрываем соединение с БД и сохраняем изменения
cursor.close()
conn.commit() 
conn.close()
