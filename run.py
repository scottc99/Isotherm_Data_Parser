#### Run both file conversion script and plotting script ####

import os
import tkFileDialog
import tkSimpleDialog
from Tkinter import *	
import time

time2 = time.sleep(2)
time3 = time.sleep(3)

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

def machineButton(machine):

	root = Tk()
	machNum = 1

	while True:
		try: 
			if machNum == machine:
				label = Label(root, text = "Machine 1 - TGA")
				label.pack()

				button1 = Button(root, text = "Run TGA Program")
				button1.pack()

				machNum += 1	

				time3
				runTGA()

			elif machNum == machine:
				label = Label(root, text = "Machine 2 - IGA")
				label.pack()

				button2 = Button(root, text = "Run IGA Program")
				button2.pack()

				machNum += 1

				time3
				runIGA()

			elif machNum == machine:
				label = Label(root, text = "Machine 3 - AMC")
				label.pack()

				button3 = Button(root, text = "Run AMC Program")
				button3.pack()

				machNum += 1

				time3
				runAMC()

			else: 
				pass
		except: 
			break

if __name__ == '__main__':
	
	curr_path = os.getcwd()

	machineButton(1)
	root.destroy()
	print "TGA JSON and XML files created. Plots completed"
	
	print "Redirecting to main path...."
	os.chdir(os.path.dirname('%s'%curr_path))
	
	time2
	machineButton(2)
	root.destroy()
	print "IGA JSON and XML files created. Plots completed"
	
	print "Redirecting to main path...."
	os.chdir(os.path.dirname('%s'%curr_path))
	
	time2
	machineButtons(3)
	root.destroy()
	print "AMC JSON and XML files created. Plots completed"

	time3
	print "File conversion for TGA, IGA, and AMC completed. You will find the"
	print "corresponding Excel, JSON, and XML files in the individual machine"
	print "Data_Files folder. The plots can be found in the plots for each"
	print "machine in the corresponding <machine_name>_Files folder under the"
	print "folder name <machine_name>_plots"


