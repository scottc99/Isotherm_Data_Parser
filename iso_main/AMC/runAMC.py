### Script for file format conversion for AMC (machine 3) ####

import glob, os
import posixpath as path
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
	wb1 = xlrd.open_workbook(filename = file_path)
	sh1 = wb1.sheet_by_index(0)

	content = []

	begin = 0

	while True: 
		try: 
			row1 = {}

			row1["index"] = begin
			
			row1["serial #"] = {}
			row1["serial #"]["unit"] = ""
			row1["serial #"]["value"] = sh1.cell_value(begin, 0)

			row1["time"] = {}
			row1["time"]["unit"] = "s (seconds)"
			row1["time"]["value"] = sh1.cell_value(begin, 1)

			row1["temperature"] = {} 
			row1["temperature"]["unit"] = "C"
			row1["temperature"]["value"] = sh1.cell_value(begin, 2)

			row1["measured pressure"] = {}
			row1["measured pressure"]["unit"] = "bar"
			row1["measured pressure"]["value"] = (sh1.cell_value(begin, 3))/(0.9869)

			row1["volume of gas(@STP)"] = {}
			row1["volume of gas(@STP)"]["unit"] = "cc"
			row1["volume of gas(@STP)"]["value"] = sh1.cell_value(begin, 4)

			row1["uptake"] = {}
			row1["uptake"]["unit"] = "mmol/g"
			row1["uptake"]["value"] = (sh1.cell_value(begin, 5)*10)/44

			content.append(row1)
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
			rowAds["measured pressure"]["unit"] = "bar"
			rowAds["measured pressure"]["value"] = (shAds.cell_value(begin, 3))/(0.9869)

			rowAds["volume of gas(@STP)"] = {}
			rowAds["volume of gas(@STP)"]["unit"] = "cc"
			rowAds["volume of gas(@STP)"]["value"] = shAds.cell_value(begin, 4)

			rowAds["uptake"] = {}
			rowAds["uptake"]["unit"] = "mmol/g"
			rowAds["uptake"]["value"] = (shAds.cell_value(begin, 5)*10)/44

			content.append(rowAds)
			begin += 1 

		except: 
			break 

	return (file_path1, content)


if __name__ == '__main__':

	os.chdir(os.path.dirname(os.getcwd()))
	already = []
	
	for file in glob.glob("AMC/Data_Files/Excel/*.xlsx"):
		absorb_path = ""
		desorb_path = ""

		if "ads" in file:
			absorb_path = file
		else:
			desorb_path = file
		
		sequence1 = file.split("/")[-1].split("_")[0]
		sequence2 = file.split("/")[-1].split("_")[2]
		sequence3 = file.split("/")[-1].split("_")[5]
		sequence4 = file.split("/")[-1].split("_")[6]


		if sequence1 and sequence2 and sequence3 and sequence4 in already:
			pass
			
		else:

			excelPath = '%s_8852_%s_CO2_20C_%s_%s_AMC.xlsx'%(sequence1, sequence2, sequence3, sequence4)
			jsonPath = '%s_8852_%s_CO2_20C_%s_%s_AMC.json'%(sequence1, sequence2, sequence3, sequence4)
			xmlPath = '%s_8852_%s_CO2_20C_%s_%s_AMC.xml'%(sequence1, sequence2, sequence3, sequence4)
			
			if absorb_path == "":
				absorb_path = "AMC/Data_Files/Excel/%s"%excelPath
			
			else: 
				desorb_path = "AMC/Data_Files/Excel/%s"%excelPath
			amc_data = {}
			absorb_content = load_set_2(absorb_path)
			desorb_content = load_set_2(desorb_path)

			amc_data["adsorbtion"] = {}
			amc_data["adsorbtion"]["filename"] = absorb_path.split("/")[-1]
			amc_data["adsorbtion"]["content"] = absorb_content

			amc_data["desorption"] = {}
			amc_data["desorption"]["filename"] = desorb_path.split("/")[-1]
			amc_data["desorption"]["content"] = desorb_content

			with open('AMC/Data_Files/JSON/%s'%jsonPath, 'w') as f:
				f.write(json.dumps(amc_data, sort_keys=True, indent=4, separators=(',', ': ')))
					
			with open('AMC/Data_Files/XML/%s'%xmlPath, 'w') as f:
				f.write(dicttoxml.dicttoxml(amc_data))

			x = etree.parse("AMC/Data_Files/XML/%s"%xmlPath)

			with open('AMC/Data_Files/XML/%s'%xmlPath, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))

			already.append(sequence1)
			already.append(sequence2)
			already.append(sequence3)
			already.append(sequence4)

			print "done" 

