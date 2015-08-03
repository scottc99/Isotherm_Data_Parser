import numpy as np
import glob, os
import simplejson as json 
import re

class TGA_Analyse:
	def __init__(self):

		self.ADS_aliqMain = []
		self.DES_aliqMain = []

		self.origin_blanks = []
		self.origin_aliqs = []

		# blanks data
		self.ads_blank = []
		self.des_blank = []

		# aliqs data
		self.ads_aliq = []
		self.des_aliq = []

		# diff blanks data
		self.diff_ads_blank = []
		self.diff_des_blank = []
		self.diff_ads_blank2 = []
		self.diff_des_blank2 = []

		# diff aliqs data
		self.diff_ads_aliq = []
		self.diff_des_aliq = []
		self.diff_ads_aliq2 = []
		self.diff_des_aliq2 = []

		# average blanks data
		self.average_ads_blank = []
		self.average_des_blank = []
		
		# average aliqs data
		self.average_ads_aliq = []
		self.average_des_aliq = []

		# average diffs blanks data
		self.average_diff_ads_blank = []
		self.average_diff_des_blank = []

		# average diffs aliqs data
		self.average_diff_ads_aliq = []
		self.average_diff_des_aliq = []

		# corrected aliqs
		self.corrected_ads_aliq = []
		self.corrected_des_aliq = []

		# corrected average aliqs data
		self.average_corrected_ads_aliq = []
		self.average_corrected_des_aliq = []


	def load(self):
		# blanks = []
		# alisqs = []
		os.chdir(os.path.dirname(os.getcwd()))
		

		index = 0
		for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
			aliqPart = file.split("/")[-1]
			find_aliq = re.search('Aliq3', aliqPart)
				
			if find_aliq:
				content = None
				with open(file, "r") as aliq_file:
					content = aliq_file.read()
					raw = json.loads(content)
					# alisqs.append(raw)
					blocks = self.split(raw, run = 0)
					
					self.ads_aliq.append(blocks[0])
					self.des_aliq.append(blocks[1])
					filePart = file.split("/")[-1].split("_")[:4]
					
					aliqLabel = '_'.join(filePart)
					self.origin_aliqs.append(aliqLabel)

					index += 1
					print file
		# os.chdir(os.path.dirname(os.getcwd()))
		index = 0
		for file in glob.glob("TGA/Data_Files/JSON/json_blankRuns/*.json"):
			content = None
			with open(file, "r") as blank_file:
				content = blank_file.read()

				raw = json.loads(content)
				# blanks.append(raw)
				blocks = self.split(raw, run = 1)
				self.ads_blank.append(blocks[0])
				self.des_blank.append(blocks[1])
				filePart = file.split("/")[-1].split("_")[:4]
				
				blankLabel = '_'.join(filePart)
				self.origin_blanks.append(blankLabel)
				
				index += 1

	def split(self, raw, run):

		begin3 = 1

		pressure_list = []
		conc_list = []

		
		while True: 
			try:
				content= raw["content"][begin3 - 1]				

				if run == 0: 
					conc_dict = content.get('weights')[3] # Before it was 3 but corrected to 4th and now second	
				elif run == 1:
					conc_dict = content.get('weights')[4]
				elif run == 2:
					conc_dict = content.get('weights')[2]

				conc_val = conc_dict.get('value')

				pressure_dict = content.get('pressure')
				pressure_val = pressure_dict.get('value')

				pressure_list.append(pressure_val)
				conc_list.append(conc_val)
					
				begin3 +=1

			except:
				break

		total = len(pressure_list) + 1

		corr_pres_index = pressure_list.index(max(pressure_list))
		corr_conc_value = conc_list[corr_pres_index]

		pressure_list1 = []
		conc_list1 = []

		pressure_list2 = []
		conc_list2 = []
		
		boundary = -1
		for t in range(total):
			if t == total - 1:
				break
			elif t > 0:
				if pressure_list[t] >= pressure_list[t + 1] and pressure_list[t] >= pressure_list[t - 1]:
					boundary = t
					break
				if pressure_list[t] <= pressure_list[t + 1] and pressure_list[t] <= pressure_list[t - 1]:
					boundary = t
					break

		pressure_list1 = list(pressure_list[0:boundary])
		pressure_list2 = list(pressure_list[boundary + 1:len(pressure_list) - 1])

		conc_list1 = list(conc_list[0:boundary])
		conc_list2 = list(conc_list[boundary + 1:len(conc_list) - 1])

		if max(pressure_list1) != max(pressure_list):  
			pressure_list1.append(max(pressure_list))
			conc_list1.append(corr_conc_value)

		return [[pressure_list1, conc_list1], [pressure_list2, conc_list2]]

	# x array to interpolate
	# The sampling.
	def align(self, dataX, dataXY, reverse=False):
		# print "dataX+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(dataX)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataX"

		# print "dataXY+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(dataXY)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataXY"

		self.UNDEF = -99.0

		if reverse:
			self.aligned = list(reversed(np.interp(list(reversed(dataX)), list(reversed(dataXY[0])), list(reversed(dataXY[1])))))
			
		else:
			self.aligned = list(np.interp(dataX, dataXY[0], dataXY[1]))
		
		# print "self.aligned++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.aligned)
		# print "++++++++++++++++++++++++++++++++++++++++++++++++self.aligned"

		return self.aligned

	def diff(self, dataY1, dataY2):
		dataSub = np.array(dataY1) - np.array(dataY2)
		return [abs(data) for data in list(dataSub)]

	def average(self, dataY):
		# print "dataY+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(dataY)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataY"
		averageY = [0.00 for d in dataY[0]]
		for data in dataY:
			for index in range(len(data)):
				averageY[index] += data[index]

		average = [float(d/len(averageY)) for d in averageY]

		# print "average+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(len(averageY) - 1)
		# print json.dumps(averageY)
		# print json.dumps(average)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average"

		return average


	def analyseBlank(self):
		##
		## self.average_ads_blank, self.average_des_blank, self.diff_ads_blank, self.diff_des_blank
		##
		#Total Average computations
		#Asbsorption align
		refPressure = None
		self.aligned_ads_blank = []
		
		#Determine the reference
		if len(self.ads_blank) > 0:
			refPressure = []
			for index in range(len(self.ads_blank[0][0])):
				value = [val[0][index] for val in self.ads_blank]
				avg_value = sum(value)/len(self.ads_blank)
				refPressure.append(avg_value)

		#Align all the rest

		for index in range(len(self.ads_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.ads_blank[index]))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_ads_blank.append([refPressure, x1])
		
		self.aligned_average = []
		for index in range(len(self.aligned_ads_blank[0][1])):
			value = [val[1][index] for val in self.aligned_ads_blank]
			avg_value = sum(value)/len(self.aligned_ads_blank)
			self.aligned_average.append(avg_value)
		
		self.average_ads_blank = [refPressure, self.aligned_average]

		#Desorbtion align
		refPressure = None
		self.aligned_des_blank = []
		
		#Determine the reference
		if len(self.des_blank) > 0:
			refPressure = []
			for index in range(len(self.des_blank[0][0])):
				value = [val[0][index] for val in self.des_blank]
				avg_value = sum(value)/len(self.des_blank)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.des_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.des_blank[index], True))

			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_des_blank.append([refPressure, x1])
		
		self.aligned_average = []
		for index in range(len(self.aligned_des_blank[0][1])):
			value = [val[1][index] for val in self.aligned_des_blank]
			avg_value = sum(value)/len(self.aligned_des_blank)
			self.aligned_average.append(avg_value)
		
		self.average_des_blank = [refPressure, self.aligned_average]
	
		##
		#Comabinatorial diff computations

		line = [0 for x in xrange(len(self.ads_blank))]
		already = [line[:] for x in xrange(len(self.ads_blank))]

		for indexI in range(0, len(self.ads_blank)):
			for indexJ in range(0, len(self.ads_blank)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
			
						# print x2
						interpolateK = self.align(self.ads_blank[indexJ][0], self.ads_blank[indexI])
						diffJK = self.diff(self.ads_blank[indexJ][1], interpolateK)
						
						
						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (6*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_ads_blank.append({'i':indexI, 'j':indexJ, 'diff':[self.ads_blank[indexJ][0], diffJK]})
		
	
		# print "diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_ads_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_ads_blank"

		line = [0 for x in xrange(len(self.des_blank))]
		already = [line[:] for x in xrange(len(self.des_blank))]

		for indexI in range(0, len(self.des_blank)):
			for indexJ in range(0, len(self.des_blank)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
						# Computing self.des_blank[indexI] - self.des_blank[indexJ]
						# self.des_blank[indexJ] as to be self.aligned.

						interpolateK = self.align(self.des_blank[indexJ][0], self.des_blank[indexI], True)
						diffJK = self.diff(self.des_blank[indexJ][1], interpolateK)

						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (6*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_des_blank.append({'i':indexI, 'j':indexJ, 'diff':[self.des_blank[indexJ][0], diffJK]})		
							
		# print "diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_des_blank"
		
		
		##
		#Average diff computations
		#Asbsorption align
		refPressure = None
		self.aligned_ads_blank = []

		#Determine the reference
		if len(self.diff_ads_blank) > 0:
			refPressure = []
			for index in range(len(self.diff_ads_blank[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_ads_blank]
				avg_value = sum(value)/len(self.diff_ads_blank)
				refPressure.append(avg_value)
			
		#Align all the rest
		for index in range(len(self.diff_ads_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_ads_blank[index]['diff']))
			self.aligned_ads_blank.append([refPressure, x1])

		self.aligned_average = []
		for index in range(len(self.aligned_ads_blank[0][1])):
			value = [val[1][index] for val in self.aligned_ads_blank]
			avg_value = sum(value)/len(self.aligned_ads_blank)
			self.aligned_average.append(avg_value)
		
		self.average_diff_ads_blank = [refPressure, self.aligned_average]

		# print self.average_diff_ads_blank

#######################################################################################
#######################################################################################

		#Desorbtion align
		refPressure= None
		self.aligned_des_blank = []

		#Determine the reference
		if len(self.diff_des_blank) > 0:
			refPressure = []
			for index in range(len(self.diff_des_blank[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_des_blank]
				avg_value = sum(value)/len(self.diff_des_blank)
				refPressure.append(avg_value)
			
		#Align all the rest
		for index in range(len(self.diff_des_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_des_blank[index]['diff'], True))
			self.aligned_des_blank.append([refPressure, x1])

		self.aligned_average = []
		for index in range(len(self.aligned_des_blank[0][1])):
			value = [val[1][index] for val in self.aligned_des_blank]
			avg_value = sum(value)/len(self.aligned_des_blank)
			self.aligned_average.append(avg_value)
		
		self.average_diff_des_blank = [refPressure, self.aligned_average]
	

		# print "average_diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_diff_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_des_blank"

	

	def analyseAliq(self):
		##
		## self.average_ads_aliq, self.average_des_aliq, self.diff_ads_aliq, self.diff_des_aliq
		##
		#Total Average computations
		#Asbsorption align
		refPressure= None
		self.aligned_ads_aliq = []

		#Determine the reference
		if len(self.ads_aliq) > 0:
			refPressure = []
			for index in range(len(self.ads_aliq[0][0])):
				value = [val[0][index] for val in self.ads_aliq]
				avg_value = sum(value)/len(self.ads_aliq)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.ads_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.ads_aliq[index]))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_ads_aliq.append([refPressure, x1])
		
		self.aligned_average = []
		for index in range(len(self.aligned_ads_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_ads_aliq]
			avg_value = sum(value)/len(self.aligned_ads_aliq)
			self.aligned_average.append(avg_value)
		
		self.average_ads_aliq = [refPressure, self.aligned_average]

#######################################################################################
#######################################################################################

		#Desorbtion align
		refPressure = None
		self.aligned_des_aliq = []
		
		#Determine the reference
		if len(self.des_aliq) > 0:
			refPressure = []
			for index in range(len(self.des_aliq[0][0])):
				value = [val[0][index] for val in self.des_aliq]
				avg_value = sum(value)/len(self.des_aliq)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.des_aliq)):
			x1 = []

			x1.extend(self.align(refPressure, self.des_aliq[index], True))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_des_aliq.append([refPressure, x1])
		
		self.aligned_average = []
		for index in range(len(self.aligned_des_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_des_aliq]
			avg_value = sum(value)/len(self.aligned_des_aliq)
			self.aligned_average.append(avg_value)
		
		self.average_des_aliq = [refPressure, self.aligned_average]
			
		##
		#Comabinatorial diff computations

		line = [0 for x in xrange(len(self.ads_aliq))]
		already = [line[:] for x in xrange(len(self.ads_aliq))]

		for indexI in range(0, len(self.ads_aliq)):
			for indexJ in range(0, len(self.ads_aliq)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
						# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
						# self.ads_aliq[indexJ] as to be self.aligned.

						interpolateK = self.align(self.ads_aliq[indexJ][0], self.ads_aliq[indexI])
						diffJK = self.diff(self.ads_aliq[indexJ][1], interpolateK)

						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (12*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_ads_aliq.append({'i':indexI, 'j':indexJ, 'diff':[self.ads_aliq[indexJ][0], diffJK]})
				

		# print "diff_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_ads_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_ads_aliq"

		line = [0 for x in xrange(len(self.des_aliq))]
		already = [line[:] for x in xrange(len(self.des_aliq))]

		for indexI in range(0, len(self.des_aliq)):
			for indexJ in range(0, len(self.des_aliq)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
						# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
						# self.ads_aliq[indexJ] as to be self.aligned.
						# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
						# self.ads_aliq[indexJ] as to be self.aligned.
						interpolateK = self.align(self.des_aliq[indexJ][0], self.des_aliq[indexI], True)
						diffJK = self.diff(self.des_aliq[indexJ][1], interpolateK)

						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (12*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_des_aliq.append({'i':indexI, 'j':indexJ, 'diff':[self.des_aliq[indexJ][0], diffJK]})

	
		##
		#Average diff computations
		#Asbsorption align
		refPressure = None
		self.aligned_diff_ads_aliq = []

		#Determine the reference
		if len(self.diff_ads_aliq) > 0:
			refPressure = []
			for index in range(len(self.diff_ads_aliq[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_ads_aliq]
				avg_value = sum(value)/len(self.diff_ads_aliq)
				refPressure.append(avg_value)
			
		#Align all the rest
		for index in range(len(self.diff_ads_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_ads_aliq[index]['diff']))
			self.aligned_diff_ads_aliq.append([refPressure, x1])

		self.aligned_average = []
		for index in range(len(self.aligned_ads_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_ads_aliq]
			avg_value = sum(value)/len(self.aligned_ads_aliq)
			self.aligned_average.append(avg_value)
		
		self.average_diff_ads_aliq = [refPressure, self.aligned_average]

		# print self.average_diff_ads_aliq

#######################################################################################
#######################################################################################

		#Desorbtion align
		refPressure= None
		self.aligned_diff_des_aliq = []

		#Determine the reference
		if len(self.diff_des_aliq) > 0:
			refPressure = []
			for index in range(len(self.diff_des_aliq[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_des_aliq]
				avg_value = sum(value)/len(self.diff_des_aliq)
				refPressure.append(avg_value)
			
		#Align all the rest
		for index in range(len(self.diff_des_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_des_aliq[index]['diff'], True))
			self.aligned_diff_des_aliq.append([refPressure, x1])

		self.aligned_average = []
		for index in range(len(self.aligned_des_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_des_aliq]
			avg_value = sum(value)/len(self.aligned_des_aliq)
			self.aligned_average.append(avg_value)
		
		self.average_diff_des_aliq = [refPressure, self.aligned_average]

########################### Convert aliq units -> blank units ######################################
		
	def mainPlots(self):
		index = 0
		for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
			
			content = None
			with open(file, "r") as aliq_file:
				content = aliq_file.read()

				raw = json.loads(content)
				# alisqs.append(raw)
				blocks = self.split(raw, run = 2)
				
				self.ADS_aliqMain.append(blocks[0])
				self.DES_aliqMain.append(blocks[1])
				
				index += 1

############################ Adsorption: Aliq3 ###############################

		refPressure = self.aligned_ads_aliq[0][0]
		
		self.ADSaliq3_list = []
		self.ADSaligned_aliq3_weight2_vals = []
		self.ADSaligned_aliq3_norm_list = []

		self.ADSdelta_mass_aliq3_list = []
		self.ADSdelta_mass_aliq3_list2 = []
		self.ADSdelta_mass_aliq3_listMain = []
		self.ADSdelta_mass_aliq3_listAvg = []
		self.ADSdelta_mass_aliq3_listDiff = []
		self.ADSaliq3_ads_list_BlankCorr = []
		self.ADSaliq3_ads_list = []


		for x in range(len(self.aligned_ads_aliq)):
			
			self.ADSaligned_aliq3_weight2_vals.extend([self.align(refPressure, self.ADS_aliqMain[x])])
			self.ADSaligned_aliq3_norm_list.extend([self.aligned_ads_aliq[x][1]])


			for y in range(len(self.ADSaligned_aliq3_norm_list[0])):
				i = self.ADSaligned_aliq3_weight2_vals[x][y]
				j = self.ADSaligned_aliq3_norm_list[x][y]
				self.ADSdelta_mass_val = (i*j)/100
				self.ADSdelta_mass_aliq3_list.append(self.ADSdelta_mass_val)
		self.ADSdelta_mass_aliq3_list2.extend(self.ADSdelta_mass_aliq3_list)
		
		for index in range(0, len(self.ADSdelta_mass_aliq3_list2), len(self.ADSaligned_aliq3_norm_list[0])):
			begin = index 
			boundary = index + len(self.ADSaligned_aliq3_norm_list[0])
			
			self.ADSdelta_mass_aliq3_listMain.append(self.ADSdelta_mass_aliq3_list2[begin:boundary])
		
		for index in range(len(self.ADSaligned_aliq3_norm_list[0])):
				value = [val[index] for val in self.ADSdelta_mass_aliq3_listMain]
				avg_value = sum(value)/len(self.ADSdelta_mass_aliq3_listMain)
				self.ADSdelta_mass_aliq3_listAvg.append(avg_value)
		
		for index in range(len(self.average_ads_blank[1])):
			x = self.ADSdelta_mass_aliq3_listAvg[index]
			y = self.average_ads_blank[1][index]
			diff = (x - y)
			self.ADSdelta_mass_aliq3_listDiff.append(diff)

		self.ADSaliq3_ads_list_BlankCorr = [refPressure, self.ADSdelta_mass_aliq3_listDiff]
		self.ADSaliq3_ads_list = [refPressure, self.ADSdelta_mass_aliq3_listAvg]

############################ Desorption: Aliq3 ###############################

		refPressure = self.aligned_des_aliq[0][0]
		
		self.DESaliq3_list = []
		self.DESaligned_aliq3_weight2_vals = []
		self.DESaligned_aliq3_norm_list = []

		self.DESdelta_mass_aliq3_list = []
		self.DESdelta_mass_aliq3_list2 = []
		self.DESdelta_mass_aliq3_listMain = []
		self.DESdelta_mass_aliq3_listAvg = []
		self.DESdelta_mass_aliq3_listDiff = []
		self.DESaliq3_des_list_BlankCorr = []
		self.DESaliq3_des_list = []

		for x in range(len(self.aligned_des_aliq)):
			self.DESaligned_aliq3_weight2_vals.extend([self.align(refPressure, self.DES_aliqMain[x])])
			self.DESaligned_aliq3_norm_list.extend([self.aligned_des_aliq[x][1]])
			
			for y in range(len(self.DESaligned_aliq3_norm_list[0])):
				i = self.DESaligned_aliq3_weight2_vals[x][y]
				j = self.DESaligned_aliq3_norm_list[x][y]
				self.DESdelta_mass_val = (i*j)/100
				self.DESdelta_mass_aliq3_list.append(self.DESdelta_mass_val)
		self.DESdelta_mass_aliq3_list2.extend(self.DESdelta_mass_aliq3_list)
		
		for index in range(0, len(self.DESdelta_mass_aliq3_list2), len(self.DESaligned_aliq3_norm_list[0])):
			begin = index 
			boundary = index + len(self.DESaligned_aliq3_norm_list[0])
			
			self.DESdelta_mass_aliq3_listMain.append(self.DESdelta_mass_aliq3_list2[begin:boundary])
		
		for index in range(len(self.DESaligned_aliq3_norm_list[0])):
				value = [val[index] for val in self.DESdelta_mass_aliq3_listMain]
				avg_value = sum(value)/len(self.DESdelta_mass_aliq3_listMain)
				self.DESdelta_mass_aliq3_listAvg.append(avg_value)
		
		for index in range(len(self.average_des_blank[1])):
			x = self.DESdelta_mass_aliq3_listAvg[index]
			y = self.average_des_blank[1][index]
			diff = (x - y)
			self.DESdelta_mass_aliq3_listDiff.append(diff)

		self.DESaliq3_des_list_BlankCorr = [refPressure, self.DESdelta_mass_aliq3_listDiff]
		self.DESaliq3_des_list = [refPressure, self.DESdelta_mass_aliq3_listAvg]


########################### Convert aliq3/aliq3  ######################################



	def analyseAll(self):
		self.analyseAliq()
		self.analyseBlank()
		self.mainPlots()
		# self.average_ads_blank 
		# self.average_des_blank
		# self.average_diff_ads_blank
		# self.average_diff_des_blank

		# self.average_ads_aliq
		# self.average_des_aliq
		# self.average_diff_ads_aliq
		# self.average_diff_des_aliq


		








