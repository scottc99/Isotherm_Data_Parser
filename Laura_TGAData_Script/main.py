#### Script for first set of rowList from TGA (machine 1) ####

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
		self.sh = None
		self.root = Tk()
		self.label = Label(self.root, text = "Enter Sheet Number")
		self.label.pack()

		self.entry = Entry(self.root)
		self.entry.pack()

		self.button = Button(self.root, text = "Load", command = self.load_sheet)
		self.button.pack()

	def load_sheet(self):
		self.sheet = self.entry.get()
		print "Sheet No: %s"%self.sheet
		if self.sheet.__class__ == type(""):
			
			self.sh = self.wb.sheet_by_index(int(self.sheet) - 1)
			self.button2 = Button(self.root, text = "Init JSON Transfer", command = self.runJSON)
			self.button2.pack()
			
		else:
			print 'Eee Roar!'

	def run(self):
		print "Please select a file"
		file_path = tkFileDialog.askopenfilename()
		self.wb = xlrd.open_workbook(filename = file_path)
		self.root.mainloop()



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
	def runJSON(self):
	
		TGA_rowDict = {}
		
		for rownum in xrange(1,self.sh.nrows):
			
			row_values = self.sh.row_values(rownum)
			TGA_rowDict['File Name'] = (row_values)
			TGA_rowDict['Experiment'] = (row_values)
			TGA_rowDict['Operator'] = (row_values)
			TGA_rowDict['Experiment ID'] = (row_values)
			TGA_rowDict['Sample Name'] = (row_values)
			TGA_rowDict['Sample Lot #'] = (row_values)
			TGA_rowDict['Notes'] = (row_values)
			TGA_rowDict[''] = (row_values)
			TGA_rowDict['Adsorbate'] = (row_values)
			TGA_rowDict['Drying Temp'] = (row_values)
			# TGA_rowDict['Drying Temp']['unit' = (ow_values[9)]
			# TGA_rowDict['Drying Temp']['value' = (ow_values[9)]
			TGA_rowDict['Heating Rate'] = (row_values)
			TGA_rowDict['Max Drying Time'] = (row_values)
			TGA_rowDict['Equil Crit'] = (row_values)
			TGA_rowDict['Run Temp'] = (row_values)
			TGA_rowDict['Max Equil Time'] = (row_values)
			TGA_rowDict['Equil Crit'] = (row_values)
			TGA_rowDict['Pres Steps'] = (row_values)
			TGA_rowDict['rowDict Logging Interval'] = (row_values)
			TGA_rowDict['Expt Started'] = (row_values)
			TGA_rowDict['Run Started'] = (row_values)


			# TGA_rowList['Elap Time'] = {}
			# TGA_rowList['Elap Time']['unit'] = 'min'
			# TGA_rowList['Elap Time']['value'] = 355.7

			# if rownum == 22:
			# 	TGA_Measurements = []
			
			# if rownum >= 24:
			# 	TGA_raw_rowList = {}
			# 	for column in sh.column_values(rownum):
			# 		row_values = sh.row_values(rownum) #column_values i think.

			j = json.dumps(TGA_rowDict)

			with open('rowDict.json', 'w') as f:
					f.write(j)
					
		

if __name__ == '__main__':

	TGInstance = TGApp()
	TGInstance.run()
	
	
