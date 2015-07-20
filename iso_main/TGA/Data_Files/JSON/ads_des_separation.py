#### Separation of .json files into adsorption and desorption lists ####

import glob, os
import xlrd
from collections import OrderedDict
import simplejson as json 
import pprint
import tkFileDialog
import tkSimpleDialog
from Tkinter import *	
import dicttoxml
import lxml.etree as etree
import traceback

if __name__ == '__main__':
	print os.getcwd()

	json_fileList = []

	for file in glob.glob("JSON/json_aliq/*.json"):
		json_file_pathTGA = file
		sequence1 = file.split("/")[-1].split("_")[0]
		sequence2 = file.split("/")[-1].split("_")[1]

		with open('%s'%json_file_pathTGA) as json_data_fileTGA:    
			json_dictTGA = json.load(json_data_fileTGA)

		json_fileList.append(file)
		index = json_fileList.index(file)

		begin3 = 1

		pressure_listTGA = []
		conc_listTGA = []


		while True: 
			try:
				content_dictTGA = json_dictTGA["content"][begin3 - 1]

				conc_dictTGA = content_dictTGA.get('weights')[3]
				conc_valTGA = conc_dictTGA.get('value')

				pressure_dictTGA = content_dictTGA.get('pressure')
				pressure_valTGA = pressure_dictTGA.get('value')

				pressure_listTGA.append(pressure_valTGA)
				conc_listTGA.append(conc_valTGA)
					
				begin3 +=1

			except:
				break

