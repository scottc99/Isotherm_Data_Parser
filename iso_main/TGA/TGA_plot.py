#### Script for plotting machine produced data ####

#### TGA (machine 1) ####

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
import TGA_fileConvert


class simplePlotsTGA(): 

	def __init__(self):

		self.root = "I think I'm an instance"

		if sequence3 == '8852':
			self.adsAliqMainList = adsMainList
			self.desAliqMainList = desMainList
			
			self.aliqPlotVals(start1)
			self.plotSimpleAliq

		else: 
			self.adsBlankMainList = adsMainList
			self.desBlankMainList = desMainList

			self.blankPlotVals(start2)
			self.plotSimpleBlank


	def aliqPlotVals(self, firstNum):
		self.adsAliqIndivList = self.adsAliqMainList[firstNum]
		
		self.adsAliqPresVals = self.adsAliqIndivList[0]
		self.adsAliqConcVals = self.adsAliqIndivList[1]
	
		self.desAliqIndivList = self.desAliqMainList[firstNum]

		self.desAliqPresVals = self.desAliqPresList[0]
		self.desAliqConcVals = self.desAliqConcList[1]

	def blankPlotVals(self, firstNum):
		self.adsBlankIndivList = self.adsBlankMainList[firstNum]

		self.adsBlankPresVals = self.adsBlankIndivList[0]
		self.adsBlankConcVals = self.adsBlankIndivList[1]
	
		self.desBlankIndivList = self.desBlankMainList[firstNum]
		
		self.desBlankPresVals = self.desBlankPresList[0]
		self.desBlankConcVals = self.desBlankConcList[1]

		
	def plotSimpleAliq(self):
		plt.figure(indexAliq)
		plt.plot(self.adsAliqPresVals, self.adsAliqConcVals, mfc = 'r', mew = .25)
		plt.plot(self.desAliqPresVals, self.desAliqConcVals, mfc = 'b', mew = .25)
		
		plot_AliqPath = '%s/TGA/TGA_plots/Aliq_plots/Simple_plots/%s_simplePlot_%s.png'\
							 %(os.getcwd(), sequence1, indexAliq)
		plt.savefig('%s'%plot_simplePath)


	def plotSimpleBlank(self):
		plt.figure(indexBlank)
		plt.plot(self.adsPresVals, self.adsConcVals, mfc = 'r', mew = .25)
		plt.plot(self.desPresVals, self.desConcVals,  mfc = 'b', mew = .25)
		
		plot_blankPath = '%s/TGA/TGA_plots/Blank_plots/Simple_plots/%s_simplePlot_%s.png'\
							 %(os.getcwd(), sequence1, indexBlank)
		plt.savefig('%s'%plot_blankPath)

		start2 += 1
		indexBlank += 1

# class multiPlotsTGA	
	
# 	def plotMany(self):


if __name__ == '__main__':

	os.chdir(os.path.dirname(os.getcwd()))

	start1 = 0
	start2 = 0
	indexBlank = 1
	indexAliq = 1

	while True:
		try:
			for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
				sequence1 = file.split("/")[-1].split("_")[0]
				sequence2 = file.split("/")[-1].split("_")[1]
				sequence3 = file.split("/")[-1].split("_")[2]

				json_aliqPathTGA = file

				with open('%s'%json_aliqPathTGA) as json_aliqDataTGA:    
					json_aliqDictTGA = json.load(json_aliqDataTGA)


				begin3 = 1

				pressureAliq_listTGA = []
				concAliq_listTGA = []


				while True: 
					try:
						contentAliq_dictTGA = json_AliqDictTGA["content"][begin3 - 1]

						concAliq_dictTGA = contentAliq_dictTGA.get('weights')[4]
						concAliq_valTGA = concAliq_dictTGA.get('value')

						pressureAliq_dictTGA = contentAliq_dictTGA.get('pressure')
						pressureAliq_valTGA = pressureAliq_dictTGA.get('value')

						pressureAliq_listTGA.append(pressure_valTGA)
						concAliq_listTGA.append(conc_valTGA)
							
						begin3 +=1

					except:
						break


				total = len(pressureAliq_listTGA)

				pressureAliq_listTGA1 = []
				concAliq_listTGA1 = []

				pressureAliq_listTGA2 = []
				concAliq_listTGA2 = []
				
				boundary = -1
				for t in range(total):
					if t == total - 1:
						break
					elif t > 0:
						if pressureAliq_listTGA[t] >= pressureAliq_listTGA[t + 1] and pressureAliq_listTGA[t] >= pressureAliq_listTGA[t - 1]:
							boundary = t
							break
						if pressureAliq_listTGA[t] <= pressureAliq_listTGA[t + 1] and pressureAliq_listTGA[t] <= pressureAliq_listTGA[t - 1]:
							boundary = t
							break

				pressureAliq_listTGA1 = list(pressureAliq_listTGA[0:boundary])
				pressureAliq_listTGA2 = list(pressureAliq_listTGA[boundary + 1:len(pressureAliq_listTGA) - 1])

				concAliq_listTGA1 = list(concAliq_listTGA[0:boundary])
				concAliq_listTGA2 = list(concAliq_listTGA[boundary + 1:len(concAliq_listTGA) - 1])
				
				TGhay = simplePlotsTGA()
				TGhay.root.mainloop()
				self.root.mainloop()
				
				self.root.destroy()

				start1 += 1
				indexAliq += 1

		except:
			for file in glob.glob("TGA/Data_Files/JSON/json_blankRuns/*.json"):
				sequence1 = file.split("/")[-1].split("_")[0]
				sequence2 = file.split("/")[-1].split("_")[1]
				sequence3 = file.split("/")[-1].split("_")[2]

				json_blankPathTGA = file

				with open('%s'%json_blankPathTGA) as json_blankDataTGA:    
					json_blankDictTGA = json.load(json_blankDataTGA)


				begin4 = 1

				pressureBlank_listTGA = []
				concBlank_listTGA = []


				while True: 
					try:
						contentBlank_dictTGA = json_BlankDictTGA["content"][begin4 - 1]

						concBlank_dictTGA = contentBlank_dictTGA.get('weights')[4]
						concBlank_valTGA = concBlank_dictTGA.get('value')

						pressureBlank_dictTGA = contentBlank_dictTGA.get('pressure')
						pressureBlank_valTGA = pressureBlank_dictTGA.get('value')

						pressureBlank_listTGA.append(pressureBlank_valTGA)
						concBlank_listTGA.append(concBlank_valTGA)
							
						begin4 +=1

					except:
						break


				total = len(pressureBlank_listTGA)

				pressureBlank_listTGA1 = []
				concBlank_listTGA1 = []

				pressureBlank_listTGA2 = []
				concBlank_listTGA2 = []
				
				boundary = -1
				for t in range(total):
					if t == total - 1:
						break
					elif t > 0:
						if pressureBlank_listTGA[t] >= pressureBlank_listTGA[t + 1] and pressureBlank_listTGA[t] >= pressureBlank_listTGA[t - 1]:
							boundary = t
							break
						if pressureBlank_listTGA[t] <= pressureBlank_listTGA[t + 1] and pressureBlank_listTGA[t] <= pressureBlank_listTGA[t - 1]:
							boundary = t
							break

				pressureBlank_listTGA1 = list(pressureBlank_listTGA[0:boundary])
				pressureBlank_listTGA2 = list(pressureBlank_listTGA[boundary + 1:len(pressureBlank_listTGA) - 1])

				concBlank_listTGA1 = list(concBlank_listTGA[0:boundary])
				concBlank_listTGA2 = list(concBlank_listTGA[boundary + 1:len(concBlank_listTGA) - 1])
				
				TGhay = simplePlotsTGA()
				TGhay.root.mainloop()
				self.root.mainloop()
				
				self.root.destroy()

				start2 += 1
				indexBlank += 1
			




