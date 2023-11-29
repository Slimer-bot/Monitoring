import requests
import os
import signal
import time
import sqlite3
import logging
from datetime import datetime, timedelta


#Задание формата логов
current_date = datetime.now().strftime('%d.%m.%Y')
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/Check/logs" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")

#cursor.execute('DELETE FROM NewBases')
def sqlInput(S, K):
    K = str(K)
    conn = sqlite3.connect("SUNTD.db", timeout=500)
    
    sql = """INSERT OR IGNORE INTO  Bases (HostPort, Chet, SUNTD)
VALUES ('""" + S + """', 0, """ + K + """);
        """
    logging.info("Запрос к БД SUNTD: " + sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit() 
    conn.close()

def url_ok(url):
    try:
        r = requests.head(url)
    except:
        r = requests.head("https://esia.gosuslugi.ru/")
        return False
    if r.status_code == (307 or 303 or 200 or 302):
        logging.info("URL: " + url + " congr")
        return True
    else: return False
    
SUNTDstr = []
SUNTDstr.append("http://suntd:4040")
SUNTDstr.append("http://suntd:4545")
SUNTDstr.append("http://suntd:5555")
SUNTDstr.append("http://suntd:5566")
SUNTDstr.append("http://suntd:5577")
SUNTDstr.append("http://suntd:7000")
SUNTDstr.append("http://suntd:7788")
SUNTDstr.append("http://suntd:8000")
SUNTDstr.append("http://suntd:8088")
SUNTDstr.append("http://suntd:8874")
SUNTDstr.append("http://suntd:9000")
SUNTDstr.append("http://suntd:41197")
SUNTDstr.append("http://suntd:80")
SUNTDstr.append("http://dream:3456")

for i in range (0, len(SUNTDstr)):
    D = url_ok(SUNTDstr[i])
    if D == True:
        #print("uma")
        K = 1
        sqlInput(SUNTDstr[i], K)


S=[]
S.append("http://REX:1000")
S.append("http://REX:80")
S.append("http://REX:4000")



for i in range (0, len(S)):
    D = url_ok(S[i])
    if D == True:
        K = 0
        sqlInput(S[i], K)

SC=[]
SC.append("http://95.79.112.201:80")
SC.append("http://95.79.112.202:80")
SC.append("http://95.79.112.203:80")
SC.append("http://95.79.112.204:80")
SC.append("http://95.79.59.227:80")
SC.append("http://91.219.56.146:80")
SC.append("http://95.79.102.106:80")

for i in range (0, len(SC)):
    D = url_ok(SC[i])
    if D == True:
        K = 0
        sqlInput(SC[i], K)
          
step = 10
i = 1000
t = 0

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
        
    #print(i)
    if (t == 0):
        step = int(i_str) * 1010
        if (step == 8080):
            t = 3
        elif (step == 9090):
            t = 3
        else:
            t = 1
            
    elif (t == 1):
        step = int(i_str) * 1100
        if (step == 8800):
            t = 4
        elif step == 9900:
            t = 4
        else:
            t = 2
            
    elif (t == 3):
        step = i + 1
        if (step == (8089 or 9099)):
            t = 1
        elif step == 8889:
            t = 2
        elif step == 9099:
            t = 1
        else:
            t = 3

    elif (t == 4):
        if i == 8800:
            step = 8880
            t = 3
        else:
            step = 9990
            t = 3
        
    else:
        i_str = int(i_str) + 1
        step = i_str * 1000
        t = 0

    if url_ok(first) == True:
        sqlInput(first, K)
        
        
    if url_ok(second) == True:
        sqlInput(second, K)

    if url_ok(third) == True:
        sqlInput(third, K)
        
    if url_ok(forth) == True:
        sqlInput(forth, K)

    if url_ok(fifth) == True:
        sqlInput(fifth, K)

    if url_ok(sixth) == True:
        sqlInput(sixth, K)
        #print("congr")
    #print(sixth)
    if url_ok(seventh) == True:
        sqlInput(seventh, K)
      
    i = step
    

        
for i in range(1210, 1220):
    L = 1
    S = "http://suntd:" + str(i)
    K = "http://dream:" + str(i)
    if url_ok(S) == True:
        sqlInput(S, L)
    if url_ok(K) == True:
        sqlInput(K, L)

