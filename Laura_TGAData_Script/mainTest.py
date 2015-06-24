import os
import xlrd
from collections import OrderedDict
import simplejson as json 
import tkFileDialog
import tkSimpleDialog
from Tkinter import *	

if __name__ == '__main__':

	root = Tk()

	print "Please select a file"
	file_path = tkFileDialog.askopenfilename()
	wb = xlrd.open_workbook(filename = file_path)

	label = Label(root, text = "Enter: [(Sheet Number) - 1]")
	label.pack()

	sheetNum = Entry(root)
	sheetNum.pack()

	button = Button(root, text = "Load")
	sh = wb.sheet_by_index(sheetNum)
	button.pack()

	root.mainloop()

	TGA_Data = OrderedDict()

	for rownum in range(1, sh.nrows):
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



	

