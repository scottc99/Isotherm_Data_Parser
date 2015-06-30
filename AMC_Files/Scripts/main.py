#### Script for file format conversion for AMC (machine 3) ####

import glob, os
import xlrd
from collections import OrderedDict
import simplejson as json 
import pprint
import tkFileDialog
from Tkinter import *	
import dicttoxml
import lxml.etree as etree

def isAbsorbed(content):
	if len(content) > 0:
		if content[-1]["measured pressure"]["value"] >= content[0]["measured pressure"]["value"]:
			return True
		else:
			return False
	else:
		print "Error: Dataset might be empty."
		return True

def load_set_2(file_path):
	wbAds = xlrd.open_workbook(filename = file_path)
	shAds = wbAds.sheet_by_index(0)

	content = []

	begin = 0

	while True: 
		try: 
			rowAds = {}

			rowAds["index"] = begin
			
			rowAds["serial #"] = {}
			rowAds["serial #"]["unit"] = ""
			rowAds["serial #"]["value"] = shAds.cell_value(begin, 0)

			rowAds["time"] = {}
			rowAds["time"]["unit"] = "s (seconds)"
			rowAds["time"]["value"] = shAds.cell_value(begin, 1)

			rowAds["temperature"] = {} 
			rowAds["temperature"]["unit"] = "C"
			rowAds["temperature"]["value"] = shAds.cell_value(begin, 2)

			rowAds["measured pressure"] = {}
			rowAds["measured pressure"]["unit"] = "atm"
			rowAds["measured pressure"]["value"] = shAds.cell_value(begin, 3)

			rowAds["volume of gas(@STP)"] = {}
			rowAds["volume of gas(@STP)"]["unit"] = "cc"
			rowAds["volume of gas(@STP)"]["value"] = shAds.cell_value(begin, 4)

			rowAds["weight %"] = {}
			rowAds["weight %"]["unit"] = "wt%"
			rowAds["weight %"]["value"] = shAds.cell_value(begin, 5)

			content.append(rowAds)
			begin += 1 

		except: 
			break 

	return content

def load_set():
	file_path1 = tkFileDialog.askopenfilename()
	wbAds = xlrd.open_workbook(filename = file_path1)
	shAds = wbAds.sheet_by_index(0)

	content = []

	begin = 0

	while True: 
		try: 
			rowAds = {}

			rowAds["index"] = begin
			
			rowAds["serial #"] = {}
			rowAds["serial #"]["unit"] = ""
			rowAds["serial #"]["value"] = shAds.cell_value(begin, 0)

			rowAds["time"] = {}
			rowAds["time"]["unit"] = "s (seconds)"
			rowAds["time"]["value"] = shAds.cell_value(begin, 1)

			rowAds["temperature"] = {} 
			rowAds["temperature"]["unit"] = "C"
			rowAds["temperature"]["value"] = shAds.cell_value(begin, 2)

			rowAds["measured pressure"] = {}
			rowAds["measured pressure"]["unit"] = "atm"
			rowAds["measured pressure"]["value"] = shAds.cell_value(begin, 3)

			rowAds["volume of gas(@STP)"] = {}
			rowAds["volume of gas(@STP)"]["unit"] = "cc"
			rowAds["volume of gas(@STP)"]["value"] = shAds.cell_value(begin, 4)

			rowAds["weight %"] = {}
			rowAds["weight %"]["unit"] = "wt%"
			rowAds["weight %"]["value"] = shAds.cell_value(begin, 5)

			content.append(rowAds)
			begin += 1 

		except: 
			break 

	return (file_path1, content)


if __name__ == '__main__':

	os.chdir(os.path.dirname(os.getcwd()))
	already = []
	for file in glob.glob("Data_Files/Excel/*.xlsx"):
		absorb_path = ""
		desorb_path = ""

		if "adsorbtion" in file:
			absorb_path = file
		else:
			desorb_path = file
		
		sequence = file.split("/")[-1].split("_")[0]
		print "Sequence: %s"%sequence
		if sequence in already:
			pass
		else:
			if absorb_path == "":
				absorb_path = "Data_Files/Excel/%s_adsorbtion.xlsx"%sequence
			else:
				desorb_path = "Data_Files/Excel/%s_desorption.xlsx"%sequence
		
			amc_data = {}
			absorb_content = load_set_2(absorb_path)
			desorb_content = load_set_2(desorb_path)

			amc_data["adsorbtion"] = {}
			amc_data["adsorbtion"]["filename"] = absorb_path.split("/")[-1]
			amc_data["adsorbtion"]["content"] = absorb_content

			amc_data["desorption"] = {}
			amc_data["desorption"]["filename"] = desorb_path.split("/")[-1]
			amc_data["desorption"]["content"] = desorb_content

			with open('Data_Files/JSON/%s_DataSet_AMC.json'%sequence, 'w') as f:
				f.write(json.dumps(amc_data, sort_keys=True, indent=4, separators=(',', ': ')))
					
			with open('Data_Files/XML/%s_DataSet_AMC.xml'%sequence, 'w') as f:
				f.write(dicttoxml.dicttoxml(amc_data))

			x = etree.parse("Data_Files/XML/%s_DataSet_AMC.xml"%sequence)

			with open('Data_Files/XML/%s_DataSet_AMC.xml'%sequence, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))

			already.append(sequence)




