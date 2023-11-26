import requests
import sqlite3

#������� ������� sqlInput, ������� ��������� ��������� host_port � sunt_d.
def sqlInput(host_port, sunt_d):
    sunt_d = str(sunt_d)#����������� sunt_d � ������.
    conn = sqlite3.connect("SUNTD.db", timeout=500)#������������� ���������� � ����� ������ "SUNTD.db" � ������� ������ connect() �� ������ sqlite3. ������������� ������� ���������� � 500 �����������   
    #������ SQL-������ ��� ������� ��� ������ ������ � ������� "Bases" 
    sql = """INSERT OR REPLACE INTO Bases (HostPort, Chet, SUNTD)
VALUES (?, 0, ?);
        """
    cursor = conn.cursor()#������� ������ ��� ���������� SQL ��������
    cursor.execute(sql, (host_port, sunt_d))#��������� SQL ������ � ������� ������ execute() �������, ��������� �������� ���������� host_port � sunt_d
    conn.commit()#��������� ��������� � ���� ������ � ������� ������ commit() 
    conn.close()#��������� ���������� � ����� ������ � ������� ������ close()
#������� ������� url_ok, ������� ��������� �������� url
def url_ok(url):
    try:
        r = requests.get(url)#�������� ��������� GET ������ � ���������� URL � ������� ������ get() �� ������ requests
    except:
        r = requests.get("https://esia.gosuslugi.ru/")#���� ��������� ������, ��������� GET ������ � URL "https://esia.gosuslugi.ru
        return False
    if r.status_code in [307, 303, 200, 302]:#��������� ������ ��� ������. ���� �� ����� 307, 303, 200 ��� 302, ���������� True. � ��������� ������ ���������� False
        return True
    else:
        return False
#������� ������ SUNTDstr � URL ��������    
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
#� ����� ���������� �������� ������ SUNTDstr
for sunt_d_str in SUNTDstr:
    is_url_ok = url_ok(sunt_d_str)#��������� ����������� URL ������ � ������� ������� url_ok
    if is_url_ok:
        sqlInput(sunt_d_str, 1)#���� URL ����� ��������, �������� ������� sqlInput � ����������� sunt_d_str � 1
#������� ������ host_port_list � URL ��������
host_port_list = [
    "http://suntd:80",
    "http://dream:3456"
]
#� ����� ���������� �������� ������ host_port_list
for host_port in host_port_list:
    is_url_ok = url_ok(host_port)
    if is_url_ok:#��������� ����������� URL ������ � ������� ������� url_ok
        sqlInput(host_port, 1)#���� URL ����� ��������, �������� ������� sqlInput � ����������� host_port � 1
#������� ������ S � URL ��������
S = [
    "http://REX:1000",
    "http://REX:80",
    "http://REX:4000"
]
#� ����� ���������� �������� ������ S
for host_port in S:
    is_url_ok = url_ok(host_port)#��������� ����������� URL ������ � ������� ������� url_ok
    if is_url_ok:
        sqlInput(host_port, 0)#���� URL ����� ��������, �������� ������� sqlInput � ����������� host_port � 0
#������� ������ sc_list � URL ��������
sc_list = [
    "http://95.79.112.201:80",
    "http://95.79.112.202:80",
    "http://95.79.112.203:80",
    "http://95.79.112.204:80",
    "http://95.79.59.227:80"
]
#� ����� ���������� �������� ������ sc_list
for host_port in sc_list:
    is_url_ok = url_ok(host_port)#��������� ����������� URL ������ � ������� ������� url_ok
    if is_url_ok:
        sqlInput(host_port, 0)# ���� URL ����� ��������, �������� ������� sqlInput � ����������� host_port � 0
#�������������� ���������� current_port, index � t          
current_port = 10
index = 10000
t = 0
#������ � ���� while, ���� index ������ 10000
while index < 10000:
    first_digit = str(index)[0]#�������� ������ ����� ����� index � ����������� �� � ������
#��������� URL ������ first, second, third, forth, fifth, sixth � seventh � �������������� �������� ���������� index
    first = f"http://95.79.112.201:{index}"
    second = f"http://95.79.112.202:{index}"
    third = f"http://95.79.112.203:{index}"
    forth = f"http://95.79.112.204:{index}"
    fifth = f"http://95.79.59.227:{index}"
    sixth = f"http://91.219.56.146:{index}"
    seventh = f"http://95.79.102.106:{index}"
#��������� �������� ���������� t        
    if t == 0:
        step = int(first_digit) * 1010#���� t ����� 0, ��������� �������� ���������� step ��� ������������ ������ ����� ����� index �� 1010
#��������� �������� ���������� step. ���� ��� ����� 8080 ��� 9090, ������������� �������� ���������� t ������ 3. � ��������� ������ ������������� �������� ���������� t ������ 1
        if step in [8080, 9090]:
            t = 3
        else:
            t = 1
#���� t ����� 1, ��������� �������� ���������� step ��� ������������ ������ ����� ����� index �� 1100            
    elif t == 1:
        step = int(first_digit) * 1100
#��������� �������� ���������� step. ���� ��� ����� 8800 ��� 9900, ������������� �������� ���������� t ������ 4. � ��������� ������ ������������� �������� ���������� t ������ 2
        if step in [8800, 9900]:
            t = 4
        else:
            t = 2
#���� t ����� 3, ����������� �������� ���������� step �� 1            
    elif t == 3:
        step = index + 1
#��������� �������� ���������� step. ���� ��� ����� 8089 ��� 9099, ������������� �������� ���������� t ������ 1. ���� ��� ����� 8889, ������������� �������� ���������� t ������ 2. � ��������� ������ ������������� �������� ���������� t ������ 3
        if step in [8089, 9099]:
            t = 1
        elif step == 8889:
            t = 2
        else:
            t = 3
#���� t ����� 4, ��������� �������� ���������� index. ���� ��� ����� 8800, ������������� �������� ���������� step ������ 8880 � �������� ���������� t ������ 3. � ��������� ������ ������������� �������� ���������� step ������ 9990 � �������� ���������� t ������ 3
    elif t == 4:
        if index == 8800:
            step = 8880
            t = 3
        else:
            step = 9990
            t = 3
#���� �� ���� �� ������� �� �����������, ��������� �������� ���������� next_digit ��� ����� ������ ����� ����� index � 1. ����� ��������� �������� ���������� step ��� ������������ �������� ���������� next_digit �� 1000. ������������� �������� ���������� t ������ 0        
    else:
        next_digit = int(first_digit) + 1
        step = next_digit * 1000
        t = 0
#��������� ����������� URL ������� first, second, third, forth, fifth, sixth � seventh � ������� ������� url_ok
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
#��������� �������� ���������� index �� �������� ���������� step      
    index = step
#������ � ���� for, ��������� �������� ���������� port � ��������� �� 1209 �� 1213
for port in range(1209, 1213):
#�������������� ���������� sunt_d �� ��������� 1
    sunt_d = 1
#��������� URL ������ host_port � dream_port � �������������� �������� ���������� port
    host_port = f"http://suntd:{port}"
    dream_port = f"http://dream:{port}"
#��������� ����������� URL ������� host_port � dream_port � ������� ������� url_ok
    if url_ok(host_port):
        sqlInput(host_port, sunt_d)
    if url_ok(dream_port):
        sqlInput(dream_port, sunt_d)