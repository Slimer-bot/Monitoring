import os
import requests
import urllib.request
import pandas as pd
from IPython.display import HTML
from datetime import datetime, timedelta
import sqlite3
import logging
import gc
import smtplib
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.image import MIMEImage              # Изображения
from email.header    import Header

current_date = datetime.now().strftime('%d.%m.%Y')
actualdate = current_date
addr_from = "o.zadonskiy@teh.expert"                # Адресат
addr_to   = "olegan.zadonskiy1@gmail.com"         # Получатель
passwordMail  = "E6JCSx5uxK6KFEtukv7N" 

substr = "status=unexpected change list products"
substr1 = "status=no required volume DB"
substr2 = "Необходимо проверить состав БД"

#Формат логов
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/Script/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")
current_date = datetime.strptime(current_date, '%d.%m.%Y')


html_string_start = '''
<!DOCTYPE html>
<html lang="ru">
<head><title>Мониторинг установок Техэксперт | СУНТД</title>
<link rel="icon" href="suntd.ico" type="image/x-icon">
<link rel="shortcut icon" href="suntd.ico" type="image/x-icon">
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/sweetalert2@7.12.15/dist/sweetalert2.min.css'>
<link rel="stylesheet" href="CSS/style.css"> 
</head>
<body>
    <div class="sticky" align="center">
    <a href="index0.html"><img src="CSS/img/ico/bravo_soft.ico" height="50" /> </a>&emsp;|&emsp; <a href="index1.html">Клиенты Техэксперт</a> &emsp;|&emsp; <a href="index.html">Клиенты СУНТД</a> &emsp;|&emsp; <a href="index2.html">Служебки</a> &emsp;|&emsp; <a href="index3.html">Смена рега</a>&emsp;|&emsp;<a href="index4.html">Смена рега СУНТД</a><div class="NewYear">С наступающим Новым 2024 годом!!!&emsp;&emsp;<img src="CSS/img/ico/elka.png" height="50" /></div>
    </div>
'''
html_string_end = '''
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@7.12.15/dist/sweetalert2.all.min.js"></script>
<script src="js/script.js"></script>
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
password2 = "skedok"
password = "kodeks"
headers1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
#неактивные установки
Inactivity = 0
#Все возможные установки
Allposactivity = 0

#Рег
reg=[]
#Хост
hosts=[]
#Порт
Ports=[]
#Срок действия лицензии
dater=[]
status=[]
stat=[]
#Клиент (наименование)
clients=[]
#Ссылки
URLS=[]
#Ссылки на Sysinfo
sysinfoURL=[]
#Ссылка на пользовательские сессии
PolzURLS = []
#Пользователи
polz=[]
#Рез.копия
rez=[]
#Перезапуск
perezap=[]
#Привязка
privyaz=[]
#Ошибка
blat=[]
#Дата рега
dater1=[]

def mailer(addr_from, passwordMail, addr_to, message):
    try:
        msg = MIMEText(message.encode('utf-8'), 'plain', 'utf-8')                               # Создаем сообщение
        msg['From']    = addr_from                          # Адресат
        msg['To']      = addr_to                            # Получатель
        msg['Subject'] = Header('Отчет об ошибке', 'utf-8')  
        server = smtplib.SMTP('smtp.mail.ntci.nnov.ru', 587)           # Создаем объект SMTP
        #server.set_debuglevel(1)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
        server.starttls()                                   # Начинаем шифрованный обмен по TLS
        server.login(addr_from, passwordMail)                   # Получаем доступ
        server.sendmail(msg['From'], addr_to, msg.as_string())                          # Отправляем сообщение
        server.quit()
        print('Email sent!')
    except:
        print('Something went wrong...')    

def make_clickable(val, v):
    return f'<a target="_blank" href="{val}">{v}</a>'

def Adder(line, current_date):
    current_date = str(current_date).replace(".",",")
    print(current_date)
    conn = sqlite3.connect("SUNTD.db", timeout=500)
    
    sql1 = """UPDATE Bases set Chet = '""" + current_date + """'WHERE HostPort ='""" + line + """';
    """
    #print(sql1)
    cursor = conn.cursor()
    cursor.execute(sql1)
    conn.commit() 
    conn.close()

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
sqlite_select_query = """SELECT * from NewBases WHERE SUNTD = 1 and Actual = 1 ORDER BY HostPort"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
Allposactivity = len(records)
for row in records:
    # считываем строку
    line = row[0]
    line1 = line.rstrip() + "/admin/title"
    line2 = line.rstrip() + "/admin/lic"
    line3 = line.rstrip() + "/admin/pref"
    line4 = line.rstrip() + "/admin"
    line5 = line.rstrip() + "/admin/cookies"
    line6 = line.rstrip() + "/sysinfo/metrics"

    mail = row[1]
    #print(row[4])
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
    #print(text1)
    
    # выводим строки
    
    parts = line.split("//" and ":")
    sysinfo = line.rstrip() + "/sysinfo/si_save_request"    
    parts[2] = parts[2].rstrip()
    Ports.append(parts[2])
    hosts.append(parts[1][2:])
    stat.append(sysinfo)
    #print(text)
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
        
        dateRab = text1.split("100001</td>")
        #print(dateRab[1][25:35])
        dater.append(dateRab[1][25:35])
        dateRab = datetime.strptime(dateRab[1][25:35], '%d.%m.%Y')
        #print(dateRab)
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
                status.append("В норме")
    except:
        dater.append("No info")
        status.append("No info")
        

    try:
        lines=[]
        lines=text3.split('\n')
        long = len(lines)
        string = ""
        for i in lines:
            if 'kserver_main_page{service="kodweb",path=' in i:
                string += i.replace('kserver_', '').replace('status="update DB"', 'Обновление/подключение БД').replace('main_page', '\nГлавная страница').replace('{service="kodweb",path=', ' ').replace('"', '').replace('}', '').replace(' 0', ' Ошибки нет').replace(' 1',' Ошибка ') + "\n"
            if 'kserver_product_control{service="kodweb",path=' in i:
                string += i.replace('kserver_', '').replace('product_control', '\nНаличие предупреждения').replace('{service="kodweb",path=', ' ').replace('"', '').replace('}', '').replace(' 0', ' Ошибки нет').replace(' 1',' Необходимо проверить состав БД') + "\n"
        #print(string)
        blat.append(string.replace('\n', '<br>'))
        
    except:
        blat.append("No info")
        string = ""

    if (substr in string) or (substr1 in string) or (substr2 in string):
        #print("Error")
        message = "На Службе: " + line + " выявлены следующие ошибки:\n" + string
        try:
            
            timers = mail.replace(",",".")
            #print(timers)
            timers = datetime.strptime(timers, '%d.%m.%Y')
            timers = timers + timedelta(days=1)
            #print(timers)
            if current_date >= timers:
                Adder(line, actualdate)
                
                mailer(addr_from, passwordMail, addr_to, message)
        except: timers = mail
        if timers == "0":
            Adder(line, actualdate)
            mailer(addr_from, passwordMail, addr_to, message)
    
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

    URLS.append(line4)
    sysinfoURL.append(sysinfo)
    del text, text1, text2, text3
#Закрываем файл
cursor.close()
conn.close()

conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
sqlite_select_query = """SELECT * from NewBases WHERE SUNTD = 1 and Actual = 0 ORDER BY HostPort"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
Allposactivity += len(records)
Allposactivity = str(Allposactivity)
logging.info("Всего строк:  " + Allposactivity)
for row in records:
    line = row[0]
    line4 = line.rstrip() + "/admin"
    Inactivity += 1
    parts = line.split("//" and ":")
    sysinfo = line.rstrip() + "/sysinfo/si_save_request"    
    parts[2] = parts[2].rstrip()
    
    Ports.append(parts[2])
    hosts.append(parts[1][2:])
    stat.append(sysinfo)
    URLS.append(line4)
    sysinfoURL.append(sysinfo)

    reg.append("No reg")
    rez.append("No info")
    polz.append("No info")
    perezap.append("No info")
    blat.append("No info")
    dater.append("No info")
    dater1.append("No info")
    status.append("No info")
    clients.append("Нет информации")
    privyaz.append("No info")
    PolzURLS.append("No info")
cursor.close()
conn.close()


for i in range(len(blat)):
    if (substr in blat[i]) or (substr1 in blat[i]) or (substr2 in blat[i]):
        blat[i] = """<button class="button-48" value='""" + blat[i].replace('Ошибка', ' ') + """'  type="button" onclick='f1(this)'><span class="text">Ошибка!!!<br>Подробнее</span></button>"""
    else: blat[i] = '<div class="Error">Ошибки нет<div>'

Activity = int(Allposactivity) - Inactivity

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
logging.info("blat: " + str(len(blat)) + ", {}".format(', '.join(map(str, blat))))
logging.info("reg: " + str(len(reg)) + ", {}".format(', '.join(map(str, reg))))
logging.info("rez: " + str(len(rez)) + ", {}".format(', '.join(map(str, rez))))
logging.info("dater1: " + str(len(dater1)) + ", {}".format(', '.join(map(str, dater1))))
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
gc.collect()
#Создаем датафрейм
data = {'Reg': reg, 'Host': hosts, 'Port': Ports, 'clients': clients, 'URLS': URLS, 'PolzURLS': PolzURLS, 'Sysinfo': "Скачать", 'sysinfoURL': sysinfoURL}
df = pd.DataFrame.from_dict(data)
n = len(URLS)

df.style.format(make_clickable)
df.insert(6,'active/Pos', polz)
df['Clients'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['URLS'], x['clients']), axis=1)
df['Active/Pos'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['PolzURLS'], x['active/Pos']), axis=1)
df['SysInfo'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['sysinfoURL'], x['Sysinfo']), axis=1)

df = df.drop(['clients', 'URLS', 'Sysinfo', 'sysinfoURL', 'active/Pos', 'PolzURLS'], axis=1)
df.style
df.insert(4,'Corp-Trial', dater)
df.insert(5,'Срок службы', dater1)
df.insert(6,'Статус рега', status)
df.insert(8,'Перезапуск', perezap)
df.insert(9,'Рез. копия', rez)
df.insert(10,'Привязка', privyaz)
df.insert(11,'Ошибки системы', blat)

#Переводим датафрейм в html
html = df.to_html(index=False,escape=False) 
  
# write html to file с приминением стилей
text_file = open("index.html", "w") 
text_file.write(html_string_start + html + html_string_end)
text_file.close()
#Добавляем цвета к элементам
text_file = open("index.html", "r") 
filedata = text_file.read()
filedata = filedata.replace('В норме', '<span class="colortext1">В норме')
filedata = filedata.replace('Просрочена', '<span class="colortext">Просрочена')
filedata = filedata.replace('Перезаказ', '<span class="colortext">Перезаказ')
filedata = filedata.replace('No info', '<span class="colortext">No info')
filedata = filedata.replace('<td>No reg', '<td span class="backgroung1">No info')
filedata = filedata.replace('Нет информации', 'Браво Софт')
filedata = filedata.replace('Необходимо проверить состав БД', 'Необходимо проверить состав БД')
filedata = filedata.replace('status=unexpected change list products', 'Изменился состав продуктов')
filedata = filedata.replace('status=no required volume DB', 'Не подключены обязательные тома БД')
filedata = filedata.replace('table border="1" class="dataframe"', 'table')
filedata = filedata.replace('<tr style="text-align: right;">', '<tr class="sticky1">')
filedata = filedata.replace('Зарегистри', '<span class="colortext1">Без срока')


text_file.close()
with open('index.html', 'w') as file:
  file.write(filedata)
del filedata
text_file = open("index0.html", "r")
filedata = text_file.read()
start = filedata.find('ActiveSUNTD:')  
end = filedata.rfind('</a>&emsp;|&emsp;')  # rfind возвращает позицию с конца строки
substring = filedata[start:end]
filedata = filedata.replace(substring, 'ActiveSUNTD: ' + str(Activity) + '/' + Allposactivity + '</a>') 
text_file.close()
with open('index0.html', 'w') as file:
  file.write(filedata)
#df.to_html('index.html', justify='center', border=3, escape=False, classes='table table-striped')
gc.collect()
