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
#from heat_color_reference import normalize0_1, rgb_vals
import os


driver = None
url = "https://connect.biorxiv.org/relate/content/181?page=1"
#url_arxiv = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=COVID-19&terms-0-field=title&terms-1-operator=OR&terms-1-term=SARS-CoV-2&terms-1-field=abstract&terms-3-operator=OR&terms-3-term=COVID-19&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=SARS-CoV-2&terms-4-field=title&terms-5-operator=OR&terms-5-term=coronavirus&terms-5-field=title&terms-6-operator=OR&terms-6-term=coronavirus&terms-6-field=abstract&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&source=home-covid-19"

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

	last = driver.find_element_by_xpath("/html/body/div[2]/section/div/div/div[1]/div[11]/div[2]/ul/li[11]")
	total_pages = int(last.text)
	#/html/body/div[2]/section/div/div/div[1]/div[1]
	#//*[@id="region-content"]
	print(total_pages)
	#print(total_pages+3)
	base_url = "https://connect.biorxiv.org/relate/content/181?page="
	datetime_obj = datetime.now()
	datetime_stamp = datetime_obj.strftime("%d-%b-%Y_%H:%M")
	dir_path = os.path.dirname(os.path.realpath(__file__))
	rel_path = "/cv19/media/"
	rel2 = "/cv19/pubs/"

	f = csv.writer(open(dir_path+rel2+"pubs_" + datetime_stamp + ".csv" , "w"))
	g = csv.writer(open(dir_path+rel_path+"pubs_latest"+".csv" , "w"))


	for i in range(1, total_pages+1):
		driver.get(base_url+str(i))
		for j in range(10):
			base_path = "/html/body/div[2]/section/div/div/div[1]/div["+str(j+1)+"]"
			article_title = driver.find_element_by_xpath(base_path+"/div/div[1]/span/a").text
			authors = driver.find_element_by_xpath(base_path+"/div/div[2]/span").text
			article_link = driver.find_element_by_xpath(base_path+"/div/div[3]/span/span[1]/a").get_attribute('href')
			article = [article_title, authors, article_link]
			#csv dump
			f.writerow(article)
			g.writerow(article)

if __name__ == "__main__":
	retrieve()
	try:
		driver.quit()
	except Exception as e:
		print("Failed to quit driver.\n")
		print(e.__class__.__name__)





