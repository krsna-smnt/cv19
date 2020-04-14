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
    global driver

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options, executable_path='/usr/local/bin/geckodriver')
    driver.get(url)

    return True


def unpack_info(info):
    raw = []
    info_list = info.find_elements_by_tag_name('td')
    for inf in info_list:
        raw.append(inf.text)

    raw[0] = raw[0].strip()
    for i in range(1,10):
        raw[i] = raw[i].strip()
        raw[i] = raw[i].replace(",", "")
        raw[i] = raw[i].replace("+", "")
        raw[i] = raw[i].strip()
        if raw[i] == '' or raw[i] == ' ':
            raw[i] = '0'
        if raw[i] == 'N/A':
            raw[i] = 0
            continue
        if i == 8 or i == 9:
            raw[i] = float(raw[i])
        else:
            raw[i] = int(raw[i])

    #Format:
    #[country_name (type: string), total_cases (type: int), *new_cases (type: int), total_dead (type: int), new_dead (type: int), total_recovered (type: int), active_cases (type: int), critical_cases (type: int), cases_per_million (type: int), deaths_per_million (type: int), first_case_date (type: string)]
    return raw


class Command(BaseCommand):
    def handle(self, *args, **options):
        max_infected_ppm = 0
        max_dead_ppm = 0

        min_infected_ppm = 999999999
        min_dead_ppm = 999999999
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

        rel2 = "datasets/World/"
        f = csv.writer(open(settings.MEDIA_ROOT+rel2+"datasets_World_" + datetime_stamp + ".csv" , "w"))

        for item in items_set:
            ret = unpack_info(item)
            if ret[0] in 'World':
                continue
            max_infected_ppm = max(max_infected_ppm, ret[1])
            min_infected_ppm = min(min_infected_ppm, ret[1])

            max_dead_ppm = max(max_dead_ppm, ret[3])
            min_dead_ppm = min(min_dead_ppm, ret[3])

        for item in items_set:
            ret = unpack_info(item)

            try:
                f.writerow(ret)
                country = Country.objects.get(name=ret[0])

                oldn = country.total_cases
                newn = ret[1]

                country.total_cases = ret[1]
                country.new_infected = ret[2]
                country.infected = ret[6]
                country.new_dead = ret[4]
                country.dead = ret[3]
                country.cured = ret[5]
                country.critical = ret[7]
                country.cases_per_million = ret[8]
                country.dead_per_million = ret[9]

                try:
                    if oldn != newn:
                        country.percentage_increase = round(100 * int(country.new_infected) / int(country.total_cases), 2)
                except ZeroDivisionError:
                    country.percentage_increase = 0

                if 'World' in ret[0]:
                    country.save()
                    continue

                infected_ppm_color = rgb_vals(normalize0_1(ret[1], max_infected_ppm, min_infected_ppm))
                dead_ppm_color = rgb_vals(normalize0_1(ret[3], max_dead_ppm, min_dead_ppm))

                country.infected_color = infected_ppm_color
                country.dead_color = dead_ppm_color
                country.save()

            except:
                print("no such country")
