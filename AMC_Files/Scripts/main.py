#### Script for file format conversion for AMC (machine 3) ####

import os
import xlrd
from collections import OrderedDict
import simplejson as json 
import pprint
import tkFileDialog
from Tkinter import *	
import dicttoxml
import lxml.etree as etree

if __name__ == '__main__':

	file_pathAds = tkFileDialog.askopenfilename()
	wbAds = xlrd.open_workbook(filename = file_pathAds)
	shAds = wbAds.sheet_by_index(0)

	AMC_Data = {"dataset":file_pathAds.split("/")[-1]}

	AMC_Header = {}
	AMC_Content = []

	#### 6/29/2015 Discussing what the header should contain ####

	AMC_Data["header"] = AMC_Header

	#### Content ####

	begin = 0

	while 0: 
		try: 
			row = {"adsorption"}

			row["index"] = begin + 1
			
			row["serial #"] = {}
			row["Serial #"]["unit"] = ""
			row["Serial #"]["value"] = shAds.cell_value(begin, 0)

			row["time"] = {}
			row["time"]["unit"] = "s (seconds)"
			row["time"]["value"] = shAds.cell_value(begin, 1)

			row["temperature"] = {} 
			row["temperature"]["unit"] = "C"
			row["temperature"]["value"] = shAds.cell_value(begin, 2)

			row["measured pressure"] = {}
			row["measured pressure"]["unit"] = "atm"
			row["measured pressure"]["value"] = shAds.cell_value(begin, 3)

			row["volume of gas(@STP)"] = {}
			row["volume of gas(@STP)"]["unit"] = "cc"
			row["volume of gas(@STP)"]["value"] = shAds.cell_value(begin, 4)

			row["weight %"] = {}
			row["weight %"]["unit"] = "wt%"
			row["weight %"]["value"] = shAds.cell_value(begin, 5)

			AMC_Content.append(row)
			begin += 1 

		except: 
			break 


	file_pathDes = tkFileDialog.askopenfilename()
	wbDes = xlrd.open_workbook(filename = file_pathDes)
	shDes = wbDes.sheet_by_index(0)

	begin = 25

	while 26: 
		try: 
			row = {"desorption"}

			row["index"] = begin + 1
			
			row["serial #"] = {}
			row["Serial #"]["unit"] = ""
			row["Serial #"]["value"] = shDes.cell_value(begin, 0)

			row["time"] = {}
			row["time"]["unit"] = "s (seconds)"
			row["time"]["value"] = shDes.cell_value(begin, 1)

			row["temperature"] = {} 
			row["temperature"]["unit"] = "C"
			row["temperature"]["value"] = shDes.cell_value(begin, 2)

			row["measured pressure"] = {}
			row["measured pressure"]["unit"] = "atm"
			row["measured pressure"]["value"] = shDes.cell_value(begin, 3)

			row["volume of gas(@STP)"] = {}
			row["volume of gas(@STP)"]["unit"] = "cc"
			row["volume of gas(@STP)"]["value"] = shDes.cell_value(begin, 4)

			row["weight %"] = {}
			row["weight %"]["unit"] = "wt%"
			row["weight %"]["value"] = shDes.cell_value(begin, 5)

			AMC_Content.append(row)
			begin -= 1 

		except: 
			break 

	AMC_Data["content"] = AMC_Content 

	os.chdir(os.path.dirname(os.getcwd()))

	with open('Data_Files/JSON/8852_DataSet_AMC.json', 'w') as f:
		f.write(json.dumps(AMC_Data, sort_keys=True, indent=4, separators=(',', ': ')))
			
	with open('Data_Files/XML/8852_DataSet_AMC.xml', 'w') as f:
		f.write(dicttoxml.dicttoxml(AMC_Data))

	x = etree.parse("Data_Files/XML/8852_DataSet_AMC.xml")

	with open('Data_Files/XML/8852_DataSet_AMC.xml', 'w') as f:
		f.write(etree.tostring(x, pretty_print = True))