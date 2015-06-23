#### Script for first set of data from TGA (machine 1) ####

import os
import xlrd
from collections import OrderedDict
import simplejson as json 
import tkFileDialog
import tkSimpleDialog
from Tkinter import *	
#### Script prompting the user to select relevant excel file ####

# class TGApp(Frame):

# 	def __init__(self, master):
		
# 		Frame.__init__(self, master)
# 		Frame.pack()
		
# 		self.label = Label(self, text = "Enter Sheet Number").grid(row = 0)
# 		self.label.pack()
		
# 		self.button = Button(self, text = "okay", command = Frame.quit)
# 		self.button.pack()


# 		self.button = Entry(self)
# 		sheet = self.get()
# 		print str(sheet)


# class TGApp(Label):

# 	def __init__(self, master = None):

# 		Label.__init__(self, master)
		
# 		self.label = Label(self, text = "Enter Sheet Number")
# 		self.label.pack()

# 	def grid(self):

# 		self.tk.call(self, row = 0, column = 0)

		
# class TGApp(Button):

# 	def __init__(self, master = None):
		
# 		Button.__init__(self, master)

# 		self.button = Button(self, text = "okay", command = Frame.quit)
# 		self.button.pack()

# class TGApp(Entry):
	
# 	def __init__(self, master = None, widget = None):
		
# 		Entry.__init__(self)
# 		sheet = self.get()
# 		print str(sheet)
		# if int(sheet) > 0:
		# 	print 'sh = wb.sheet_by_index' + (int(sheet) - 1)
		# else:
		# 	print 'Eee Roar!' 



class TGApp:
	def __init__(self):
		self.root = Tk()
		self.label = Label(self.root, text = "Enter Sheet Number")
		self.label.pack()

		self.entry = Entry(self.root)
		self.entry.pack()

		button = Button(self.root, text = "Load", command = self.load_sheet)
		button.pack()

	def load_sheet(self):
		self.sheet = self.entry.get()
		print "Sheet No: %s"%self.sheet
		if int(self.sheet) > 0:
			try:
				self.sh = self.wb.sheet_by_index(int(self.sheet) - 1)
				self.root.destroy()
			except:
				print "Error loading the sheet."
		else:
			print 'Eee Roar!'

	def run(self):
		print "Please select a file"
		file_path = tkFileDialog.askopenfilename()
		self.wb = xlrd.open_workbook(filename = file_path)
		self.root.mainloop()



# class Student:
# 	def __init__(self, name):
# 		self.name = name

# 	def whoAreYou(self):
# 		print "I am %s."%self.name

# 	def rename(self, newName):
# 		self.name = newName



if __name__ == '__main__':

	TGInstance = TGApp()
	TGInstance.run()

	# student1 = Student("John")
	# student2 = Student("Alice")

	# student1.whoAreYou()
	# student2.whoAreYou()

	# student2.rename("Alicia")
	
	# student1.whoAreYou()
	# student2.whoAreYou()

	# root = Tk()
	# label = Label(root, text = "Enter Sheet Number")
	# label.pack()

	# entry = Entry(root)
	# entry.pack()

	# def load_sheet():
	# 	sheet = entry.get()
	# 	print "Sheet No: %s"%sheet
	# 	if int(sheet) > 0:
	# 		try:
	# 			sh = wb.sheet_by_index(int(sheet) - 1)
	# 			root.destroy()
	# 		except:
	# 			print "Error loading the sheet."
	# 	else:
	# 		print 'Eee Roar!'

	# button = Button(root, text = "Load", command = load_sheet)
	# button.pack()

	
	# root.mainloop()
	# print "Hey!!! Where am i?"


#if int(self.e1.get()) > 0:
#			return 'sh = wb.sheet_by_index' + (int(int(self.e1.get()))) - 1
#else:
#			print "Error: Wierd index!"


# TGA_Data = OrderedDict()

# for rownum in range(1,sh.nrows):
# 	row_values = sh.row_values(rownum)
# 	# print row_values[9]
# 	TGA_Data['File Name'] = row_values[0]
# 	TGA_Data['Experiment'] = row_values[1]
# 	TGA_Data['Operator'] = row_values[2]
# 	TGA_Data['Experiment ID'] = row_values[3]
# 	TGA_Data['Sample Name'] = row_values[4]
# 	TGA_Data['Sample Lot #'] = row_values[5]
# 	TGA_Data['Notes'] = row_values[6]
# 	TGA_Data[''] = row_values[7]
# 	TGA_Data['Adsorbate'] = row_values[8]
# 	TGA_Data['Drying Temp'] = {}
# 	TGA_Data['Drying Temp']['unit']=row_values[9][1]
# 	TGA_Data['Drying Temp']['value']=row_values[9][0]
# 	TGA_Data['Heating Rate'] = row_values[10]
# 	TGA_Data['Max Drying Time'] = row_values[11]
# 	TGA_Data['Equil Crit'] = row_values[12]
# 	TGA_Data['Run Temp'] = row_values[13]
# 	TGA_Data['Max Equil Time'] = row_values[14]
# 	TGA_Data['Equil Crit'] = row_values[15]
# 	TGA_Data['Pres Steps'] = row_values[16]
# 	TGA_Data['Data Logging Interval'] = row_values[17]
# 	TGA_Data['Expt Started'] = row_values[18]
# 	TGA_Data['Run Started'] = row_values[19]



# 	TGA_Data['Elap Time'] = {}
# 	TGA_Data['Elap Time']['unit'] = 'min'
# 	TGA_Data['Elap Time']['value'] = 355.7

# 	if rownum == 22:
# 		TGA_Measurements = []
	
# 	# if rownum >= 24:
# 	# 	TGA_raw_Data = {}
# 	# 	for column in sh.column_values(rownum):
# 	# 		row_values = sh.row_values(rownum) #column_values i think.

# 	j = json.dumps(TGA_Data)

# 	with open('data.json', 'w') as f:
# 			f.write(j)


