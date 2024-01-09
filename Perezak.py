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
<!DOCTYPE html>
<html lang="ru">
<head>
<title>Мониторинг установок Техэксперт | СУНТД</title>
<link rel="icon" href="suntd.ico" type="image/x-icon">
<link rel="shortcut icon" href="suntd.ico" type="image/x-icon">
<link rel="stylesheet" href="CSS/style.css"> 
</head>
<div class="sticky" align="center">
      <a href="index0.html"><img src="CSS/img/ico/bravo_soft.ico" height="50" /> </a>&emsp;|&emsp; <a href="index1.html">Клиенты Техэксперт</a> &emsp;|&emsp; <a href="index.html">Клиенты СУНТД</a> &emsp;|&emsp; <a href="index2.html">Служебки</a> &emsp;|&emsp; <a href="index3.html">Смена рега</a> &emsp;|&emsp; <a href="output.xlsx">Скачать</a><div class="NewYear">С наступающим Новым 2024 годом!!!&emsp;&emsp;<img src="CSS/img/ico/elka.png" height="50" /></div>
</div>
'''
html_string_end = '''
<script src="js/snowstorm-min.js"></script>

<script>

	window.onload = function() {

		snowStorm.snowColor = "#fff"; // Цвет снежинок
		snowStorm.flakesMaxActive = 100; // Максимальное количество видимых снежинок
		snowStorm.followMouse = true; // true - гоняться за курсором, false - нет
		snowStorm.snowCharacter = "&bull;"; // Вид снежинки

	};

</script>
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
#Дата рега
dater1=[]

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
                else:
                    session.auth = (username, password2)
                    response = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
                    if response.ok:
                        text = response.text
                        return text
            
            except:
                text = ""
                return text
                
        r.close()
        
    except:
        text = ""
        return text

conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
sqlite_select_query = """SELECT * from NewBases Where Actual = 1 ORDER BY HostPort"""
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
        clientwhithoutdate = pred[2].replace('\n', '').replace('&quot;', '').replace('.', '').replace('B', '').replace('/', '').replace('br', '').replace('>', '').replace('<', '').replace('до ', '').replace('Зарегистрирована на: ', '').replace("Ограничение по сроку работы системы: ", "")
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
        try:
            pred = text.split("\nЗарегистрирована на: <B>" and "</B><BR>")
            #print(pred[2])
            result = ""
            clientwhithoutdate = pred[2].replace('до', '').replace('B', '').replace('\n', '').replace('br', '').replace('>', '').replace('<', '').replace("Ограничение по сроку работы системы: ", "").replace(' ', '')
            result += clientwhithoutdate[0:10]
            #print(result)
            dater1.append(result)
            try:
                result = datetime.strptime(result, '%d.%m.%Y')
                #print(result)
            except:
                result = dateRab
        except:
            dater1.append("No info")
        if (current_date >= dateRab or current_date >= result):
            status.append("Просрочена")
            #print(dateRab)
        else:
            dateRab = dateRab - timedelta(days=28)
            result = result - timedelta(days=28)
            if (current_date >= dateRab or current_date >= result):
                status.append("Перезаказ")
        
            else:
                
                hosts.pop()
                Ports.pop()
                URLS.pop()
                reg.pop()
                dater.pop()
                clients.pop()
                dater1.pop()
    except:
        dater.append("No info")
        status.append("No info")

for i in range(len(dater1)):
 
    # replace hardik with shardul
    if dater1[i] == 'Зарегистри':
        dater1[i] = 'Без срока'

logging.info("hosts: " + str(len(hosts)) + ", {}".format(', '.join(map(str, hosts))))
logging.info("Ports: " + str(len(Ports)) + ", {}".format(', '.join(map(str, Ports))))
logging.info("dater: " + str(len(dater)) + ", {}".format(', '.join(map(str, dater))))
logging.info("dater1: " + str(len(dater1)) + ", {}".format(', '.join(map(str, dater1))))
logging.info("status: " + str(len(status)) + ", {}".format(', '.join(map(str, status))))
logging.info("clients: " + str(len(clients)) + ", {}".format(' '.join(map(str, clients))))
logging.info("URLS: " + str(len(URLS)) + ", {}".format(', '.join(map(str, URLS))))
logging.info("reg: " + str(len(reg)) + ", {}".format(', '.join(map(str, reg))))
#Удаляем лишние данные из списков, если есть
while len(dater) > len(hosts):
    dater.pop()
    logging.info("dater удален")
while len(dater1) > len(hosts):
    dater1.pop()
    logging.info("dater1 удален")
while len(status) > len(hosts):
    status.pop()
    logging.info("status удален")

    
data = {'Reg': reg,'Host': hosts, 'Port': Ports, 'clients': clients, 'URLS': URLS, 'Corp-Trial': dater, 'Срок службы': dater1, 'Статус рега': status}
df = pd.DataFrame.from_dict(data)
#n = len(URLS)
df1 = df.copy()
df1 = df1.drop(['URLS', 'Статус рега'], axis=1)
with pd.ExcelWriter('output.xlsx',
                    mode='w') as writer:  
    df1.to_excel(writer, sheet_name='Перезаказ', index=False)

df.style.format(make_clickable)
df['Clients'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['URLS'], x['clients']), axis=1)
df = df.drop(['clients', 'URLS'], axis=1)
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
filedata = filedata.replace('table border="1" class="dataframe"', 'table')
filedata = filedata.replace('<tr style="text-align: right;">', '<tr class="sticky1">')
filedata = filedata.replace('Без срока', '<span class="colortext1">Без срока')
text_file.close()
with open('index3.html', 'w') as file:
  file.write(filedata)    
 
