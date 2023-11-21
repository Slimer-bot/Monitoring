import schedule
import os
import time
import logging
import sqlite3
import requests
from datetime import datetime, timedelta


current_date = datetime.now().strftime('%d.%m.%Y')
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename = "logs/Base/logs_" + current_date + ".txt", format=format, level=logging.INFO, datefmt="%H:%M:%S")
logging.info("Служба запущена")

def job_1():
    logging.info("1 thread running...")
    try:
        os.startfile("DataCheck.exe")
    except:
        logging.info("DataCheck.exe can't start running...")
    try:
        os.startfile("pyScript.exe")
    except:
        logging.info("pyScript.exe can't start running...")
    try:
        os.startfile("pyScript2.exe")
    except:
        logging.info("pyScript2.exe can't start running...")
    

def job_2():
    logging.info("2 thread running...")
    try:
        os.startfile("checkSUNTD.exe")
    except:
        logging.info("checkSUNTD.exe can't start running...")

schedule.every(5).minutes.do(job_1)
schedule.every(1).hours.do(job_2)


while True:
    schedule.run_pending()
    time.sleep(1)

    
