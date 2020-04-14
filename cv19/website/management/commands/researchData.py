from django.core.management.base import BaseCommand, CommandError
from website.models import *
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import string, sys, signal, time, csv, os


driver = None
url = "https://connect.biorxiv.org/relate/content/181?page=1"

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
    global driver

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options, executable_path='/usr/local/bin/geckodriver')
    driver.get(url)

    return True

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not init_driver():
            print("Failed to initialize")
            return

        last = driver.find_element_by_xpath("/html/body/div[2]/section/div/div/div[1]/div[11]/div[2]/ul/li[11]")
        total_pages = int(last.text)
        base_url = "https://connect.biorxiv.org/relate/content/181?page="
        datetime_obj = datetime.now()
        datetime_stamp = datetime_obj.strftime("%d-%b-%Y_%H:%M")
        rel2 = "pubs/"

        f = csv.writer(open(settings.MEDIA_ROOT+rel2+"pubs_" + datetime_stamp + ".csv" , "w"))

        for i in range(1, total_pages+1):
            driver.get(base_url+str(i))
            for j in range(10):
                base_path = "/html/body/div[2]/section/div/div/div[1]/div["+str(j+1)+"]"
                try:
                    article_title = driver.find_element_by_xpath(base_path+"/div/div[1]/span/a").text
                except:
                    article_title = None
                try:
                    authors = driver.find_element_by_xpath(base_path+"/div/div[2]/span").text
                except:
                    authors = None
                try:

                    article_link = driver.find_element_by_xpath(base_path+"/div/div[1]/span/a").get_attribute('href')
                except:
                    article_link = None

                article = [article_title, authors, article_link]
                f.writerow(article)

                if not Publication.objects.filter(title=article_title).exists():
                    pub = Publication(title=article_title, authors=authors, link=article_link)
                    pub.source = "biorxiv" if "biorxiv" in article_link else "medrxiv"
                    pub.save()

        driver.quit()
