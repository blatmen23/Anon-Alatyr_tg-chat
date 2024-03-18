from threading import Thread
from database import CleanerDatabase
import time
import config

def cleaner():
  database = CleanerDatabase()
  while True:
    time.sleep(config.CLEANER_PERIOD * 60)
    database.minus_complaint()
    print("Клинер смыл одну жалобу с каждого")

def complaint_cleaner():
    t = Thread(target=cleaner)
    t.start()