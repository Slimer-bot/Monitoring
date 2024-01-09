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

#Актуальная дата (формат дата)
current_date = datetime.now().strftime('%d.%m.%Y')
actualdate = current_date
#Почтовые адреса от кого и кому
addr_from = "o.zadonskiy@teh.expert"                # Адресат
addr_to   = "updatee@teh.expert"         # Получатель
#addr_to1 = "i.popov@teh.expert"
addr_to2 = "olegan.zadonskiy1@gmail.com"
#Пароль к почте
passwordMail  = "E6JCSx5uxK6KFEtukv7N"
#Дефолтный Header в сообщении на почте
Header = 'Отчет об ошибке'
#Строки для поиска ошибок в службах
substr = "status=unexpected change list products"
substr1 = "status=no required volume DB"
substr2 = "Необходимо проверить состав БД"
#Формат для логирования
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/Script2/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")
#Актуальная дата строкового типа
current_date = datetime.strptime(current_date, '%d.%m.%Y')
#Шаблон для страницы html
html_string_start = '''
<!DOCTYPE html>
<html lang="ru">
<head>
<title>Мониторинг установок Техэксперт | СУНТД</title>
<link rel="icon" href="suntd.ico" type="image/x-icon">
<link rel="shortcut icon" href="suntd.ico" type="image/x-icon">
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/sweetalert2@7.12.15/dist/sweetalert2.min.css'>
<link rel="stylesheet" href="CSS/style.css"> 
</head>
<body>
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

#Логин и пароли учеток служб
username = "kodeks"
#username1
password1 = "skedoks"
password = "kodeks"
password2 = "skedok"
#Агент для открытия вэб службы
headers1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
#неактивные установки
Inactivity = 0
#Все возможные установки
Allposactivity = 0
#Хосты
hosts=[]
#Порты
Ports=[]
#Даты
dater=[]
#Статус перезаказа
status=[]
#Корпоративная лицензия
stat=[]
#НАименование организации
clients=[]
#Ссылка на службу
URLS=[]
#Ссылка на СисИнфо
sysinfoURL=[]
#Ссылка на пользователей (лицензия)
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
#Ошибка
blat=[]
#Дата рега
dater1=[]

#Создание кликабельного текста в html
def make_clickable(val, v):
    return f'<a target="_blank" href="{val}">{v}</a>'

#Отправка почтового письма
def mailer(addr_from, passwordMail, addr_to, message, Header):
    try:
        #Формат сообщения
        msg = MIMEText(message.encode('utf-8'), 'plain', 'utf-8')                               # Создаем сообщение
        msg['From']    = addr_from                          # Адресат
        msg['To']      = addr_to                            # Получатель
        msg['Subject'] = Header                             # Заголовок
        server = smtplib.SMTP('smtp.mail.ru', 587)           # Создаем объект SMTP
        #server.set_debuglevel(1)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
        server.starttls()                                   # Начинаем шифрованный обмен по TLS
        server.login(addr_from, passwordMail)                   # Получаем доступ
        server.sendmail(msg['From'], addr_to, msg.as_string())  #Отправляем письмо                        # Отправляем сообщение
        server.quit()                                           #Покидаем сервер
        logging.info('Email sent!')                             #Успешная отправка
    except:
        logging.info('Something went wrong...')                 #Неуспешная отправка

#Обновление данных в БД об успешной отправке письма
def Adder(line, current_date):
    current_date = str(current_date).replace(".",",")
    #print(current_date)
    #Создаем соединение с БД
    conn = sqlite3.connect("SUNTD.db", timeout=500)
    #Заполняем столбец Chet текущей датой
    sql1 = """UPDATE Bases set Chet = '""" + current_date + """'WHERE HostPort ='""" + line + """';
    """
    #print(sql1)
    #logging.info('Something went wrong...')  
    cursor = conn.cursor()
    #Выполняем скрипт в  sql
    cursor.execute(sql1)
    #Сохраняем изменения
    conn.commit()
    #Закрываем соединение с БД
    conn.close()

#Код аутенфикации на сервере службы
def aunt(line, headers1, username, password, password1, password2, cookies):
    session = requests.Session() #Создаем сессию
    try:
        #Подключаемся к URL, используем куки сервера, в заголовке запроса указываем User-Agent (браузер), говорим, что соединение должно быть закрыто
        r = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
        # Указываем referer и User-Agent. Иногда , если не указать , то приводит к ошибкам. 
        session.headers.update({'Referer':line})
        session.headers.update({'User-Agent':headers1})
        #Производим утенфикацию по логину и паролю
        session.auth = (username, password)
        response = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
        #print(session.cookies.get_dict())
        if response.ok:
            #Если запрос удачный, то сохраняем текст страницы и закрываем соединение
            text = response.text
            response = session.close()
            return text
        else:
            try:
                #Иначе авторизируемся под другим паролем и пробуем по аналогии с ^
                session.auth = (username, password1)
                response = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
                if response.ok:
                    text = response.text
                    return text
            except:
                #Пробуем третью комбинацию пароля и пробуем по аналогии с ^
                session.auth = (username, password2)
                response = session.get(line, cookies=cookies, headers = {'User-Agent': headers1, 'Connection':'close'})
                if response.ok:
                    text = response.text
                    return text
        r.close()
        
    except:
        text = ""
        return text

#Устанавливаем соединение с БД
conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
#Выбираем все строки из таблицы NewBases, которые относятся к ТП и рабочие. Сортируем по HostPort
sqlite_select_query = """SELECT * from NewBases WHERE SUNTD = 0 and Actual = 1 ORDER BY HostPort"""
#Выполняем запрос к БД
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
#Записываем количество всех служб
Allposactivity = len(records)
#Для каждой службы из выборки БД
for row in records:
    #Записываем строку с URL
    line = row[0]
    #Видоизменяем URL в зависимости от необходимой информации со службы
    line1 = line.rstrip() + "/admin/title"
    line2 = line.rstrip() + "/admin/lic"
    line3 = line.rstrip() + "/admin/pref"
    line4 = line.rstrip() + "/admin"
    line5 = line.rstrip() + "/admin/cookies"
    line6 = line.rstrip() + "/sysinfo/metrics"
    #Узнаем, было ли отправлено сегодня сообщение
    mail = row[1]
    try:
        #Вытаскиваем сегодняшние куки из БД
        strokaforcook = row[4].replace("4443444","{").replace("333433","}").replace("221222",":").replace("112111","'").replace("000100",",").replace("555455"," ").replace("777677","==")
        cookies = eval(strokaforcook)
    except:
        cookies = row[4]
    #Говорим какие куки у сервера
    logging.info(cookies)
    #Считываем текста страниц
    text = aunt(line1, headers1, username, password, password1, password2, cookies)
    text1 = aunt(line2, headers1, username, password, password1, password2, cookies)
    text2 = aunt(line3, headers1, username, password, password1, password2, cookies)
    text3 = aunt(line6, headers1, username, password, password1, password2, cookies)

    #Разделяем строки, чтобы получить Host и Port
    parts = line.split("//" and ":")
    #сылка на скачивание сисинфо
    sysinfo = line.rstrip() + "/sysinfo/si_save_request"    
    parts[2] = parts[2].rstrip()
    Ports.append(parts[2])
    #print(line)

    try:
        #Ищем рег со страницы админки
        registr = text.split("Регистрационный номер: <B>" and "</B><BR>")
        registr = registr[1]
        #print(registr[38:])
        registr1 = registr[34:]
        #Добавляем рег в список
        reg.append(registr[34:])
    except:
        reg.append("No reg")
    
    try:
        #Вытаскиваем данные о названии организации из админки
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
        #Сохраняем данные о клиенте в список
        clients.append(result)
    except:
        clients.append("Нет информации")

    try:
        #Ищем информацию о привязке рега службы
        privazka = text1.split("</H3></CENTER><BR> Привязка:")
        sep = "<br>"
        privazka = privazka[1].split(sep, 1)[0]
        privazka = privazka.strip(' ')
        #print(privazka)
        privyaz.append(privazka)
    except:
        privyaz.append("No info")

    try:
        #Ищем информацию о запланированном создании резервной копии
        rezerv = text2.split("""<INPUT TYPE="TEXT" NAME="reservtime" VALUE=""")
        rezerv = rezerv[1]
        rezerv = rezerv[1:6]
        #print(rezerv.replace('"', ''))
        rez.append(rezerv.replace('"', ''))
    except:
        rez.append("No info")

    try:
        #На какое время назначен перезапуск службы
        perezapusk = text2.split("""<INPUT TYPE="TEXT" NAME="restarttime" VALUE=""")
        perezapusk = perezapusk[1]
        perezapusk = perezapusk[1:6]
        #print(perezapusk.replace('"', ''))
        perezap.append(perezapusk.replace('"', ''))
    except:
        perezap.append("No info")

    try:
        #Ищем информацию о занятых пользователями лицензий
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
        #Просматриваем сообщения об ошибках на службе
        lines=[]
        lines=text3.split('\n')
        long = len(lines)
        string = ""
        #Просматриваем построчно
        for i in lines:
            #Сообщения на странице каталога
            if 'kserver_main_page{service="kodweb",path=' in i:
                #Русифицируем, делаем пригодным для чтения и анализа
                string += i.replace('kserver_', '').replace('status="update DB"', 'Обновление/подключение БД').replace('main_page', '\nГлавная страница').replace('{service="kodweb",path=', ' ').replace('"', '').replace('}', '').replace(' 0', ' Ошибки нет').replace(' 1',' Ошибка ') + "\n"
            #Сообщение о предупреждениях в каталоге
            if 'kserver_product_control{service="kodweb",path=' in i:
                #Русифицируем, делаем пригодным для чтения и анализа
                string += i.replace('kserver_', '').replace('product_control', '\nНаличие предупреждения').replace('{service="kodweb",path=', ' ').replace('"', '').replace('}', '').replace(' 0', ' Ошибки нет').replace(' 1',' Необходимо проверить состав БД') + "\n"
        #print(string)
        #Добавляем информацию в список
        blat.append(string.replace('\n', '<br>'))
    except:
        blat.append("No info")
        string = ""

        
    #Проверяем наличие одного из сообщений об ошибке на службе
    if (substr in string) or (substr1 in string) or (substr2 in string):
        #print("Error")
        #Фиксируем сообщение об ошибке
        message = "На Службе: " + line + " выявлены следующие ошибки:\n" + string
        try:
            #Смотрим в БД и проверяем, делали ли сегодня рассылку
            timers = mail.replace(",",".")
            #print(timers)
            timers = datetime.strptime(timers, '%d.%m.%Y')
            timers = timers + timedelta(days=1)
            #print(timers)
            if current_date >= timers:
                #Сверям, было ли отправлено сегодня сообщение
                Adder(line, actualdate)
                #Обновляем заголовок
                Header = 'Отчет об ошибке' + registr1
                #Обращаемся к функции отправки сообщений
                mailer(addr_from, passwordMail, addr_to, message, Header)
                #mailer(addr_from, passwordMail, addr_to1, message, Header)
                mailer(addr_from, passwordMail, addr_to2, message, Header)
        except: timers = mail
        #Если раньше сообщения не отправлялись вовсе, но ошибка есть
        if timers == "0":
            Adder(line, actualdate)
            mailer(addr_from, passwordMail, addr_to, message, Header)
            #mailer(addr_from, passwordMail, addr_to1, message, Header)
            mailer(addr_from, passwordMail, addr_to2, message, Header)
    
    try:
        try:
            #Ищем корпоративную лицензию
            dateRab = text1.split("100001</td>")
            #print(dateRab[1][25:35])
            dater.append(dateRab[1][25:35])
            dateRab = datetime.strptime(dateRab[1][25:35], '%d.%m.%Y')

        except:
            dateRab = current_date
            dater.append("No info")
        try:
            #Лицензия рега
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
        status.append("No info")
    #Добавляем хост сервера в список
    hosts.append(parts[1][2:])
    stat.append(sysinfo)
    #Добавляем ссылку на админку службы в список
    URLS.append(line4)
    #Ссылка на сисинфо
    sysinfoURL.append(sysinfo)
    
#Закрываем соединение с БД
cursor.close()
conn.close()

#Создаем новое соединение с БД
conn = sqlite3.connect("SUNTD.db", timeout=1500)
cursor = conn.cursor()
#Отправляем запрос на поиск нерабочих служб
sqlite_select_query = """SELECT * from NewBases WHERE SUNTD = 0 and Actual = 0 ORDER BY HostPort"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
#Добавляем нерабочие службы к общему списку служб
Allposactivity += len(records)
Allposactivity = str(Allposactivity)
#Выводим количество служб, с которыми будет работать программа
logging.info("Всего строк:  " + Allposactivity)
#Для каждой службы выполняем:
for row in records:
    #Добавляем ссылки на службы
    line = row[0]
    line4 = line.rstrip() + "/admin"
    #Увеличиваем счетчик неактивных служб
    Inactivity += 1
    #Разделяем HostPort на host и Port
    parts = line.split("//" and ":")
    #ссылка на сохранение сисинфо
    sysinfo = line.rstrip() + "/sysinfo/si_save_request"    
    parts[2] = parts[2].rstrip()
    #Добавляем порт в список
    Ports.append(parts[2])
    #Добавляем Host в список
    hosts.append(parts[1][2:])
    #Добавляем ссылку на сисинфо
    stat.append(sysinfo)
    #Добавляем ссылку на службу
    URLS.append(line4)
    #Добавляем ссылку на сисинфо
    sysinfoURL.append(sysinfo)

    #Служба недоступна, поэтому все остальные списки заполняем значениями о том, что информации нет
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

#Заменяем те сообщения, в которых нет ошибки соответствующей подписью
for i in range(len(blat)):
    if (substr in blat[i]) or (substr1 in blat[i]) or (substr2 in blat[i]):
        blat[i] = """<button class="button-48" value='""" + blat[i].replace('Ошибка', ' ') + """'  type="button" onclick='f1(this)'><span class="text">Ошибка!!!<br>Подробнее</span></button>"""
    else: blat[i] = '<div class="Error">Ошибки нет<div>'
#Сверяем сколько служб активно из возможных
Activity = int(Allposactivity) - Inactivity
#Выводим информацию о заполненных списках
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
logging.info("reg: " + str(len(reg)) + ", {}".format(', '.join(map(str, reg))))
logging.info("blat: " + str(len(blat)) + ", {}".format(', '.join(map(str, blat))))
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
#Удаляем мусор
gc.collect()

#Формируем первичный датафрейм
data = {'Reg': reg,'Host': hosts, 'Port': Ports, 'clients': clients, 'URLS': URLS,'active/Pos': polz, 'PolzURLS': PolzURLS, 'Sysinfo': "Скачать", 'sysinfoURL': sysinfoURL}
df = pd.DataFrame.from_dict(data)
n = len(URLS)

#Делаем кликабельными данные из таблицы о клиентах, сисинфо и пользователей, работающих с лицензиями
df.style.format(make_clickable)
df['Clients'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['URLS'], x['clients']), axis=1)
df['Active/Pos'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['PolzURLS'], x['active/Pos']), axis=1)
df['SysInfo'] = df.apply(lambda x: "<a href='{}' target='_blank'>{}</a>".format(x['sysinfoURL'], x['Sysinfo']), axis=1)

#Удаляем столбцы, которые сделали кликабельными
df = df.drop(['clients', 'URLS', 'Sysinfo', 'sysinfoURL', 'active/Pos', 'PolzURLS'], axis=1)
#Стилизируем Датафрейм
df.style
#Добавляем списки в столбцы таблицы
df.insert(4,'Corp-Trial', dater)
df.insert(5,'Срок службы', dater1)
df.insert(6,'Статус рега', status)
df.insert(8,'Перезапуск', perezap)
df.insert(9,'Рез. копия', rez)
df.insert(10,'Привязка', privyaz)
df.insert(11,'Ошибки системы', blat)

#Переводим датафрейм в html
html = df.to_html(index=False,escape=False)  
  
#Создаем html страничку по шаблону и используя датафрейм 
text_file = open("index1.html", "w") 
text_file.write(html_string_start + html + html_string_end) 
text_file.close()
#Открываем файл html для чтения
text_file = open("index1.html", "r")
#Считываем данные из html
filedata = text_file.read()
#Добавляем цвета к элементам
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
filedata = filedata.replace('лБраво Софт‰', '"Браво Софт"')
#Закрываем Html файл
text_file.close()
#Открываем html файл для записи
with open('index1.html', 'w') as file:
  file.write(filedata)
#Убираем мусор
del filedata
#Запоминаем текущую дату и время в формате
DateTime = datetime.now().strftime("%d.%m.%Y %H:%M")
#Открываем html ГС для чтения
text_file = open("index0.html", "r", encoding="utf-8")
filedata = text_file.read()
#Индекс начала
start = filedata.find('ActiveTech:')  
end = filedata.rfind('</a>')  # rfind возвращает позицию с конца строки
substring = filedata[start:end] #Подстрока с индексами начала и конца
#Заполняем информацию об активных/возможных пользователях
filedata = filedata.replace(substring, 'ActiveTech:' + str(Activity) + '/' + Allposactivity)
start = filedata.find('Актуализировано')  #Индекс начала
end = filedata.rfind('<br>')  # rfind возвращает позицию с конца строки
substring = filedata[start:end] #Подстрока с индексами начала и конца
#Заполняем информацию об актуальности данных
filedata = filedata.replace(substring, 'Актуализировано (' + str(DateTime) + ')')
#Закрываем файл
text_file.close()
#Записываем все изменения на ГС
with open('index0.html', 'w', encoding="utf-8") as file:
  file.write(filedata)
  
#df.to_html('index.html', justify='center', border=3, escape=False, classes='table table-striped')
