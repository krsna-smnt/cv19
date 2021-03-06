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
url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=COVID-19&terms-0-field=title&terms-1-operator=OR&terms-1-term=SARS-CoV-2&terms-1-field=abstract&terms-3-operator=OR&terms-3-term=COVID-19&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=SARS-CoV-2&terms-4-field=title&terms-5-operator=OR&terms-5-term=coronavirus&terms-5-field=title&terms-6-operator=OR&terms-6-term=coronavirus&terms-6-field=abstract&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&source=home-covid-19" 

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

        xp = "/html/body/main/div[2]/nav[1]/ul"
        xp1 = "/html/body/main/div[2]/nav[1]/ul/li[1]"

        pages_div = driver.find_element_by_xpath(xp)
        num_pages = len(pages_div.find_elements_by_tag_name("li"))
        print(num_pages)
        base_url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=COVID-19&terms-0-field=title&terms-1-operator=OR&terms-1-term=SARS-CoV-2&terms-1-field=abstract&terms-3-operator=OR&terms-3-term=COVID-19&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=SARS-CoV-2&terms-4-field=title&terms-5-operator=OR&terms-5-term=coronavirus&terms-5-field=title&terms-6-operator=OR&terms-6-term=coronavirus&terms-6-field=abstract&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&source=home-covid-19&start="
        base_path = "/html/body/main/div[2]/ol"
        datetime_obj = datetime.now()
        datetime_stamp = datetime_obj.strftime("%d-%b-%Y_%H:%M")
        rel2 = "pubs/"

        f = csv.writer(open(settings.MEDIA_ROOT+rel2+"pubs_arxiv_" + datetime_stamp + ".csv" , "w"))
        for i in range(num_pages):
            start = i * 200
            driver.get(base_url+str(start))
            articles_div = driver.find_element_by_xpath(base_path)
            articles_num = len(articles_div.find_elements_by_class_name("arxiv-result"))

            for j in range(1, articles_num+1):
                try:
                    date = driver.find_element_by_xpath(base_path+"/li["+str(j)+"]/p[4]").text
                except:
                    date = None
                try:
                    comments = driver.find_element_by_xpath(base_path+"/li["+str(j)+"]/p[5]/span[2]").text
                except:
                    comments = None
                try:
                    link = driver.find_element_by_xpath(base_path+"/li["+str(j)+"]/div/p/a").get_attribute("href")
                except:
                    link = None
                try:
                    pdf_link = driver.find_element_by_xpath(base_path+"/li["+str(j)+"]/div/p/span/a").get_attribute("href")
                except:
                    pdf_link = None
                try:
                    title = driver.find_element_by_xpath(base_path+"/li["+str(j)+"]/p[1]").text
                except:
                    title = None
                try:
                    authors_list = driver.find_element_by_xpath(base_path+"/li["+str(j)+"]/p[2]").find_elements_by_tag_name("a")
                    authors = [i.text for i in authors_list]
                    authorz = ""
                    for k in authors:
                        authorz += k + ", "
                    authorz = authorz.rstrip(", ")
                except:
                    authors_list = authors = authorz = None
                
                article = [title, authorz, link, pdf_link, date, comments]
                f.writerow(article)

                if not Publication.objects.filter(title=title).exists():
                    pub = Publication(title=title, authors=authorz, link=link)
                    pub.source = "arxiv"
                    pub.pdf = pdf_link
                    pub.date = date
                    pub.comments = comments
                    pub.save()

        driver.quit()
