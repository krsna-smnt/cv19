import ipinfo
import os
import csv

access_token = "55873d1230f00c"
handler = ipinfo.getHandler(access_token)

def gather_by_ip(ip_addr):
	details = handler.getDetails(ip_addr)
	#print(details.all)
	return details.all

def unzip_ips(file):
	fh = open(file)
	ip_addr_list = []
	for line in fh:
		#print(line)
		info_list = line.split(" ")
		#print(info_list)
		ip_addr_list.append(info_list[1])

	return ip_addr_list



#def plot()
	
if __name__ == '__main__':

	new_l = unzip_ips("/home/sumanth/Desktop/cv19/hosts.txt")
	print(new_l)
	#ip_addr_list = ["54.208.102.37", "106.212.231.152"]
	ip_addr_list = list(set(new_l))
	dir_path = os.path.dirname(os.path.realpath(__file__))
	rel_path = "/cv19/media/"
	f = csv.writer(open(dir_path+rel_path+"traffic_dets_latest" + ".csv" , "w"))

	#print(gather_by_ip(ip_addr))
	#det = gather_by_ip("106.212.231.152")
	lat_list = long_list = []
	for ip_addr in ip_addr_list:
		ip_dets = gather_by_ip(ip_addr)
		lat = float(ip_dets['latitude'])
		lon = float(ip_dets['longitude'])
		timezone = ip_dets['timezone']
		#hostname = ip_dets['hostname']
		city = ip_dets['city']
		country_code = ip_dets['country']
		country = ip_dets['country_name']
		region = ip_dets['region']
		postal = ip_dets['postal']
		org = ip_dets['org']
		entry = [ip_addr, lat, lon, timezone, org, city, country, country_code, region, postal]
		print(entry)
		f.writerow(entry)
		#/var/log/apache2, other_vhosts_access.log, other_vhosts_access.log.1





		

		



	#print(det['country'])
