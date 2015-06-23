#### Script for first set of data from TGA (machine 1) ####

import os
import xlrd
from collections import OrderedDict
from dialog import Dialog
import simplejson as json 
import Tkinter as tk
import tkFileDialog
import tkSimpleDialog
import tkinter
	
#### Script prompting the user to select relevant excel file ####

print "Please select a file"
file_path = tkFileDialog.askopenfilename()
wb = xlrd.open_workbook(filename = file_path)

class TGApp:

	def __init__(self, master):
		frame = Frame(master)
		frame.pack()
		self.createwidgets()

	def createWidget(self):
		self.label = Label(frame, text = "Enter Sheet Number")
		self.label.pack() 

		button = Button(frame, text = "okay", command = frame.quit)
		self.button.pack()
		
		e1.grid(row=0, column=1)
		self.e1.grid.pack()
		
		e1 = Entry(frame)
		self.e1.pack()
		

		if int(self.e1.get()) > 0:
			return 'sh = wb.sheet_by_index' + (int(int(self.e1.get()))) - 1

		else:
			print "Error: Wierd index!"

root = tk.Tk()
root.mainloop()
print TGApp.createwidget(self)


TGA_Data = OrderedDict()

for rownum in range(1,sh.nrows):
	row_values = sh.row_values(rownum)
	# print row_values[9]
	TGA_Data['File Name'] = row_values[0]
	TGA_Data['Experiment'] = row_values[1]
	TGA_Data['Operator'] = row_values[2]
	TGA_Data['Experiment ID'] = row_values[3]
	TGA_Data['Sample Name'] = row_values[4]
	TGA_Data['Sample Lot #'] = row_values[5]
	TGA_Data['Notes'] = row_values[6]
	TGA_Data[''] = row_values[7]
	TGA_Data['Adsorbate'] = row_values[8]
	TGA_Data['Drying Temp'] = {}
	TGA_Data['Drying Temp']['unit']=row_values[9][1]
	TGA_Data['Drying Temp']['value']=row_values[9][0]
	TGA_Data['Heating Rate'] = row_values[10]
	TGA_Data['Max Drying Time'] = row_values[11]
	TGA_Data['Equil Crit'] = row_values[12]
	TGA_Data['Run Temp'] = row_values[13]
	TGA_Data['Max Equil Time'] = row_values[14]
	TGA_Data['Equil Crit'] = row_values[15]
	TGA_Data['Pres Steps'] = row_values[16]
	TGA_Data['Data Logging Interval'] = row_values[17]
	TGA_Data['Expt Started'] = row_values[18]
	TGA_Data['Run Started'] = row_values[19]



	TGA_Data['Elap Time'] = {}
	TGA_Data['Elap Time']['unit'] = 'min'
	TGA_Data['Elap Time']['value'] = 355.7

	if rownum == 22:
		TGA_Measurements = []
	
	# if rownum >= 24:
	# 	TGA_raw_Data = {}
	# 	for column in sh.column_values(rownum):
	# 		row_values = sh.row_values(rownum) #column_values i think.

	j = json.dumps(TGA_Data)

	with open('data.json', 'w') as f:
			f.write(j)


