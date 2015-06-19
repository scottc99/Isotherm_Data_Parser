#### Script for first set of data from TGA (machine 1) ####

from openpyxl import load_workbook
import os 
import os.path
wb = load_workbook (filename = "8852_DataSet_TGA.xlsx")

print wb.get_sheet_names()

