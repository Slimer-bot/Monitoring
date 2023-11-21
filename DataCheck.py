import sqlite3
import requests
import os


#def sort():
    #sqlzap = "SELECT * FROM NewBases ORDER BY HostPort"
    #cursor = conn.cursor()
    #cursor.execute(sqlzap)
    #conn.commit()
    #c = "Сортировка произведена"
    #return c

def sqlInput(S, K, C, R, conn):
    K = str(K)
    C = str(C)
    R = str(R)
    sql = """replace INTO NewBases (HostPort, Actual, Chet, SUNTD)
VALUES ('""" + S + """',""" + K +  """,""" + C +  """,""" + R +  """);
        """
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
print("Всего строк:  ", len(records))
for row in records:
    D = url_ok(row[0])
    if D == True:
        K = 1
        sqlInput(row[0], K, row[1], row[2], conn)
    else:
        K = 0
        sqlInput(row[0], K, row[1], row[2], conn)
#print(sort())
cursor.close()
conn.commit() 
conn.close()





