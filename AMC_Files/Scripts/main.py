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

	os.chdir(os.path.dirname(os.getcwd()))

	for file in glob.glob("Data_Files/Excel/*.xlsx"):
		file_path = file
		sequence = file.split("/")[-1].split("_")[0]

		file_path1 = tkFileDialog.askopenfilename()
		wb1 = xlrd.open_workbook(filename = file_path1)
		sh1 = wb1.sheet_by_index(0)

		AMC_Data = {}

		AMC_Header1 = {"dataset":file_path1.split("/")[-1]}
		AMC_adsorbedContent = []

		begin = 0

		while True: 
			try: 
				row = {}

				row["index"] = begin 
				
				row["serial #"] = {}
				row["serial #"]["unit"] = ""
				row["serial #"]["value"] = sh1.cell_value(begin, 0)

				row["time"] = {}
				row["time"]["unit"] = "s (seconds)"
				row["time"]["value"] = sh1.cell_value(begin, 1)

				row["temperature"] = {} 
				row["temperature"]["unit"] = "C"
				row["temperature"]["value"] = sh1.cell_value(begin, 2)

				row["measured pressure"] = {}
				row["measured pressure"]["unit"] = "atm"
				row["measured pressure"]["value"] = sh1.cell_value(begin, 3)

				row["volume of gas(@STP)"] = {}
				row["volume of gas(@STP)"]["unit"] = "cc"
				row["volume of gas(@STP)"]["value"] = sh1.cell_value(begin, 4)

				row["weight %"] = {}
				row["weight %"]["unit"] = "wt%"
				row["weight %"]["value"] = sh1.cell_value(begin, 5)

				AMC_Content1.append(row)
				begin += 1 

			except: 
				break 


		file_path2 = tkFileDialog.askopenfilename()
		wb2 = xlrd.open_workbook(filename = file_path2)
		sh2 = wb2.sheet_by_index(0)

		AMC_Header2 = {"dataset":file_path2.split("/")[-1]}
		AMC_desorbedContent = []

		begin = 0

		while True: 
			try: 
				row = {}

				row["index"] = begin 
				
				row["serial #"] = {}
				row["serial #"]["unit"] = ""
				row["serial #"]["value"] = sh2.cell_value(begin, 0)

				row["time"] = {}
				row["time"]["unit"] = "s (seconds)"
				row["time"]["value"] = sh2.cell_value(begin, 1)

				row["temperature"] = {} 
				row["temperature"]["unit"] = "C"
				row["temperature"]["value"] = sh2.cell_value(begin, 2)

				row["measured pressure"] = {}
				row["measured pressure"]["unit"] = "atm"
				row["measured pressure"]["value"] = sh2.cell_value(begin, 3)

				row["volume of gas(@STP)"] = {}
				row["volume of gas(@STP)"]["unit"] = "cc"
				row["volume of gas(@STP)"]["value"] = sh2.cell_value(begin, 4)

				row["weight %"] = {}
				row["weight %"]["unit"] = "wt%"
				row["weight %"]["value"] = sh2.cell_value(begin, 5)

				AMC_Content2.append(row)
				begin += 1 

			except: 
				break 

	AMC_Data["content"] = AMC_Content 

	with open('Data_Files/JSON/8852_DataSet_AMC.json', 'w') as f:
		f.write(json.dumps(AMC_Data, sort_keys=True, indent=4, separators=(',', ': ')))
			
	with open('Data_Files/XML/8852_DataSet_AMC.xml', 'w') as f:
		f.write(dicttoxml.dicttoxml(AMC_Data))

	x = etree.parse("Data_Files/XML/8852_DataSet_AMC.xml")

	with open('Data_Files/XML/8852_DataSet_AMC.xml', 'w') as f:
		f.write(etree.tostring(x, pretty_print = True))