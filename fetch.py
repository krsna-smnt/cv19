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

import csv
from heat_color_reference import normalize0_1, rgb_vals

driver = None
url = "https://covindia.com/"



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



def unpack_info(info):
	district_name = ""
	infected_str = ""
	dead_str = ""
	info = info.replace("\"","")
	inter = info.split('|')
	
	district_name = inter[0].strip()

	if len(inter) > 1:
		inter[1] = inter[1].replace("Infected:", "")
		inter[2] = inter[2].replace("Deaths:", "")
		infected_str = inter[1].strip()
		dead_str = inter[2].strip()

	else:
		infected_str = dead_str = "0"

	#Final touches
	dead_n_str = ""
	for c in dead_str:
		if c in "1234567890":
			dead_n_str += c
		else:
			break
	dead_str = dead_str.replace(dead_n_str, "")
	dead_str.strip()
	dead_n_str.strip()

	#Format:
	# [district-name (type: string), infected (type: int), dead (type: int), district_details (type: string)]
	ret = [district_name, int(infected_str), int(dead_n_str), dead_str]

	return ret




def retrieve():
	max_infected = 0
	max_dead = 0

	min_infected = 99999999
	min_dead = 99999999
	if not init_driver():
		print("Failed to initialize")
		return

	items = driver.find_elements_by_class_name("clickable")
	items_set = list(set(items))
	districts = []

	for item in items_set:
		districts.append(item.text)
	districts_set = list(set(districts))
	print("%d administrative entities found\n" % len(districts_set))

	
	datetime_obj = datetime.now()
	datetime_stamp = datetime_obj.strftime("%d-%b-%Y_%H:%M")

	f = csv.writer(open("datasets_India_" + datetime_stamp + ".csv" , "w"))
	g = csv.writer(open("color_codes_India_" + datetime_stamp + ".csv" , "w"))

	for district in districts_set:
		ret = unpack_info(district)
		max_infected = max(max_infected, ret[1])
		min_infected = min(min_infected, ret[1])

		max_dead = max(max_dead, ret[2])
		min_dead = min(min_dead, ret[2])

	for district in districts_set:
		ret = unpack_info(district)
		infected_color = rgb_vals(normalize0_1(ret[1], max_infected, min_infected))
		dead_color = rgb_vals(normalize0_1(ret[2], max_dead, min_dead))
		color_list = [ret[0], infected_color, dead_color]
		f.writerow(ret)
		g.writerow(color_list)
		print(ret)
		#print(color_list)



if __name__ == "__main__":
	retrieve()
	try:
		driver.quit()
	except Exception as e:
		print("Failed to quit driver.\n")
		print(e.__class__.__name__)
