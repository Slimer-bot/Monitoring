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
logging.basicConfig(filename = "logs/Script2/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")
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
    .colortext2 {
     color: black; 
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
stat=[]
clients=[]
URLS=[]
sysinfoURL=[]
PolzURLS = []
#Пользователи
polz=[]
#Рез.копия
rez=[]
#Перезапуск
perezap=[]
#Привязка
privyaz=[]
#Рег
reg=[]
#Remarks
error=[]
#Ошибка
blat=[]
    
def make_clickable(val, v):
    return f'<a target="_blank" href="{val}">{v}</a>'

def IsError(url):
    try: r = requests.head(url)
    except:
        r.status_code = (300)
    if r.status_code == (200):
        return True
    else: return False

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
sqlite_select_query = """SELECT * from NewBases WHERE SUNTD = 0 ORDER BY HostPort"""
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
    line6 = line.rstrip() + "/sysinfo/metrics"
    try:
        strokaforcook = row[4].replace("4443444","{").replace("333433","}").replace("221222",":").replace("112111","'").replace("000100",",").replace("555455"," ").replace("777677","==")
        cookies = eval(strokaforcook)
    except:
        cookies = row[4]
    logging.info(cookies)
    text = aunt(line1, headers1, username, password, password1, password2, cookies)
    text1 = aunt(line2, headers1, username, password, password1, password2, cookies)
    text2 = aunt(line3, headers1, username, password, password1, password2, cookies)
    text3 = aunt(line6, headers1, username, password, password1, password2, cookies)

    #выводим строки
    parts = line.split("//" and ":")
    sysinfo = line.rstrip() + "/sysinfo/si_save_request"    
    parts[2] = parts[2].rstrip()
    Ports.append(parts[2])
    #print(line)

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
        privazka = text1.split("</H3></CENTER><BR> Привязка:")
        sep = "<br>"
        privazka = privazka[1].split(sep, 1)[0]
        privazka = privazka.strip(' ')
        #print(privazka)
        privyaz.append(privazka)
    except:
        privyaz.append("No info")

    try:
        rezerv = text2.split("""<INPUT TYPE="TEXT" NAME="reservtime" VALUE=""")
        rezerv = rezerv[1]
        rezerv = rezerv[1:6]
        #print(rezerv.replace('"', ''))
        rez.append(rezerv.replace('"', ''))
    except:
        rez.append("No info")

    try:
        perezapusk = text2.split("""<INPUT TYPE="TEXT" NAME="restarttime" VALUE=""")
        perezapusk = perezapusk[1]
        perezapusk = perezapusk[1:6]
        #print(perezapusk.replace('"', ''))
        perezap.append(perezapusk.replace('"', ''))
    except:
        perezap.append("No info")

    try:
        polzovat = text.split("Пользователи работающие с продуктами")
        polzovat1 = text.split("Пользователи работающие с продуктами (стандартные, расширенные лицензии):")
        polzovat = polzovat[1]
        polzovat1 = polzovat1[1]
        polzovat = polzovat[22:-6] + "/" + polzovat1[30:35]
        polzovat = polzovat.replace(':', '').replace(' ', '').replace(')', '').replace('<', '').replace('b', '').replace('a', '').replace('а', '')
        #print(polzovat)
        polz.append(polzovat)
        PolzURLS.append(line5)
    except:
        polz.append("No info")
        PolzURLS.append(line5)

    try:
        lines=[]
        lines=text3.split('\n')
        long = len(lines)
        string = ""
        for i in lines:
            if 'kserver_main_page{service="kodweb",path=' in i:
                string += i.replace('kserver_', '').replace('status="update DB"', 'Обновление/подключение БД').replace('main_page', 'Главная страница').replace('{service="kodweb",path=', ' ').replace('"', '').replace('}', '').replace('0', 'Ошибки нет').replace('1','Ошибка ') + "\n"
            if 'kserver_product_control{service="kodweb",path=' in i:
                string += i.replace('kserver_', '').replace('product_control', 'Наличие предупреждения').replace('{service="kodweb",path=', ' ').replace('"', '').replace('}', '').replace('0', 'Ошибки нет').replace('1','Необходимо проверить состав БД') + "\n"
        #print(string)
        blat.append(string.replace('\n', '<br>'))
    except:
        blat.append("No info")
    
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
                status.append("В норме")
        
    except:
        dater.append("No info")
        status.append("No info")
    hosts.append(parts[1][2:])
    stat.append(sysinfo)        
    URLS.append(line4)
    sysinfoURL.append(sysinfo)
    error.append(IsError(line.rstrip() + "/.apiDocInfo?nd=1200159302&authMode=system&source=kassist"))

# закрываем файл
cursor.close()
conn.close()

logging.info("hosts: " + str(len(hosts)) + ", {}".format(', '.join(map(str, hosts))))
logging.info("Ports: " + str(len(Ports)) + ", {}".format(', '.join(map(str, Ports))))
logging.info("dater: " + str(len(dater)) + ", {}".format(', '.join(map(str, dater))))
logging.info("status: " + str(len(status)) + ", {}".format(', '.join(map(str, status))))
logging.info("stat: " + str(len(stat)) + ", {}".format(', '.join(map(str, stat))))
logging.info("clients: " + str(len(clients)) + ", {}".format(' '.join(map(str, clients))))
logging.info("URLS: " + str(len(URLS)) + ", {}".format(', '.join(map(str, URLS))))
logging.info("sysinfoURL: " + str(len(sysinfoURL)) + ", {}".format(', '.join(map(str, sysinfoURL))))
logging.info("PolzURLS: " + str(len(PolzURLS)) + ", {}".format(', '.join(map(str, PolzURLS))))
logging.info("polz: " + str(len(polz)) + ", {}".format(', '.join(map(str, polz))))
logging.info("perezap: " + str(len(perezap)) + ", {}".format(', '.join(map(str, perezap))))
logging.info("privyaz: " + str(len(privyaz)) + ", {}".format(', '.join(map(str, privyaz))))
logging.info("error: " + str(len(error)) + ", {}".format(', '.join(map(str, error))))
logging.info("reg: " + str(len(reg)) + ", {}".format(', '.join(map(str, reg))))
logging.info("blat: " + str(len(blat)) + ", {}".format(', '.join(map(str, blat))))

data = {'Reg': reg,'Host': hosts, 'Port': Ports, 'clients': clients, 'URLS': URLS,'active/Pos': polz, 'PolzURLS': PolzURLS, 'Sysinfo': "Скачать", 'sysinfoURL': sysinfoURL}
df = pd.DataFrame.from_dict(data)
n = len(URLS)

df.style.format(make_clickable)
df['Clients'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['URLS'], x['clients']), axis=1)
df['Active/Pos'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['PolzURLS'], x['active/Pos']), axis=1)
df['SysInfo'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['sysinfoURL'], x['Sysinfo']), axis=1)

df = df.drop(['clients', 'URLS', 'Sysinfo', 'sysinfoURL', 'active/Pos', 'PolzURLS'], axis=1)
df.style
df.insert(4,'Corp-Trial', dater)
df.insert(5,'Статус рега', status)

df.insert(7,'Перезапуск', perezap)
df.insert(8,'Рез. копия', rez)
df.insert(9,'Привязка', privyaz)
df.insert(10,'Ошибки системы', blat)

#Переводим датафрейм в html
html = df.to_html(index=False,escape=False)  
  
# write html to file 
text_file = open("index1.html", "w") 
text_file.write(html_string_start + html + html_string_end) 
text_file.close()
#Добавляем цвета к элементам
text_file = open("index1.html", "r") 
filedata = text_file.read()
filedata = filedata.replace('В норме', '<span class="colortext1">В норме')
filedata = filedata.replace('Просрочена', '<span class="colortext">Просрочена')
filedata = filedata.replace('Перезаказ', '<span class="colortext">Перезаказ')
filedata = filedata.replace('No info', '<span class="colortext1">No info')
filedata = filedata.replace('<td>No reg', '<td span class="backgroung1">No info')
filedata = filedata.replace('Нет информации', 'Браво Софт')
filedata = filedata.replace('Ошибка', '<span class="colortext">"Ошибка"<span class="colortext2">')
filedata = filedata.replace('Необходимо проверить состав БД', '<span class="colortext">Необходимо проверить состав БД<span class="colortext2">')
filedata = filedata.replace('status=unexpected change list products', '<span class="colortext">Изменился состав продуктов')
filedata = filedata.replace('status=no required volume DB', '<span class="colortext">Не подключены обязательные тома БД')

text_file.close()
with open('index1.html', 'w') as file:
  file.write(filedata)

#df.to_html('index.html', justify='center', border=3, escape=False, classes='table table-striped')
