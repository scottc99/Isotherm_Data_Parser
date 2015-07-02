#### Script for plotting machine produced data ####

#### TGA (machine 1) ####

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
				content_dict = json_dict["content"][begin - 1]

				conc_dict = content_dict.get('weights')[3]
				conc_val = conc_dict.get('value')

				pressure_dict = content_dict.get('pressure')
				pressure_val = pressure_dict.get('value')

				pressure_list.append(pressure_val)
				conc_list.append(conc_val)
					
				begin +=1

			except:
				break

	
		plot_path = '%s/TGA_plots/%s_TGAplot.png'%(os.getcwd(), sequence)

		plt.plot(pressure_list, conc_list, 'ro')
		plt.axis([0, 50, 0, 3.5])
		plt.savefig('%s'%plot_path)

	print "done" 