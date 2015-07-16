#### Script for file format conversion for TGA (machine 1) ####

import glob, os
from collections import OrderedDict, Counter
import simplejson as json 	
import matplotlib
import matplotlib.markers as mark
from matplotlib.markers import MarkerStyle
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot, ion
import pylab
import numpy as np

os.chdir(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))

for file in glob.glob("Data_Files/JSON/json_blankRuns/*.json"):
	sequence1 = file.split("/")[-1].split("_")[0]
	sequence2 = file.split("/")[-1].split("_")[1]
	sequence3 = file.split("/")[-1].split("_")[2:]
	
	pathTail = "_".join(sequence3)

	already = []
	json_file_pathTGA = file

	loopNum = 1
	while True:
		try:
			if sequence1 and sequence2 in already: 
				pass

			else:
				with open('%s'%json_file_pathTGA) as json_data_fileTGA:    
					json_dictTGAloopNum = json.load(json_data_fileTGA)
			loopNum += 1
		except: 
			break

	already.append(sequence1)
	already.append(sequence2)

	print loopNum

