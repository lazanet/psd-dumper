# -*- coding: utf-8 -*-
import urllib, os, json, time, urllib.request, subprocess, datetime
from pprint import pprint
from bs4 import BeautifulSoup
from multiprocessing import Pool, Value, Array

def fetch_url(url, mode="PYTHON"):
	agent =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
	if (mode == "PYTHON"):
		req = urllib.request.Request(url, data=None, headers={'User-Agent': agent})
		with urllib.request.urlopen(req) as f:
			data = f.read().decode('utf-8', 'ignore')
		return data
	else:
		out = subprocess.Popen(["curl" ,url, "-H 'Connection: keep-alive'", "-H 'Upgrade-Insecure-Requests: 1'", "-H '{}'".format(agent), "-H 'Sec-Fetch-Mode: navigate'", "-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'", "-H 'Sec-Fetch-Site: none'", "-H 'Accept-Encoding: gzip, deflate, br'", "-H 'Cookie: cookieconsent_dismissed=yes; defaultFormat=6;'", "--compressed"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout,stderr = out.communicate()
		return stdout

def exp_json(data):
	return json.dumps(data, indent=4, ensure_ascii=False)

def save(text, filepath):
	dirs = os.path.dirname(filepath)
	if not dirs != '' and not os.path.exists(dirs):
		os.makedirs(dirs, exist_ok = True)
	with open(filepath, 'w', encoding="utf-8") as my_file:
		my_file.write(text)

def links_extract(url):
	data = fetch_url(url)
	soup = BeautifulSoup(data, "lxml")
	return [link for link in soup.findAll('a')]	

def select_extract(url, name):
	obj = {}
	print (url)
	data = fetch_url(url)
	soup = BeautifulSoup(data, "lxml")
	tmp = soup.find(attrs={"name" : name}).findChildren()
	for item in tmp:
		obj[item.get_text().strip()] = item.get('value')
	obj.pop("")
	return obj

def time():
	now = datetime.datetime.now()
	d = int(now.strftime("%d"))
	m = int(now.strftime("%m"))
	Y = int(now.strftime("%Y"))
	y = int(now.strftime("%y"))
	M = now.strftime("%b")
	return {'d':d, 'm':m, 'y':y, 'M': M, 'Y':Y}
	
####################################################################
host = "https://pesstatsdatabase.com"

def dump_nations():
	# Find All Nations
	data = select_extract(host, "DdbNations")
	return data
	
def dump_championships(id):
	data = select_extract(host+"/PSD/select_championship.php?q={}".format(id), "DdbChamp")
	return data

def dump_clubs(id):
	data = select_extract(host+"/PSD/select_club.php?q={}".format(id), "DdbClub")
	return data

def dump_players(id):
	data = select_extract(host+"/PSD/select_players.php?q={}".format(id), "DdbClub")
	for player in data:
		data[player] = int(data[player][3:].split("&")[0])
	return {v: k for k, v in data.items()}

def dump_stats(id, version=999):
	#print("{}, version={}".format(id, version))
	stats = ""
	ver = ""

	if (version < 14):
		ver = "_old2011"
	elif (version >= 14 and version <= 17):
		ver = "20{}".format(version)

	url = host+"/PSD/Player{}.php?Id={}".format(ver, id)
	#print(url)

	data = fetch_url(url, "CURL")

	soup = BeautifulSoup(data, "lxml")
	for br in soup.find_all("br"):
		br.replace_with("\n")
	try:
		tmp = soup.find(attrs={"id" : "info"})
		stats += tmp.getText()
		tmp = soup.find(attrs={"id" : "other_info"})
		stats += tmp.getText()
	except:
		pass
	return stats
