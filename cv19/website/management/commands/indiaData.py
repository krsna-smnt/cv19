from django.core.management.base import BaseCommand, CommandError
import ipinfo, os, csv, string, sys, signal, time
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

from .heat_color_reference import normalize0_1, rgb_vals


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
    global driver

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options, executable_path='/usr/local/bin/geckodriver')
    driver.get(url)

    return True


def unpack_info(info):
    if info is None:
        return
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

    dead_n_str = ""
    for c in dead_str:
        if c in "1234567890":
            dead_n_str += c
        else:
            break
    dead_str = dead_str.replace(dead_n_str, "")
    dead_str.strip()
    dead_n_str.strip()

    # [district-name (type: string), infected (type: int), dead (type: int), district_details (type: string)]
    ret = [str(district_name), int(infected_str), int(dead_n_str), str(dead_str)]

    return ret


class Command(BaseCommand):
    def handle(self, *args, **options):
        max_infected = 0
        max_dead = 0
        min_infected = 99999999
        min_dead = 99999999

        print("hi")
        if not init_driver():
            print("Failed to initialize")
            return

        items = driver.find_elements_by_class_name("clickable")
        items_set = list(set(items))
        districts = []

        for item in items_set:
            districts.append(item.get_attribute("data-original-title"))
        districts_set = list(set(districts))
        print("%d administrative entities found\n" % len(districts_set))

        
        datetime_obj = datetime.now()
        datetime_stamp = datetime_obj.strftime("%d-%b-%Y_%H:%M")
        
        rel2 = "datasets/India/"
        print("hloo")
        f = csv.writer(open(settings.MEDIA_ROOT+rel2+"datasets_India_" + datetime_stamp + ".csv" , "w"))

        for district in districts_set:
            ret = unpack_info(district)
            if ret is None:
                continue

            max_infected = max(max_infected, ret[1])
            min_infected = min(min_infected, ret[1])

            max_dead = max(max_dead, ret[2])
            min_dead = min(min_dead, ret[2])

        for district in districts_set:
            print("yoyo")
            ret = unpack_info(district)
            if ret is None:
                continue

            infected_color = rgb_vals(normalize0_1(ret[1], max_infected, min_infected))
            dead_color = rgb_vals(normalize0_1(ret[2], max_dead, min_dead))
            f.writerow(ret)

            try:
                print("yes")
                subregion = Subregion.objects.get(name=ret[0])
                subregion.total_cases = ret[1]
                subregion.dead = ret[2]
                subregion.infected_color = infected_color
                subregion.dead_color = dead_color
                subregion.save()
            except:
                print("no such subregion", ret[0])

        driver.quit()
