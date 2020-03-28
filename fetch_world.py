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
url = "https://www.worldometers.info/coronavirus/"


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
	raw = []
	info_list = info.find_elements_by_tag_name('td')
	for inf in info_list:
		raw.append(inf.text)

	raw[0] = raw[0].strip()
	for i in range(1,len(raw)):
		raw[i] = raw[i].strip()
		raw[i] = raw[i].replace(",", "")
		raw[i] = raw[i].replace("+", "")
		if raw[i] == '' or raw[i] == ' ':
			raw[i] = '0'
		if i == 8 or i == 9:
			raw[i] = float(raw[i])
		else:
			raw[i] = int(raw[i])

	#Format:
	#[country_name (type: string), total_cases (type: int), *new_cases (type: int), total_dead (type: int), new_dead (type: int), total_recovered (type: int), active_cases (type: int), critical_cases (type: int), cases_per_million (type: int), deaths_per_million (type: int)]

	return raw



def retrieve():
	max_infected_ppm = 0.00
	max_dead_ppm = 0.00

	min_infected_ppm = 999999.99
	min_dead_ppm = 999999.99
	if not init_driver():
		print("Failed to initialize")
		return

	table_div = driver.find_element_by_id("main_table_countries_today")
	table_rows_odd = table_div.find_elements_by_class_name("odd")
	table_rows_even = table_div.find_elements_by_class_name("even")

	table_rows_odd += table_rows_even
	items = table_rows_odd 

	items_set = list(set(items))
	
	print("%d administrative entities found\n" % len(items_set))

	datetime_obj = datetime.now()
	datetime_stamp = datetime_obj.strftime("%d-%b-%Y_%H:%M")

	f = csv.writer(open("datasets_World_" + datetime_stamp + ".csv" , "w"))
	g = csv.writer(open("color_codes_World_" + datetime_stamp + ".csv" , "w"))

	for item in items_set:
		ret = unpack_info(item)
		max_infected_ppm = max(max_infected_ppm, ret[len(ret) - 2])
		min_infected_ppm = min(min_infected_ppm, ret[len(ret) - 2])

		max_dead_ppm = max(max_dead_ppm, ret[len(ret) - 1])
		min_dead_ppm = min(min_dead_ppm, ret[len(ret) - 1])

	for item in items_set:
		ret = unpack_info(item)
		infected_ppm_color = rgb_vals(normalize0_1(ret[len(ret) - 2], max_infected_ppm, min_infected_ppm))
		dead_ppm_color = rgb_vals(normalize0_1(ret[len(ret) - 1], max_dead_ppm, min_dead_ppm))
		color_list = [ret[0], infected_ppm_color, dead_ppm_color]
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