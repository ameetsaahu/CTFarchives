#URL validator function
import re
def url_is_valid(string):

	regex = ("((http|https)://)(www.)?" +
			 "[a-zA-Z0-9@:%._\\+~#?&//=]" +
			 "{2,256}\\.[a-z]" +
			 "{2,6}\\b([-a-zA-Z0-9@:%" +
			 "._\\+~#?&//=]*)")
	if string:
		checker = re.compile(regex)

		if (re.search(checker, string)):
			return True

	return False

#JSON checker function
import urllib.request
import json
def link_is_json(string):
	stud = urllib.request.urlopen(string)
	data = stud.read()
	try:
		json_obj = json.loads(data)
	except:
		json_obj = 0
	return json_obj

def write_json_file(stud_dict):
	for entry in stud_dict:
		for key, value in entry.items():
			csv_dw.writerow({"Name":key, "Grade":value['grade']})

#-------------------------------------------------------------------------------------------------------------------------------
import sys
import csv

if len(sys.argv) != 2 :
	print("Usage:\n\tpython3 program.py \"input_file_name_here.txt\"")
	exit()

file = open(sys.argv[1], "r")

csv_file = open("output.csv", "w")
fields = ["Name", "Grade"]
csv_dw = csv.DictWriter(csv_file, fieldnames = fields)
csv_dw.writeheader()

while True:
	link = ""
	link = file.readline().strip("\n")
	if not link:	
		break

	if not url_is_valid(link):
		print("URL is incorrect")
		exit()

	stud_dict = link_is_json(link)
	if not stud_dict:
		print("file is not a JSON file")
		exit()
	
	print("Yo! Thats a JSON file")
	write_json_file(stud_dict)`