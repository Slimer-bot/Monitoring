import os
import requests
import urllib.request
import pandas as pd
from IPython.display import HTML
from datetime import datetime, timedelta
import sqlite3
 
current_date = datetime.now().strftime('%d.%m.%Y')
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
      <tr><td colspan="5" style="text-align: left; font: bold 14px SegoeUI;"><a href="index1.html">Клиенты Техэксперт</a> &emsp;|&emsp; <a href="index.html">Клиенты СУНТД</a> &emsp;|&emsp; <a href="index2.html">Служебки</a></td></tr>'
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

#def LoadInfo():
    
def make_clickable(val, v):
    return f'<a target="_blank" href="{val}">{v}</a>'

def IsError(url):
    try: r = requests.head(url)
    except:
        r.status_code = (300)
    if r.status_code == (200):
        return True
    else: return False

def aunt(line, headers1, username, password, password1):
    session = requests.Session()
    try:
        r = session.get(line, headers = {'User-Agent': headers1})

        # Указываем referer. Иногда , если не указать , то приводит к ошибкам. 
        session.headers.update({'Referer':line})
        session.headers.update({'User-Agent':headers1})
    
        session.auth = (username, password)
        response = session.get(line)
        if response.ok:
            text = response.text
            return text
        else:
            session.auth = (username, password1)
            response = session.get(line)
            if response.ok:
                text = response.text
                return text
    except:
        text = ""
        return text


conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
sqlite_select_query = """SELECT * from NewBases WHERE SUNTD = 0 ORDER BY HostPort"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
print("Всего строк:  ", len(records))
for row in records:
    # считываем строку
    line = row[0]
    line1 = line.rstrip() + "/admin/title"
    line2 = line.rstrip() + "/admin/lic"
    line3 = line.rstrip() + "/admin/pref"
    line4 = line.rstrip() + "/admin"
    line5 = line.rstrip() + "/admin/cookies"
    text = aunt(line1, headers1, username, password, password1)
    text1 = aunt(line2, headers1, username, password, password1)
    text2 = aunt(line3, headers1, username, password, password1)

    # выводим строки
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
        pred = text.split("Зарегистрирована на: <B>" and "&quot;" and "&quot;")
        #print(pred[3])
        clients.append(pred[3])
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

#n=10
#del clients[-n:]
#clients.extend(["Кодекс", "Техэксперт", "Портал Браво Софт (Техэксперт)", "Техэксперт SMART", "Горячая линия Браво Софт", "Портал Браво Софт (Кодекс)", "Менеджер лицензий", "Для скачивания с http | base3.kodeks.expert", 'Для скачивания с http', 'Менеджер лицензий'])
#print(clients)#del dater[-n:]

#print(len(clients))
#print(len(hosts))
#print(len(Ports))
#print(len(dater))
#print(len(status))
#print(len(URLS))
#print(len(sysinfoURL))


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
df.insert(10,'Ошибка', error)

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
filedata = filedata.replace('True', '<span class="colortext1">Отсутствует')
filedata = filedata.replace('False', '<span class="colortext">ДА!')
text_file.close()
with open('index1.html', 'w') as file:
  file.write(filedata)

#df.to_html('index.html', justify='center', border=3, escape=False, classes='table table-striped')
