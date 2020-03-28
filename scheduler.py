import schedule
import time
import os
import sys

def update_date_files():
	pass

def run_india_fetch():
	os.system("python3 fetch.py")
def run_world_fetch():
	os.system("python3 fetch_world.py")

def job():
    print("Performing Jobs")
    try:
    	run_india_fetch()
    except:
    	print("Couldn't run fetch.py")
    try:
    	run_world_fetch()
    except:
    	print("Couldn't run fetch_world.py")

    try:
    	update_data_files()
    except:
    	print("Couldn't update data files")

#schedule.every(0.1).minutes.do(job)
schedule.every(1).hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every(5).to(10).minutes.do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
