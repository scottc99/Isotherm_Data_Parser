#### Script for first set of data from TGA (machine 1) ####
from openpyxl import load_workbook
wb = load_workbook(filename = 8852_DataSet_TGA) 

print wb.get_sheet_names()

