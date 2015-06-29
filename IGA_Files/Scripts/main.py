#### Script for file format conversion for TGA (machine 1) ####

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

	file_path = tkFileDialog.askopenfilename()
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

			row["'%' mass"] = {} 
			row["'%' mass"]["unit"] = "'%' mass"
			row["'%' mass"]["value"] = sh.cell_value(begin, 2)

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

	with open('8852_DataSet_IGA.json', 'w') as f:
		f.write(json.dumps(IGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))
			
	with open('8852_DataSet_IGA.xml', 'w') as f:
		f.write(dicttoxml.dicttoxml(IGA_Data))

	x = etree.parse("8852_DataSet_IGA.xml")

	with open('8852_DataSet_IGA.xml', 'w') as f:
		f.write(etree.tostring(x, pretty_print = True))











