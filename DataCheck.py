import sqlite3
import requests
import os
import logging
from datetime import datetime, timedelta

current_date = datetime.now().strftime('%d.%m.%Y')

format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/dataCheck/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")


def sqlInput(S, K, C, R, conn):
    K = str(K)
    C = str(C)
    R = str(R)
    sql = """replace INTO NewBases (HostPort, Actual, Chet, SUNTD)
VALUES ('""" + S + """',""" + K +  """,""" + C +  """,""" + R +  """);
        """
    logging.info("Запрос к БД SUNTD: " + sql)
    #print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit() 


def url_ok(url):
    try: r = requests.head(url)
    except:
        r = requests.head("https://esia.gosuslugi.ru/")
        return False
    if r.status_code == (307 or 303 or 200 or 302):
        return True
    else: return False


conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
cursor.execute('DELETE FROM NewBases')
sqlite_select_query = """SELECT * from Bases"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
logging.info("\n\n\nВсего строк:  " + str(len(records)))
for row in records:
    D = url_ok(row[0])
    if D == True:
        K = 1
        sqlInput(row[0], K, row[1], row[2], conn)
    else:
        K = 0
        sqlInput(row[0], K, row[1], row[2], conn)


cursor.close()
conn.commit() 
conn.close()





