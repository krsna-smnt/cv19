from django.core.management.base import BaseCommand, CommandError
import ipinfo, os, csv, string
from website.models import UserTracking
from django.conf import settings
import os.path

access_token = "55873d1230f00c"
handler = ipinfo.getHandler(access_token)

def unzip_ips(file):
    fh = open(file, encoding='utf-8')
    ip_addr_list = []

    device_info_list = []
    total_count = 0
    for line in fh:
        info_list = line.split(" ")
    
        line = line.rstrip("\n")
        line = line[::-1]
        ctr = 0
        txt = ""
        for i in line:
            if i == "\"":
                if ctr < 2:
                    ctr += 1
                    continue
                else: 
                    break
            else:
                txt += i
        ip_addr_list.append(info_list[1])
        device_info_list.append(txt[::-1])
        total_count += 1

    return ip_addr_list, device_info_list, total_count

def gather_by_ip(ip_addr):
    details = handler.getDetails(ip_addr)
    return details.all


class Command(BaseCommand):
    def handle(self, *args, **options):
        files = ['/var/log/apache2/other_vhosts_access.log', '/var/log/apache2/other_vhosts_access.log.1']

        for file in files:
            if os.path.isfile(file):
                new_l, _, _  = unzip_ips(settings.MEDIA_ROOT + "hosts.txt")
                ip_addr_list = list(set(new_l))

                lat_list = long_list = []
                for ip_addr in ip_addr_list:
                    count = 0
                    for ip_addr_dup in new_l:
                        if ip_addr_dup == ip_addr:
                            count += 1
                    ip_dets = gather_by_ip(ip_addr)
                    lat = float(ip_dets['latitude'])
                    lon = float(ip_dets['longitude'])
                    timezone = ip_dets['timezone']

                    city = ip_dets['city']
                    country_code = ip_dets['country']
                    country = ip_dets['country_name']
                    region = ip_dets['region']
                    postal = ip_dets['postal']
                    org = ip_dets['org']
                    entry = [ip_addr, count, lat, lon, timezone, org, city, country, country_code, region, postal]
                    userInfo = UserTracking(ip_address=ip_addr, count=count, country=country, latitude=lat, longitude=lon, timezone=timezone, organization=org, city=city, country_code=country_code, region=region, postal=postal)
                    userInfo.save()
            else:
                print("not a file")