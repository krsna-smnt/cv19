from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import string
import sys
import signal
import time
import os

import csv
#from heat_color_reference import normalize0_1, rgb_vals

driver = None
url = "http://covid19tracker.co.in/uploadFiles/"


def stop_handler(sig, frame):
	print("Quit")
	driver.quit()
	sys.exit(0)
signal.signal(signal.SIGINT, stop_handler)


def pause_handler(signum, frame):
    print("Paused")
    signal.pause()
signal.signal(signal.SIGTSTP, pause_handler)


def init_driver():
	try:
		global driver

		options = Options()
		options.headless = True

		driver = webdriver.Firefox(options=options)
		driver.get(url)

		return True
	except:
		return False



def retrieve():
	if not init_driver():
		print("Failed to initialize")
		return


	dir_path = os.path.dirname(os.path.realpath(__file__))
	rel_path = "/cv19/media/"
	#rel2 = "/cv19/datasets/India/"
	try:
		stats_india = driver.find_element_by_name("statsIndia")
		stats_india.send_keys(dir_path+rel_path+"datasets_India_latest" + ".csv")
		print("done")
	except:
		print("stats_india unsuccessful")

	try:
		stats_world = driver.find_element_by_name("statsWorld")
		stats_world.send_keys(dir_path+rel_path+"datasets_World_latest" + ".csv")
		#	stats_world.send_keys("/root/cv19/cv19/datasets/World/datasets_World_13-Apr-2020_00:58.csv")
		print("done")
	except:
		print("stats_world unsuccessful")

	try:	
		colors_india = driver.find_element_by_name("colorIndia")
		colors_india.send_keys(dir_path+rel_path+"color_codes_India_latest"+".csv")
	except:
		print("color_india unsuccessful")

	try:
		colors_world = driver.find_element_by_name("colorWorld")
		colors_world.send_keys(dir_path+rel_path+"color_codes_World_latest"+".csv")
	except:
		print("color_world unsuccessful")

	try:	
		submit_button = driver.find_element_by_xpath("/html/body/div/form/button")
		submit_button.click()
		print("click")
	except:
		print("form submission unsuccessful")


if __name__ == "__main__":
	retrieve()
	try:
		driver.quit()
	except Exception as e:
		print("Failed to quit driver.\n")
		print(e.__class__.__name__)
