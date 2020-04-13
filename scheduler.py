import schedule
import time
import os
import sys
import requests

def update_data_files():
    os.system("python upload_data.py")

def run_india_fetch():
    os.system("python fetch.py")

def run_world_fetch():
    os.system("python fetch_world.py")

def run_research_fetch():
    os.system("python fetch_research.py")
    os.system("python fetch_arxiv.py")

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

def job2():
    print("performing job2: research papers fetch")
    try:
    	run_research_fetch()
    except:
    	print("Couldn't run fetch_research.py or fetch_arxiv.py")


#schedule.every(0.1).minutes.do(job)
schedule.every(1).hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every(5).to(10).minutes.do(job)
schedule.every().tuesday.do(job2)
schedule.every().friday.do(job2)
#schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
