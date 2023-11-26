import schedule
import os
import time
import logging

# Устанавливаем формат логирования
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename="logs/logs.txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")
logging.info("Служба запущена")

def job_1():
    logging.info("1 thread running...")
    
    # Запускаем DataCheck.exe
    try:
        os.startfile("DataCheck.exe")
    except:
        logging.info("DataCheck.exe can't start running...")
    
    # Запускаем pyScript.exe
    try:
        os.startfile("pyScript.exe")
    except:
        logging.info("pyScript.exe can't start running...")
    
    # Запускаем pyScript2.exe
    try:
        os.startfile("pyScript2.exe")
    except:
        logging.info("pyScript2.exe can't start running...")

def job_2():
    logging.info("2 thread running...")
    
    # Запускаем checkSUNTD.exe
    try:
        os.startfile("checkSUNTD.exe")
    except:
        logging.info("checkSUNTD.exe can't start running...")

# Устанавливаем расписание выполнения задач
schedule.every(5).minutes.do(job_1)
schedule.every(1).hours.do(job_2)

# Запускаем бесконечный цикл выполнения задач
while True:
    schedule.run_pending()
    time.sleep(1)