import requests
import os
import signal
import time
import sqlite3

# ‘ункци€ дл€ вставки данных в базу данных SQLite
def sqlInput(S, K):
    K = str(K)
    conn = sqlite3.connect("SUNTD.db", timeout=500)

    sql = """replace INTO Bases (HostPort, Chet, SUNTD)
VALUES ('""" + S + """', 0, """ + K + """);
        """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

# ‘ункци€ дл€ проверки доступности URL
def url_ok(url):
    try:
        r = requests.head(url)
    except:
        r = requests.head("https://esia.gosuslugi.ru/")
        return False
    if r.status_code == (307 or 303 or 200 or 302):
        print("congr")
        return True
    else:
        return False

# —писок URL-адресов дл€ проверки
SUNTDstr = [
    "http://suntd:4040",
    "http://suntd:4545",
    "http://suntd:5555",
    "http://suntd:5566",
    "http://suntd:5577",
    "http://suntd:7000",
    "http://suntd:7788",
    "http://suntd:8000",
    "http://suntd:8088",
    "http://suntd:8874",
    "http://suntd:9000",
    "http://suntd:41197",
    "http://suntd:80",
    "http://dream:3456"
]

# ѕроверка доступности URL-адресов и вставка данных в базу данных SQLite
for url in SUNTDstr:
    if url_ok(url):
        sqlInput(url, 1)

# —писок URL-адресов дл€ проверки
S = [
    "http://REX:1000",
    "http://REX:80",
    "http://REX:4000"
]

# ѕроверка доступности URL-адресов и вставка данных в базу данных SQLite
for url in S:
    if url_ok(url):
        sqlInput(url, 1)

# —писок URL-адресов дл€ проверки
SC = [
    "http://95.79.112.201:80",
    "http://95.79.112.202:80",
    "http://95.79.112.203:80",
    "http://95.79.112.204:80",
    "http://95.79.59.227:80"
]

# ѕроверка доступности URL-адресов и вставка данных в базу данных SQLite
for url in SC:
    if url_ok(url):
        sqlInput(url, 0)

step = 10
i = 1000
t = 0

# ÷икл дл€ проверки доступности URL-адресов и вставки данных в базу данных SQLite
while i < 10000:
    i_str = str(i)
    i_str = i_str[0]
    first = "http://95.79.112.201:" + str(i)
    second = "http://95.79.112.202:" + str(i)
    third = "http://95.79.112.203:" + str(i)
    forth = "http://95.79.112.204:" + str(i)
    fifth = "http://95.79.59.227:" + str(i)
    sixth = "http://91.219.56.146:" + str(i)
    seventh = "http://95.79.102.106:" + str(i)
    K = 0

    if t == 0:
        step = int(i_str) * 1010
        if step == 8080 or step == 9090:
            t = 3
        else:
            t = 1

    elif t == 1:
        step = int(i_str) * 1100
        if step == 8800 or step == 9900:
            t = 4
        else:
            t = 2

    elif t == 3:
        step = i + 1
        if step == (8089 or 9099):
            t = 1
        elif step == 8889:
            t = 2
        elif step == 9099:
            t = 1
        else:
            t = 3

    elif t == 4:
        if i == 8800:
            step = 8880
            t = 3
        else:
            step = 9990
            t = 3

    else:
        i_str = int(i_str) + 1
        step = int(i_str) * 1000
        t = 0

    # ѕроверка доступности URL-адресов и вставка данных в базу данных SQLite
    if url_ok(first):
        sqlInput(first, K)

    if url_ok(second):
        sqlInput(second, K)

    if url_ok(third):
        sqlInput(third, K)

    if url_ok(forth):
        sqlInput(forth, K)

    if url_ok(fifth):
        sqlInput(fifth, K)

    if url_ok(sixth):
        sqlInput(sixth, K)

    if url_ok(seventh):
        sqlInput(seventh, K)

    i = step

for i in range(1210, 1220):
    L = 1
    S = "http://suntd:" + str(i)
    K = "http://dream:" + str(i)
    if url_ok(S):
        sqlInput(S, L)
    if url_ok(K):
        sqlInput(K, L)