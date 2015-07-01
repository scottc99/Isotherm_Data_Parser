#### Script for plotting machine produced data ####

#### IGA (machine 2) ####

import glob, os
from collections import OrderedDict
import simplejson as json 
from pprint import pprint
import tkFileDialog
from Tkinter import *	
import matplotlib.pyplot as plot
import numpy as np


if __name__ == '__main__':

	
	os.chdir(os.path.dirname(os.getcwd()))

	for file in glob.glob("Data_Files/JSON/*.json"):
		json_file_path = file
		sequence = file.split("/")[-1].split("_")[0]

		with open('%s'%json_file_path) as json_data_file:    
			json_dict = json.load(json_data_file)
		
#						{Pressure}
#					{		row		 }		
#				[		  Content		 ]
#			 {			 json_data   		}

		

		begin = 1

		pressure_dict = {}
		
		while True: 
			try:
				content_dict = json_dict["content"][begin - 1]
				print content_dict
				row_dict = content_dict[3]
				print row_dict
				bar_val = row_dict[0]
				
				for value in bar_val.values():
					pressure_dict.append(value)
					
				begin +=1

			except:
				break 

		

