import glob, os
from collections import OrderedDict
import simplejson as json 	
import matplotlib
import matplotlib.markers as mark
from matplotlib.markers import MarkerStyle
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot, ion
import pylab
import numpy as np

if __name__ == '__main__':

#### AMC metadata for comp. plot ####

	
	os.chdir(os.path.dirname(os.getcwd()))

	for file in glob.glob("AMC_Files/Data_Files/JSON/*"):
		json_file_pathAMC = file
		sequence = file.split("/")[-1].split("_")[0]

		with open('%s'%json_file_pathAMC) as json_data_fileAMC:    
			json_dictAMC = json.load(json_data_fileAMC)

	
		begin1 = 1

		pressure_listAMC = []
		conc_listAMC = []

		while True: 
			try:
				adsorption_dictAMC = json_dictAMC.get("adsorbtion")
				
				content1_dictAMC = adsorption_dictAMC["content"][begin1 - 1]

				conc1_dictAMC = content1_dictAMC.get("uptake")
				conc1_valAMC = conc1_dictAMC.get("value")

				pressure1_dictAMC = content1_dictAMC.get("measured pressure")
				pressure1_valAMC = pressure1_dictAMC.get("value")

				conc_listAMC.append(conc1_valAMC)
				pressure_listAMC.append(pressure1_valAMC)

				desorption_dictAMC = json_dictAMC.get("desorption")
				
				content2_dictAMC = desorption_dictAMC["content"][begin1 - 1]

				conc2_dictAMC = content2_dictAMC.get("uptake")
				conc2_valAMC = conc2_dictAMC.get("value")

				pressure2_dictAMC = content2_dictAMC.get("measured pressure")
				pressure2_valAMC = pressure2_dictAMC.get("value")

				conc_listAMC.append(conc2_valAMC)
				pressure_listAMC.append(pressure2_valAMC)

				begin1 +=1

			except:
				break


#### IGA metadata for comp. plot ####


	for file in glob.glob("IGA_Files/Data_Files/JSON/*.json"):
		json_file_pathIGA = file
		sequence = file.split("/")[-1].split("_")[0]

		with open('%s'%json_file_pathIGA) as json_data_fileIGA:    
			json_dictIGA = json.load(json_data_fileIGA)

		begin2 = 1

		pressure_listIGA = []
		conc_listIGA = []

		while True: 
			try:
				content_dictIGA = json_dictIGA["content"][begin2 - 1]
				
				pressure_dictIGA = content_dictIGA.get('pressure')
				conc_dictIGA = content_dictIGA.get('concentration')

				pressure_valIGA = pressure_dictIGA.get('value')
				conc_valIGA = conc_dictIGA.get('value')

				pressure_listIGA.append(pressure_valIGA)
				conc_listIGA.append(conc_valIGA)
					
				begin2 +=1

			except:
				break

#### TGA metadata for comp. plot ####


	for file in glob.glob("TGA_Files/Data_Files/JSON/*.json"):
		json_file_pathTGA = file
		sequence = file.split("/")[-1].split("_")[0]

		with open('%s'%json_file_pathTGA) as json_data_fileTGA:    
			json_dictTGA = json.load(json_data_fileTGA)

	

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
		
		plot_pathComp = '%s/Comparison_Files/Comparison_plots/%s_Compplot.png'%(os.getcwd(), sequence)

		plAMC = pressure_listAMC
		plIGA = pressure_listIGA
		plTGA = pressure_listTGA

		
		plt.plot(pressure_listAMC, conc_listAMC, 'ro')

		# plt.plot(pressure2_valAMC, conc2_valAMC, 'ro')
		mark.MarkerStyle(marker = 'o', fillstyle = u'none')

		plt.plot(pressure_listIGA, conc_listIGA, 'bs')
		mark.MarkerStyle(marker = 's', fillstyle = u'none')

		plt.plot(pressure_listTGA, conc_listTGA, 'g^')
		mark.MarkerStyle(marker = '^', fillstyle = u'none')

		plt.axis([0, 50, 0, 3.75])
		plt.savefig('%s'%plot_pathComp)


	print "done"