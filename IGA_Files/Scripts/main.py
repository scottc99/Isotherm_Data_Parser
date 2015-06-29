#### Script for file format conversion for IGA (machine 2) ####

import glob, os
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
		wb = xlrd.open_workbook(filename = file_path)
		sh = wb.sheet_by_index(0)

		IGA_Data = {"dataset":file_path.split("/")[-1]}

		IGA_Header = {}
		IGA_Content = []

		#### 6/28/2015 Discussing what the header should contain ####

		IGA_Data["header"] = IGA_Header

		#### Content ####

		begin = 1

		while 1: 
			try: 
				row = {}

				row["index"] = begin 
				
				row["weight"] = {}
				row["weight"]["unit"] = "mg"
				row["weight"]["value"] = sh.cell_value(begin, 0)

				row["pressure"] = {}
				row["pressure"]["unit"] = "mbar"
				row["pressure"]["value"] = sh.cell_value(begin, 1)

				row["mass %"] = {} 
				row["mass %"]["unit"] = "mass %"
				row["mass %"]["value"] = sh.cell_value(begin, 2)

				row["concentration"] = {}
				row["concentration"]["unit"] = "mmol/g"
				row["concentration"]["value"] = sh.cell_value(begin, 3)

				row["sample temp"] = {}
				row["sample temp"]["unit"] = "C"
				row["sample temp"]["value"] = sh.cell_value(begin, 4)

				IGA_Content.append(row)
				begin += 1 

			except: 
				break 

		IGA_Data["content"] = IGA_Content 

		#filename = file_path.split("/")[-1].split(".")[0]

		with open('Data_Files/JSON/%s_DataSet_IGA.json'%sequence, 'w') as f:
			f.write(json.dumps(IGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))
				
		with open('Data_Files/XML/%s_DataSet_IGA.xml'%sequence, 'w') as f:
			f.write(dicttoxml.dicttoxml(IGA_Data))

		x = etree.parse("Data_Files/XML/%s_DataSet_IGA.xml"%sequence)

		with open('Data_Files/XML/%s_DataSet_IGA.xml'%sequence, 'w') as f:
			f.write(etree.tostring(x, pretty_print = True))











