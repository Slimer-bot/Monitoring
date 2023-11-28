import os
import requests
import urllib.request
import pandas as pd
from IPython.display import HTML
from datetime import datetime, timedelta
import sqlite3
import logging
 
current_date = datetime.now().strftime('%d.%m.%Y')
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/perezak/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")
current_date = datetime.strptime(current_date, '%d.%m.%Y')

html_string_start = '''
<html>
    <title>Мониторинг установок Техэксперт | СУНТД</title>
 <link rel="icon" href="favicon.ico" type="image/x-icon">
 <link rel="shortcut icon" href="suntd.ico" type="image/x-icon">
 <style>
    table {
        border-collapse: collapse;
        font-size: 13px;
        font-family: SegoeUI, sans-serif;
        background-color: white;
        border: 1px solid #000;
        border-radius: 5px;
        margin-top: -15px;
	margin-bottom: 20px;
    }
    
    th, td {
        padding: 6px;
        text-align: left;
        border: 1px solid #000;
        border-radius: 0;
    }
    
    .colortext {
     color: red; /* Красный цвет выделения */
    }
    
    .colortext1 {
     color: blue; /* Синий цвет выделения */
    }
    .backgroung1{
    background-color:#f19cbb;
    color: red;
    }
    th {
        border-collapse: collapse;
	background-color: #228B22;
        color: #FFFFFF;
        font-weight: normal;
	font-size: 14px;
    }
    
    tr:nth-child(even) {
        
    }

    tr:last-child td:first-child {
        border-bottom-left-radius: 5px;
    }

    tr:last-child td:last-child {
        border-bottom-right-radius: 5px;
    }
  </style>
  <body>
      <table>
      <tr><td colspan="5" style="text-align: left; font: bold 14px SegoeUI; background-color:#228B22"><a href="index1.html">Клиенты Техэксперт</a> &emsp;|&emsp; <a href="index.html">Клиенты СУНТД</a> &emsp;|&emsp; <a href="index2.html">Служебки</a> &emsp;|&emsp; <a href="index3.html">Перезаказ</a></td></tr>'
      </table>
'''
html_string_end = '''
  </body>
</html>
'''

username = "kodeks"
#username1
password1 = "skedoks"
password = "kodeks"
password2 = "skedok"
headers1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
hosts=[]
Ports=[]
dater=[]
status=[]
clients=[]
URLS=[]
reg=[]
index=0
def make_clickable(val, v):
    return f'<a target="_blank" href="{val}">{v}</a>'

def aunt(line, headers1, username, password, password1, password2, cookies):
    session = requests.Session()
    try:
        r = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})

        # Указываем referer. Иногда , если не указать , то приводит к ошибкам. 
        session.headers.update({'Referer':line})
        session.headers.update({'User-Agent':headers1})
    
        session.auth = (username, password)
        response = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
        
        
        #print(session.cookies.get_dict())
        if response.ok:
            text = response.text
            response = session.close()
            return text
        else:
            try:
                session.auth = (username, password1)
                response = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
                if response.ok:
                    text = response.text
                    return text
            except:
                session.auth = (username, password2)
                response = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
                if response.ok:
                    text = response.text
                    return text
        r.close()
        
    except:
        text = ""
        return text

conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
sqlite_select_query = """SELECT * from NewBases ORDER BY HostPort"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
logging.info("Всего строк:  " + str(len(records)))
for row in records:
    # считываем строку
    line = row[0]
    line1 = line.rstrip() + "/admin/title"
    line2 = line.rstrip() + "/admin/lic"
    line3 = line.rstrip() + "/admin/pref"
    line4 = line.rstrip() + "/admin"
    line5 = line.rstrip() + "/admin/cookies"
    try:
        strokaforcook = row[4].replace("4443444","{").replace("333433","}").replace("221222",":").replace("112111","'").replace("000100",",").replace("555455"," ").replace("777677","==")
        cookies = eval(strokaforcook)
    except:
        cookies = row[4]
    logging.info(cookies)
    index+=1
    logging.info(index)
    text = aunt(line1, headers1, username, password, password1, password2, cookies)
    text1 = aunt(line2, headers1, username, password, password1, password2, cookies)
    text2 = aunt(line3, headers1, username, password, password1, password2, cookies)
      
    URLS.append(line4)
    parts = line.split("//" and ":")
    parts[2] = parts[2].rstrip()
    Ports.append(parts[2])
    hosts.append(parts[1][2:]) 
    
    try:
        registr = text.split("Регистрационный номер: <B>" and "</B><BR>")
        registr = registr[1]
        #print(registr[38:])
        reg.append(registr[34:])
    except:
        reg.append("No reg")

    try:
        pred = text.split("\nЗарегистрирована на: <B>" and "</B><BR>")
        #print(pred[2])
        result = ""
        clientwhithoutdate = pred[2].replace('\n', '').replace('.', '').replace('B', '').replace('/', '').replace('br', '').replace('>', '').replace('<', '').replace('до ', '').replace('Зарегистрирована на: ', '').replace("Ограничение по сроку работы системы: ", "")
        for char in clientwhithoutdate[0:10]:
        # Проверяем, является ли символ цифрой
            if not char.isdigit():
            # Если символ не является цифрой, добавляем его в конечную строку
                result += char
        result += clientwhithoutdate[10:]
        #print(result)
        clients.append(result)
        
    except:
        clients.append("Нет информации")
        
    try:
        dateRab = text1.split("100001</td>")
        #print(dateRab[1][25:35])
        dater.append(dateRab[1][25:35])
        dateRab = datetime.strptime(dateRab[1][25:35], '%d.%m.%Y')
        if (current_date >= dateRab):
            status.append("Просрочена")
        else:
            dateRab = dateRab - timedelta(days=28)
            if (current_date >= dateRab):
                status.append("Перезаказ")
        
            else:
                hosts.pop()
                Ports.pop()
                URLS.pop()
                reg.pop()
                dater.pop()
                clients.pop()
        
    except:
        dater.append("No info")
        status.append("No info")

logging.info("hosts: " + str(len(hosts)) + ", {}".format(', '.join(map(str, hosts))))
logging.info("Ports: " + str(len(Ports)) + ", {}".format(', '.join(map(str, Ports))))
logging.info("dater: " + str(len(dater)) + ", {}".format(', '.join(map(str, dater))))
logging.info("status: " + str(len(status)) + ", {}".format(', '.join(map(str, status))))
logging.info("clients: " + str(len(clients)) + ", {}".format(' '.join(map(str, clients))))
logging.info("URLS: " + str(len(URLS)) + ", {}".format(', '.join(map(str, URLS))))
logging.info("reg: " + str(len(reg)) + ", {}".format(', '.join(map(str, reg))))


data = {'Reg': reg,'Host': hosts, 'Port': Ports, 'clients': clients, 'URLS': URLS}
df = pd.DataFrame.from_dict(data)
n = len(URLS)

df.style.format(make_clickable)
df['Clients'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['URLS'], x['clients']), axis=1)

df = df.drop(['clients', 'URLS'], axis=1)
df.style
df.insert(4,'Corp-Trial', dater)
df.insert(5,'Статус рега', status)


#Переводим датафрейм в html
html = df.to_html(index=False,escape=False)  
  
# write html to file 
text_file = open("index3.html", "w") 
text_file.write(html_string_start + html + html_string_end) 
text_file.close()
#Добавляем цвета к элементам
text_file = open("index3.html", "r") 
filedata = text_file.read()
filedata = filedata.replace('В норме', '<span class="colortext1">В норме')
filedata = filedata.replace('Просрочена', '<span class="colortext">Просрочена')
filedata = filedata.replace('Перезаказ', '<span class="colortext">Перезаказ')
filedata = filedata.replace('No info', '<span class="colortext1">No info')
filedata = filedata.replace('<td>No reg', '<td span class="backgroung1">No info')
filedata = filedata.replace('Нет информации', 'Браво Софт')
filedata = filedata.replace('True', '<span class="colortext1">Отсутствует')
filedata = filedata.replace('False', '<span class="colortext">ДА!')
text_file.close()
with open('index3.html', 'w') as file:
  file.write(filedata)    
