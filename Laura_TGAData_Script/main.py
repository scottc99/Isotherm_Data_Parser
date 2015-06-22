#### Script for first set of data from TGA (machine 1) ####

import os
import xlrd
from collections import OrderedDict
from dialog import Dialog
import simplejson as json 
import Tkinter as Tk
import tkFileDialog
import tkSimpleDialog

root = Tk.Tk()
root.withdraw()

print "Please select a file"
file_path = tkFileDialog.askopenfilename()
wb = xlrd.open_workbook(filename = file_path)

class Sheet_Dialog(tkSimpleDialog.Dialog):
	
	def body(self,master):

		Label(master, text="Sheet_Number:").grid(row=0)
		self.e1 = Entry(master)	
		
		self.e1.grid(row=0, column=1)
		return self.e1

	def apply(self):
		first = int(self.e1.get())
		for x in range (1,n):
			if x == self.e1:
				sh = wb.sheet_by_index(int(int(x)-1))
		return first 

		


