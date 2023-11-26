import requests
import sqlite3

#Создаем функцию sqlInput, которая принимает аргументы host_port и sunt_d.
def sqlInput(host_port, sunt_d):
    sunt_d = str(sunt_d)#Преобразуем sunt_d в строку.
    conn = sqlite3.connect("SUNTD.db", timeout=500)#Устанавливаем соединение с базой данных "SUNTD.db" с помощью метода connect() из модуля sqlite3. Устанавливаем таймаут соединения в 500 миллисекунд   
    #Задаем SQL-запрос для вставки или замены данных в таблице "Bases" 
    sql = """INSERT OR REPLACE INTO Bases (HostPort, Chet, SUNTD)
VALUES (?, 0, ?);
        """
    cursor = conn.cursor()#Создаем курсор для выполнения SQL запросов
    cursor.execute(sql, (host_port, sunt_d))#Выполняем SQL запрос с помощью метода execute() курсора, передавая значения переменных host_port и sunt_d
    conn.commit()#Фиксируем изменения в базе данных с помощью метода commit() 
    conn.close()#Закрываем соединение с базой данных с помощью метода close()
#Создаем функцию url_ok, которая принимает аргумент url
def url_ok(url):
    try:
        r = requests.get(url)#Пытаемся выполнить GET запрос к указанному URL с помощью метода get() из модуля requests
    except:
        r = requests.get("https://esia.gosuslugi.ru/")#Если возникает ошибка, выполняем GET запрос к URL "https://esia.gosuslugi.ru
        return False
    if r.status_code in [307, 303, 200, 302]:#Проверяем статус код ответа. Если он равен 307, 303, 200 или 302, возвращаем True. В противном случае возвращаем False
        return True
    else:
        return False
#Создаем список SUNTDstr с URL адресами    
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
    "http://suntd:41197"
]
#В цикле перебираем элементы списка SUNTDstr
for sunt_d_str in SUNTDstr:
    is_url_ok = url_ok(sunt_d_str)#Проверяем доступность URL адреса с помощью функции url_ok
    if is_url_ok:
        sqlInput(sunt_d_str, 1)#Если URL адрес доступен, вызываем функцию sqlInput с аргументами sunt_d_str и 1
#Создаем список host_port_list с URL адресами
host_port_list = [
    "http://suntd:80",
    "http://dream:3456"
]
#В цикле перебираем элементы списка host_port_list
for host_port in host_port_list:
    is_url_ok = url_ok(host_port)
    if is_url_ok:#Проверяем доступность URL адреса с помощью функции url_ok
        sqlInput(host_port, 1)#Если URL адрес доступен, вызываем функцию sqlInput с аргументами host_port и 1
#Создаем список S с URL адресами
S = [
    "http://REX:1000",
    "http://REX:80",
    "http://REX:4000"
]
#В цикле перебираем элементы списка S
for host_port in S:
    is_url_ok = url_ok(host_port)#Проверяем доступность URL адреса с помощью функции url_ok
    if is_url_ok:
        sqlInput(host_port, 0)#Если URL адрес доступен, вызываем функцию sqlInput с аргументами host_port и 0
#Создаем список sc_list с URL адресами
sc_list = [
    "http://95.79.112.201:80",
    "http://95.79.112.202:80",
    "http://95.79.112.203:80",
    "http://95.79.112.204:80",
    "http://95.79.59.227:80"
]
#В цикле перебираем элементы списка sc_list
for host_port in sc_list:
    is_url_ok = url_ok(host_port)#Проверяем доступность URL адреса с помощью функции url_ok
    if is_url_ok:
        sqlInput(host_port, 0)# Если URL адрес доступен, вызываем функцию sqlInput с аргументами host_port и 0
#Инициализируем переменные current_port, index и t          
current_port = 10
index = 10000
t = 0
#Входим в цикл while, пока index меньше 10000
while index < 10000:
    first_digit = str(index)[0]#Получаем первую цифру числа index и преобразуем ее в строку
#Формируем URL адреса first, second, third, forth, fifth, sixth и seventh с использованием значения переменной index
    first = f"http://95.79.112.201:{index}"
    second = f"http://95.79.112.202:{index}"
    third = f"http://95.79.112.203:{index}"
    forth = f"http://95.79.112.204:{index}"
    fifth = f"http://95.79.59.227:{index}"
    sixth = f"http://91.219.56.146:{index}"
    seventh = f"http://95.79.102.106:{index}"
#Проверяем значение переменной t        
    if t == 0:
        step = int(first_digit) * 1010#Если t равно 0, вычисляем значение переменной step как произведение первой цифры числа index на 1010
#Проверяем значение переменной step. Если оно равно 8080 или 9090, устанавливаем значение переменной t равным 3. В противном случае устанавливаем значение переменной t равным 1
        if step in [8080, 9090]:
            t = 3
        else:
            t = 1
#Если t равно 1, вычисляем значение переменной step как произведение первой цифры числа index на 1100            
    elif t == 1:
        step = int(first_digit) * 1100
#Проверяем значение переменной step. Если оно равно 8800 или 9900, устанавливаем значение переменной t равным 4. В противном случае устанавливаем значение переменной t равным 2
        if step in [8800, 9900]:
            t = 4
        else:
            t = 2
#Если t равно 3, увеличиваем значение переменной step на 1            
    elif t == 3:
        step = index + 1
#Проверяем значение переменной step. Если оно равно 8089 или 9099, устанавливаем значение переменной t равным 1. Если оно равно 8889, устанавливаем значение переменной t равным 2. В противном случае устанавливаем значение переменной t равным 3
        if step in [8089, 9099]:
            t = 1
        elif step == 8889:
            t = 2
        else:
            t = 3
#Если t равно 4, проверяем значение переменной index. Если оно равно 8800, устанавливаем значение переменной step равным 8880 и значение переменной t равным 3. В противном случае устанавливаем значение переменной step равным 9990 и значение переменной t равным 3
    elif t == 4:
        if index == 8800:
            step = 8880
            t = 3
        else:
            step = 9990
            t = 3
#Если ни одно из условий не выполняется, вычисляем значение переменной next_digit как сумму первой цифры числа index и 1. Затем вычисляем значение переменной step как произведение значения переменной next_digit на 1000. Устанавливаем значение переменной t равным 0        
    else:
        next_digit = int(first_digit) + 1
        step = next_digit * 1000
        t = 0
#Проверяем доступность URL адресов first, second, third, forth, fifth, sixth и seventh с помощью функции url_ok
    if url_ok(first):
        sqlInput(first, 0)
        
    if url_ok(second):
        sqlInput(second, 0)

    if url_ok(third):
        sqlInput(third, 0)
        
    if url_ok(forth):
        sqlInput(forth, 0)

    if url_ok(fifth):
        sqlInput(fifth, 0)

    if url_ok(sixth):
        sqlInput(sixth, 0)

    if url_ok(seventh):
        sqlInput(seventh, 0)
#Обновляем значение переменной index на значение переменной step      
    index = step
#Входим в цикл for, перебирая значения переменной port в диапазоне от 1209 до 1213
for port in range(1209, 1213):
#Инициализируем переменную sunt_d со значением 1
    sunt_d = 1
#Формируем URL адреса host_port и dream_port с использованием значения переменной port
    host_port = f"http://suntd:{port}"
    dream_port = f"http://dream:{port}"
#Проверяем доступность URL адресов host_port и dream_port с помощью функции url_ok
    if url_ok(host_port):
        sqlInput(host_port, sunt_d)
    if url_ok(dream_port):
        sqlInput(dream_port, sunt_d)