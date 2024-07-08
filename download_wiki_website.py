import json
import sys
import os
import re
from pywebcopy import save_webpage
import time

def is_literal_or_date (answer): 
	return not('www.wikidata.org' in answer)

# return if the given string describes a year in the format YYYY
def is_year(year):
	pattern = re.compile('^[0-9][0-9][0-9][0-9]$')
	if not(pattern.match(year.strip())):
		return False
	else:
		return True

# return if the given string is a date
def is_date(date):
	pattern = re.compile('^[0-9]+ [A-z]+ [0-9][0-9][0-9][0-9]$')
	if not(pattern.match(date.strip())):
		return False
	else:
		return True

# return if the given string is a timestamp
def is_timestamp(timestamp):
	pattern = re.compile('^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T00:00:00Z')
	if not(pattern.match(timestamp.strip())):
		return False
	else:
		return True

# convert a year to timestamp style
def convert_year_to_timestamp(year):
	return year + '-01-01T00:00:00Z'


# convert the given month to a number
def convert_month_to_number(month):
	return{
		"january" : "01",
		"february" : "02",
		"march" : "03",
		"april" : "04",
		"may" : "05",
		"june" : "06",
		"july" : "07",
		"august" : "08",
		"september" : "09", 
		"october" : "10",
		"november" : "11",
		"december" : "12"
	}[month.lower()]


# convert a date from the wikidata frontendstyle to timestamp style
def convert_date_to_timestamp (date):	
	sdate = date.split(" ")
	# add the leading zero
	if (len(sdate[0]) < 2):
		sdate[0] = "0" + sdate[0]
	return sdate[2] + '-' + convert_month_to_number(sdate[1]) + '-' + sdate[0] + 'T00:00:00Z'


# get the wikidata id of a wikidata url
def wikidata_url_to_wikidata_id(url):
	if not url:
		return False
	if "XMLSchema#dateTime" in url or "XMLSchema#decimal" in url:
		date = url.split("\"", 2)[1]
		date = date.replace("+", "")
		return date
	if(is_literal_or_date(url)):
		if is_year(url):
			return convert_year_to_timestamp(url)
		if is_date(url):
			return convert_date_to_timestamp(url)
		else:
			url = url.replace("\"", "")
			return url
	else:
		url_array = url.split('/')
		# the wikidata id is always in the last component of the id
		return url_array[len(url_array)-1].split("?")[0].split(".")[0]

sys.path.append("/home/lihuil2/IterativeQA/Donot_Release/process_data/CONVEX/library")

if __name__ == '__main__':
    conversations = []
    conversations_path_train = "./data/CONQUER/ConvRef_trainset_processed.json"
    with open(conversations_path_train, "r") as data:
        conversations_train = json.load(data)
    
    conversations_path_dev = "./data/CONQUER/ConvRef_devset_processed.json"
    with open(conversations_path_dev, "r") as data:
        conversations_dev = json.load(data)
    
    conversations_path_test = "./data/CONQUER/ConvRef_testset_processed.json"
    with open(conversations_path_test, "r") as data:
        conversations_test = json.load(data)
    
    conversations.extend(conversations_train)
    conversations.extend(conversations_dev)
    conversations.extend(conversations_test)

    # get all useful entities
    node_set = set()
    for conversation in conversations:
        if 'conv_id' not in conversation:
            print(" xxx ", conversation)
            continue
        seed_entity = conversation['seed_entity']
        seed_entity = wikidata_url_to_wikidata_id(seed_entity)
        node_set.add(seed_entity)

        questions =  conversation['questions']
        for q in questions:
            answer = q['gold_answer']
            if type(answer) == list:
                answer = answer[0]
            answer = wikidata_url_to_wikidata_id(answer)
            if answer.startswith("Q") or answer.startswith("P"):
                node_set.add(answer)

    # read node and download data
    # if webpage already exist don't donwload
    download_folder = '/home/lihuil2/IterativeQA/Donot_Release/Downloads'
    download_folder_detail = download_folder + "/recognisable-name/www.wikidata.org/wiki"
    isExist = os.path.exists(download_folder_detail)
    if not isExist:
        os.makedirs(download_folder_detail)
    kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name'}

    downloaded_files = set()
    for path in os.listdir(download_folder_detail):
        if os.path.isfile(os.path.join(download_folder_detail, path)):
            downloaded_files.add(path.strip().split(".")[0])
    
    # download web page
    for node in node_set:
        if node not in downloaded_files:
            url = 'https://www.wikidata.org/wiki/' +  node
            save_webpage(url, download_folder, **kwargs)
            time.sleep(1.0) # sleep 1 seconds
            