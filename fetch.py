from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

import sys
import signal
import time 

driver = None
requiredURL = "https://time.is/GMT"


def stop_handler(sig, frame):
	print("Quit")
	driver.quit()
	sys.exit(0)
signal.signal(signal.SIGINT, stop_handler)


def pause_handler(signum, frame):
    print("Paused")
    signal.pause()
signal.signal(signal.SIGTSTP, pause_handler)


def initDriver():
	try:
		global driver

		options = Options()
		options.headless = True

		driver = webdriver.Firefox(options=options)
		driver.get(requiredURL)

		return True
	except:
		return False


def getTime():
	if not initDriver():
		print("Failed to initialize")
		return

	timeDiv = driver.find_element_by_id('clock')
	time = lambda: timeDiv.find_elements_by_tag_name('span')
	while True:
		try:
			rightNow = ""
			for character in time():
				rightNow += str(character.get_attribute('innerHTML'))

			print (rightNow, end='\r')
		except Exception as e:
			# print(e.__class__.__name__)
			pass


if __name__ == "__main__":
	getTime()

	try:
		driver.quit()
	except Exception as e:
		print("Failed to quit driver.\n")
		print(e.__class__.__name__)
