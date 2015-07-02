#### Run both file conversion script and plotting script ####

import os
import tkFileDialog
import tkSimpleDialog
import Tkinter as Tk
from Tkinter import *	
import time

time1 = time.sleep(1)
time2 = time.sleep(2)

def runTGA():

	print "Running TGA file conversion and creating plots"

	TGA_scripts_path =  os.path.dirname('%s/TGA_Files/Scripts/'%curr_path)
	TGAplot_path = os.chdir(TGA_scripts_path)

	os.system('python main.py')
	os.system('python TGAplot.py')

def runIGA():

	print "Running IGA file conversion and creating plots"

	IGA_scripts_path =  os.path.dirname('%s/IGA_Files/Scripts/'%curr_path)
	IGAplot_path = os.chdir(IGA_scripts_path)

	os.system('python main.py')
	os.system('python IGAplot.py')

def runAMC():

	print "Running AMC file conversion and creating plots"

	AMC_scripts_path =  os.path.dirname('%s/AMC_Files/Scripts/'%curr_path)
	AMCplot_path = os.chdir(AMC_scripts_path)

	os.system('python main.py')
	os.system('python AMCplot.py')

def machineInit(x):
	
	if x == 1: 
		runTGA()

	elif x == 2: 
		runIGA()

	elif x == 3: 
		runAMC()

	else: 
		pass


if __name__ == '__main__':
	
	curr_path = os.getcwd()

	machineInit(1)
	print "IGA JSON and XML files created. Plots completed"
	print "Redirecting to main path...."
	os.chdir(os.path.dirname('%s'%curr_path))
	
	machineInit(2)
	print "IGA JSON and XML files created. Plots completed"
	print "Redirecting to main path...."
	os.chdir(os.path.dirname('%s'%curr_path))
	time1
	
	machineInit(3)
	print "AMC JSON and XML files created. Plots completed"
	time2
	

	print "File conversion for TGA, IGA, and AMC completed. You will find the"
	print "corresponding Excel, JSON, and XML files in the individual machine"
	print "Data_Files folder. The plots can be found in the plots for each"
	print "machine in the corresponding <machine_name>_Files folder under the"
	print "folder name <machine_name>_plots"


