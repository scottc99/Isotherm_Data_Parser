#### Script for plotting machine produced data ####

#### AMC (machine 3) ####

import glob, os
from collections import OrderedDict
import simplejson as json 	
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot, ion
import pylab
import numpy as np


if __name__ == '__main__':

	
	os.chdir(os.path.dirname(os.getcwd()))

	for file in glob.glob("Data_Files/JSON/*.json"):
		json_file_path = file
		sequence = file.split("/")[-1].split("_")[0]

		with open('%s'%json_file_path) as json_data_file:    
			json_dict = json.load(json_data_file)

	
		begin = 1

		pressure_list = []
		conc_list = []

		while True: 
			try:
				adsorption_dict = json_dict.get("adsorbtion")
				
				content1_dict = adsorption_dict["content"][begin -1]

				conc1_dict = content1_dict.get("uptake")
				conc1_val = conc1_dict.get("value")

				pressure1_dict = content1_dict.get("measured pressure")
				pressure1_val = pressure1_dict.get("value")

				conc_list.append(conc1_val)
				pressure_list.append(pressure1_val)

				desorption_dict = json_dict.get("desorption")
				
				content2_dict = desorption_dict["content"][begin -1]

				conc2_dict = content2_dict.get("uptake")
				conc2_val = conc2_dict.get("value")

				pressure2_dict = content2_dict.get("measured pressure")
				pressure2_val = pressure2_dict.get("value")

				conc_list.append(conc2_val)
				pressure_list.append(pressure2_val)

				begin +=1

			except:
				break

	

	plt.plot(pressure_list, conc_list, 'ro')
	plt.axis([-5, 50, 0, 3.5])
	plt.show()

	print "done" 