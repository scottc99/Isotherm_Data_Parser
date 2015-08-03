import numpy as np
import glob, os
import simplejson as json 
import re

class TGA_Analyse:
	def __init__(self):

		self.DESmaster_list_blankCorr = []
		self.DESmaster_list_raw = []

		self.DESmaster_list_blankCorr = []
		self.DESmaster_list_raw = []

		self.DES_aliqMain = []
		self.DES_aliqMain = []

		self.origin_blanks = []
		self.origin_aliqs = []

		# blanks data
		self.DES_blank = []
		self.des_blank = []

		# aliqs data
		self.DES_aliq = []
		self.des_aliq = []

		# diff blanks data
		self.diff_DES_blank = []
		self.diff_des_blank = []
		self.diff_DES_blank = []
		self.diff_des_blank = []

		# diff aliqs data
		self.diff_DES_aliq = []
		self.diff_des_aliq = []
		self.diff_DES_aliq2 = []
		self.diff_des_aliq2 = []

		# average blanks data
		self.average_DES_blank = []
		self.average_des_blank = []
		
		# average aliqs data
		self.average_DES_aliq = []
		self.average_des_aliq = []

		# average diffs blanks data
		self.average_diff_DES_blank = []
		self.average_diff_des_blank = []

		# average diffs aliqs data
		self.average_diff_DES_aliq = []
		self.average_diff_des_aliq = []

		# corrected aliqs
		self.corrected_DES_aliq = []
		self.corrected_des_aliq = []

		# corrected average aliqs data
		self.average_corrected_DES_aliq = []
		self.average_corrected_des_aliq = []


	def load(self):
		# blanks = []
		# alisqs = []
		os.chdir(os.path.dirname(os.getcwd()))
		

		index = 0
		for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
			aliqPart = file.split("/")[-1]
			find_aliq = re.search('Aliq2', aliqPart)
				
			if find_aliq:
				content = None
				with open(file, "r") as aliq_file:
					content = aliq_file.read()
					raw = json.loads(content)
					# alisqs.append(raw)
					blocks = self.split(raw, run = 0)
					
					self.DES_aliq.append(blocks[0])
					self.des_aliq.append(blocks[1])
					filePart = file.split("/")[-1].split("_")[:4]
					
					aliqLabel = '_'.join(filePart)
					self.origin_aliqs.append(aliqLabel)

					index += 1
					
		# os.chdir(os.path.dirname(os.getcwd()))
		index = 0
		for file in glob.glob("TGA/Data_Files/JSON/json_blank/*.json"):
			content = None
			with open(file, "r") as blank_file:
				content = blank_file.read()

				raw = json.loads(content)
				# blanks.append(raw)
				blocks = self.split(raw, run = 0)
				self.DES_blank.append(blocks[0])
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
		## self.average_DES_blank, self.average_des_blank, self.diff_DES_blank, self.diff_des_blank
		##
		#Total Average computations
		#Asbsorption align
	
		refPressure = None
		self.aligned_DES_blank = []
		
		#Determine the reference
		if len(self.DES_blank) > 0:
			refPressure = []
			for index in range(len(self.DES_blank[0][0])):
				value = [val[0][index] for val in self.DES_blank]
				avg_value = sum(value)/len(self.DES_blank)
				refPressure.append(avg_value)
		
		#Align all the rest
		for index in range(len(self.DES_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.DES_blank[index]))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_DES_blank.append([refPressure, x1])


		# self.aligned_average = []
		# for index in range(len(self.aligned_DES_blank[0][1])):
		# 	value = [val[1][index] for val in self.aligned_DES_blank]
		# 	avg_value = sum(value)/len(self.aligned_DES_blank)
		# 	self.aligned_average.append(avg_value)
		
		# self.average_DES_blank = [refPressure, self.aligned_average]

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
		
		

		# self.aligned_average = []
		# for index in range(len(self.aligned_des_blank[0][1])):
		# 	value = [val[1][index] for val in self.aligned_des_blank]
		# 	avg_value = sum(value)/len(self.aligned_des_blank)
		# 	self.aligned_average.append(avg_value)
		
		# self.average_des_blank = [refPressure, self.aligned_average]

		##
		#Comabinatorial diff computations

		line = [0 for x in xrange(len(self.DES_blank))]
		already = [line[:] for x in xrange(len(self.DES_blank))]

		for indexI in range(0, len(self.DES_blank)):
			for indexJ in range(0, len(self.DES_blank)):

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
						interpolateK = self.align(self.DES_blank[indexJ][0], self.DES_blank[indexI])
						diffJK = self.diff(self.DES_blank[indexJ][1], interpolateK)
						
						
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
							self.diff_DES_blank.append({'i':indexI, 'j':indexJ, 'diff':[self.DES_blank[indexJ][0], diffJK]})
		
	
		# print "diff_DES_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_DES_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_DES_blank"

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
		self.aligned_DES_blank = []

		#Determine the reference
		if len(self.diff_DES_blank) > 0:
			refPressure = []
			for index in range(len(self.diff_DES_blank[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_DES_blank]
				avg_value = sum(value)/len(self.diff_DES_blank)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.diff_DES_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_DES_blank[index]['diff']))
			self.aligned_DES_blank.append([refPressure, x1])

		self.aligned_average = []
		for index in range(len(self.aligned_DES_blank[0][1])):
			value = [val[1][index] for val in self.aligned_DES_blank]
			avg_value = sum(value)/len(self.aligned_DES_blank)
			self.aligned_average.append(avg_value)
		
		self.average_diff_DES_blank = [refPressure, self.aligned_average]

		# print self.average_diff_DES_blank

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
		## self.average_DES_aliq, self.average_des_aliq, self.diff_DES_aliq, self.diff_des_aliq
		##
		#Total Average computations
		#Asbsorption align
		refPressure = None
		self.aligned_DES_aliq = []

		#Determine the reference
		if len(self.DES_aliq) > 0:
			refPressure = []
			for index in range(len(self.DES_aliq[0][0])):
				value = [val[0][index] for val in self.DES_aliq]
				avg_value = sum(value)/len(self.DES_aliq)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.DES_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.DES_aliq[index]))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_DES_aliq.append([refPressure, x1])
		
		# self.aligned_average = []
		# for index in range(len(self.aligned_DES_aliq[0][1])):
		# 	value = [val[1][index] for val in self.aligned_DES_aliq]
		# 	avg_value = sum(value)/len(self.aligned_DES_aliq)
		# 	self.aligned_average.append(avg_value)
			
		# self.average_DES_aliq = [refPressure, self.aligned_average]

#######################################################################################
#######################################################################################

		#Desorbtion align
		refPressure= None
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
		
		##
		#Comabinatorial diff computations

		line = [0 for x in xrange(len(self.DES_aliq))]
		already = [line[:] for x in xrange(len(self.DES_aliq))]

		for indexI in range(0, len(self.DES_aliq)):
			for indexJ in range(0, len(self.DES_aliq)):

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
						# Computing self.DES_aliq[indexI] - self.DES_aliq[indexJ]
						# self.DES_aliq[indexJ] as to be self.aligned.

						interpolateK = self.align(self.DES_aliq[indexJ][0], self.DES_aliq[indexI])
						diffJK = self.diff(self.DES_aliq[indexJ][1], interpolateK)

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
							self.diff_DES_aliq.append({'i':indexI, 'j':indexJ, 'diff':[self.DES_aliq[indexJ][0], diffJK]})
				

		# print "diff_DES_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_DES_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_DES_aliq"

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
						# Computing self.DES_aliq[indexI] - self.DES_aliq[indexJ]
						# self.DES_aliq[indexJ] as to be self.aligned.
						# Computing self.DES_aliq[indexI] - self.DES_aliq[indexJ]
						# self.DES_aliq[indexJ] as to be self.aligned.
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
		self.aligned_diff_DES_aliq = []

		#Determine the reference
		if len(self.diff_DES_aliq) > 0:
			refPressure = []
			for index in range(len(self.diff_DES_aliq[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_DES_aliq]
				avg_value = sum(value)/len(self.diff_DES_aliq)
				refPressure.append(avg_value)
		
		#Align all the rest
		for index in range(len(self.diff_DES_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_DES_aliq[index]['diff']))
			self.aligned_diff_DES_aliq.append([refPressure, x1])

		self.average_diff_DES_aliq = []
		for index in range(len(self.aligned_diff_DES_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_diff_DES_aliq]
			avg_value = sum(value)/len(self.aligned_diff_DES_aliq)
			self.average_diff_DES_aliq.append(avg_value)
	
		self.average_diff_DES_aliq = [refPressure, self.average_diff_DES_aliq]

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

		self.average_diff_des_aliq = []
		for index in range(len(self.aligned_diff_des_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_diff_des_aliq]
			avg_value = sum(value)/len(self.aligned_diff_des_aliq)
			self.average_diff_des_aliq.append(avg_value)
	
		self.average_diff_des_aliq = [refPressure, self.average_diff_des_aliq]
		
########################### Convert aliq units -> blank units ######################################

	# def baliqEatToast(self, sliced): 
	# 	if sliced == 1:	
	# 		for index in range(len(self.DESaligned_aliq2_norm_list1[0])):
	# 			x = self.DESdelta_mass_aliq2_list1[index]
	# 			y = self.new_DES_blank_align1[index]
				
	# 			diff1 = (x - y)
	# 		self.DESdelta_mass_aliq2_listDiff1.append(diff1)
		
	# 	self.DESaliq2_DES_list_BlankCorr1.append([self.DESrefPressure, self.DESdelta_mass_aliq2_listDiff1])
	# 	self.DESaliq2_DES_list1.append([self.DESrefPressure, self.DESdelta_mass_aliq2_list1])

	# 	if sliced == 2:
	# 		for index in range(len(self.DESaligned_aliq2_norm_list1[0])):
	# 			x = self.DESdelta_mass_aliq2_list1[index]
	# 			y = self.new_des_blank_align1[index]
				
	# 			diff2 = (x - y)
	# 		self.DESdelta_mass_aliq2_listDiff1.append(diff2)

	# 	self.DESaliq2_des_list_BlankCorr1.append([self.DESrefPressure, self.DESdelta_mass_aliq2_listDiff1])
	# 	self.DESaliq2_des_list1.append([self.DESrefPressure, self.DESdelta_mass_aliq2_list1])

	# 	if sliced == 3:
	# 		for index in range(len(self.DESaligned_aliq2_norm_list2[0])):
	# 			x = self.DESdelta_mass_aliq2_list2[index]
	# 			y = self.new_DES_blank_align2[index]
				
	# 			diff1 = (x - y)
	# 		self.DESdelta_mass_aliq2_listDiff2.append(diff1)

	# 	self.DESaliq2_DES_list_BlankCorr2.append([self.DESrefPressure, self.DESdelta_mass_aliq2_listDiff2])
	# 	self.DESaliq2_DES_list2.append([self.DESrefPressure, self.DESdelta_mass_aliq2_list2])

	# 	if sliced == 4:
	# 		for index in range(len(self.DESaligned_aliq2_norm_list2[0])):
	# 			x = self.DESdelta_mass_aliq2_list2[index]
	# 			y = self.new_des_blank_align2[index]
				
	# 			diff2 = (x - y)
	# 		self.DESdelta_mass_aliq2_listDiff2.append(diff2)

	# 	self.DESaliq2_des_list_BlankCorr2.append([self.DESrefPressure, self.DESdelta_mass_aliq2_listDiff2])
	# 	self.DESaliq2_des_list2.append([self.DESrefPressure, self.DESdelta_mass_aliq2_list2])

	def DESPlotsCombine(self):

		self.DES_aliqRaw_list = []
		self.DES_aliqBlank1_list = []
		self.DES_aliqBlank2_list = []
		self.DES_aliqBlank_many_list = []

		DESaliq_average = []
		DESblank1_average = []
		DESblank2_average = []

		diff_aliqBlank1_list = []
		diff_aliqBlank2_list = []

		for index in range(len(self.DESdelta_mass_aliq2_listMain[0])):
			
			aliq_value = [val[index] for val in self.DESdelta_mass_aliq2_listMain]
			blank1_value = [val[index] for val in self.DES_Aliq1_blankMain]
			blank2_value = [val[index] for val in self.DES_Aliq2_blankMain]

			aliq_avg_value = sum(aliq_value)/len(self.DESdelta_mass_aliq2_listMain)
			blank1_avg_value = sum(blank1_value)/len(self.DES_Aliq1_blankMain)
			blank2_avg_value = sum(blank2_value)/len(self.DES_Aliq2_blankMain)
			
			DESaliq_average.append(aliq_avg_value)
			DESblank1_average.append(blank1_avg_value)
			DESblank2_average.append(blank2_avg_value)

		self.DES_aliqRaw_list.extend([self.DESrefPressure, DESaliq_average])

		for val in range(len(self.DESdelta_mass_aliq2_listMain[0])):

			xVal = DESaliq_average[val]
			b1Val = DESblank1_average[val]
			b2Val = DESblank2_average[val]

			diff_aliqB1 = (xVal - b1Val)
			diff_aliqB2 = (xVal - b2Val)

			diff_aliqBlank1_list.append(diff_aliqB1)
			diff_aliqBlank2_list.append(diff_aliqB2)

		self.DES_aliqBlank1_list.extend([self.DESrefPressure, diff_aliqBlank1_list])
		self.DES_aliqBlank2_list.extend([self.DESrefPressure, diff_aliqBlank2_list])
		
		self.DES_aliqBlank_many_list.append([self.DES_aliqRaw_list, self.DES_aliqBlank1_list, self.DES_aliqBlank2_list])
		# print self.DES_aliqRaw_list
		# print self.DES_aliqBlank1_list
		# print self.DES_aliqBlank2_list
		# print self.DESrefPressure

	def desPlotsCombine(self):

		self.DES_aliqRaw_list = []
		self.DES_aliqBlank1_list = []
		self.DES_aliqBlank2_list = []
		self.DES_aliqBlank_many_list = []

		DESaliq_average = []
		DESblank1_average = []
		DESblank2_average = []

		diff_aliqBlank1_list = []
		diff_aliqBlank2_list = []

		for index in range(len(self.DESdelta_mass_aliq2_listMain[0])):
			
			aliq_value = [val[index] for val in self.DESdelta_mass_aliq2_listMain]
			blank1_value = [val[index] for val in self.DES_Aliq1_blankMain]
			blank2_value = [val[index] for val in self.DES_Aliq2_blankMain]

			aliq_avg_value = sum(aliq_value)/len(self.DESdelta_mass_aliq2_listMain)
			blank1_avg_value = sum(blank1_value)/len(self.DES_Aliq1_blankMain)
			blank2_avg_value = sum(blank2_value)/len(self.DES_Aliq2_blankMain)
			
			DESaliq_average.append(aliq_avg_value)
			DESblank1_average.append(blank1_avg_value)
			DESblank2_average.append(blank2_avg_value)

		self.DES_aliqRaw_list.extend([self.DESrefPressure, DESaliq_average])

		for val in range(len(self.DESdelta_mass_aliq2_listMain[0])):

			xVal = DESaliq_average[val]
			b1Val = DESblank1_average[val]
			b2Val = DESblank2_average[val]

			diff_aliqB1 = (xVal - b1Val)
			diff_aliqB2 = (xVal - b2Val)

			diff_aliqBlank1_list.append(diff_aliqB1)
			diff_aliqBlank2_list.append(diff_aliqB2)

		self.DES_aliqBlank1_list.extend([self.DESrefPressure, diff_aliqBlank1_list])
		self.DES_aliqBlank2_list.extend([self.DESrefPressure, diff_aliqBlank2_list])

		self.DES_aliqBlank_many_list.append([self.DES_aliqRaw_list, self.DES_aliqBlank1_list, self.DES_aliqBlank2_list])

		# print self.DES_aliqRaw_list
		# print self.DES_aliqBlank1_list
		# print self.DES_aliqBlank2_list
		# print self.DESrefPressure
	
	def mainPlotsAliq(self):
			
		aliqNum = 0
		self.DESdelta_mass_aliq2_listMain = []
		self.DESdelta_mass_aliq2_listMain = []
		for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
			aliqPart = file.split("/")[-1]
			find_aliq = re.search('Aliq2', aliqPart)

			if find_aliq:
			
				content = None
				print aliqNum
				with open(file, "r") as aliq_file:
					content = aliq_file.read()
					raw = json.loads(content)
					blocks = self.split(raw, run = 2)
					# print blocks
					conc_listDES = []
					conc_listDes = []

					for i in range(len(self.DES_aliq[0][0])):
						conc_listDES.append(blocks[0][1][0])
					for j in range(len(self.des_aliq[0][0])):
						conc_listDes.append(blocks[0][1][0])
					# print conc_listDES
					# print conc_listDes
					self.DES_aliqMain.extend([blocks[0][0], conc_listDES])
					self.DES_aliqMain.extend([blocks[1][0], conc_listDes])

############################ DESorption/Desorption: Aliq2 ###############################
					
					self.DESrefPressure = self.aligned_DES_aliq[0][0]
					self.DESrefPressure = self.aligned_des_aliq[0][0]		

					DESaligned_aliq2_weight2_vals = []
					DESaligned_aliq2_norm_list = []
					DESdelta_mass_aliq2_list = []
					# self.DESdelta_mass_aliq2_listMain = []

					DESaligned_aliq2_weight2_vals.extend(self.align(self.DESrefPressure, self.DES_aliqMain))
					DESaligned_aliq2_norm_list.extend(self.aligned_DES_aliq[aliqNum])
					
					for x in range(len(DESaligned_aliq2_norm_list[0])):
						i = DESaligned_aliq2_weight2_vals[x]
						j = DESaligned_aliq2_norm_list[1][x]

						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_aliq2_list.append(DESdelta_mass_val)
					self.DESdelta_mass_aliq2_listMain.append(DESdelta_mass_aliq2_list)

					DESaligned_aliq2_weight2_vals = []
					DESaligned_aliq2_norm_list = []
					DESdelta_mass_aliq2_list = []
					# self.DESdelta_mass_aliq2_listMain = []

					DESaligned_aliq2_weight2_vals.extend(self.align(self.DESrefPressure, self.DES_aliqMain))										
					DESaligned_aliq2_norm_list.extend(self.aligned_des_aliq[aliqNum])
				
					for y in range(len(DESaligned_aliq2_norm_list[0])):
						i = DESaligned_aliq2_weight2_vals[y]
						j = DESaligned_aliq2_norm_list[1][y]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_aliq2_list.append(DESdelta_mass_val)
					self.DESdelta_mass_aliq2_listMain.append(DESdelta_mass_aliq2_list)

			aliqNum += 1
		
		
	def mainPlotsBlank(self):
		
		blankNum1 = 0
		blankNum2 = 0

		self.DES_Aliq1_blankMain = []
		self.DES_Aliq1_blankMain = []
		self.DES_Aliq2_blankMain = []
		self.DES_Aliq2_blankMain = []
		for file in glob.glob("TGA/Data_Files/JSON/json_blank/*.json"):
			blankPart = file.split("/")[-1]
			find_blankAliq1 = re.search('Aliq1', blankPart)
			find_blankAliq2 = re.search('Aliq2', blankPart)
			if find_blankAliq1:

				conc_listBlankDES = []
				conc_listBlankDes = []
				DES_blankMain = []
				DES_blankMain = []

				content = None
				with open(file, "r") as blank_file:
					print "Blank Num1: %s"%blankNum1
					content = blank_file.read()
					raw = json.loads(content)
					blocks = self.split(raw, run = 2)

					for i in range(len(self.DES_aliq[0][0])):
						conc_listBlankDES.append(blocks[0][1][0])
					for j in range(len(self.des_aliq[0][0])):
						conc_listBlankDes.append(blocks[0][1][0])

					DES_blankMain.extend([blocks[0][0], conc_listBlankDES])
					DES_blankMain.extend([blocks[1][0], conc_listBlankDes])
					
# ############################ DESorption: blank ###############################		

					DESaligned_blank_weight2_vals = []
					DESaligned_blank_norm_list = []
					DESdelta_mass_blank_list = []
						
					DESaligned_blank_weight2_vals.extend(self.align(self.DESrefPressure, DES_blankMain))
					DESaligned_blank_norm_list.extend(self.aligned_DES_blank[blankNum1])
				
					for x in range(len(DESaligned_blank_norm_list[0])):
						i = DESaligned_blank_weight2_vals[x]
						j = DESaligned_blank_norm_list[1][x]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_blank_list.append(DESdelta_mass_val)	
					self.DES_Aliq1_blankMain.append(DESdelta_mass_blank_list)

		############################ Desorption: blank ###############################

					DESaligned_blank_weight2_vals = []
					DESaligned_blank_norm_list = []
					DESdelta_mass_blank_list = []
					
					DESaligned_blank_weight2_vals.extend(self.align(self.DESrefPressure, DES_blankMain))										
					DESaligned_blank_norm_list.extend(self.aligned_des_blank[blankNum1])
					
					for y in range(len(DESaligned_blank_norm_list[0])):
						
						i = DESaligned_blank_weight2_vals[y]
						j = DESaligned_blank_norm_list[1][y]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_blank_list.append(DESdelta_mass_val)
					self.DES_Aliq1_blankMain.append(DESdelta_mass_blank_list)

				blankNum1 += 1		

			if find_blankAliq2:
				
				conc_listBlankDES = []
				conc_listBlankDes = []
				DES_blankMain = []
				DES_blankMain = []
				
				content = None
				with open(file, "r") as blank_file:
					print "Blank Num2: %s"%blankNum2
					content = blank_file.read()
					raw = json.loads(content)
					blocks = self.split(raw, run = 2)

					for i in range(len(self.DES_aliq[0][0])):
						conc_listBlankDES.append(blocks[0][1][0])
					for j in range(len(self.des_aliq[0][0])):
						conc_listBlankDes.append(blocks[0][1][0])

					DES_blankMain.extend([blocks[0][0], conc_listBlankDES])
					DES_blankMain.extend([blocks[1][0], conc_listBlankDes])
					
# ############################ DESorption: blank ###############################		

					DESaligned_blank_weight2_vals = []
					DESaligned_blank_norm_list = []
					DESdelta_mass_blank_list = []
						
					DESaligned_blank_weight2_vals.extend(self.align(self.DESrefPressure, DES_blankMain))
					DESaligned_blank_norm_list.extend(self.aligned_DES_blank[blankNum2])
				
					for x in range(len(DESaligned_blank_norm_list[0])):
						
						i = DESaligned_blank_weight2_vals[x]
						j = DESaligned_blank_norm_list[1][x]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_blank_list.append(DESdelta_mass_val)		
					self.DES_Aliq2_blankMain.append(DESdelta_mass_blank_list)
		############################ Desorption: blank ###############################

					DESaligned_blank_weight2_vals = []
					DESaligned_blank_norm_list = []
					DESdelta_mass_blank_list = []
					
					DESaligned_blank_weight2_vals.extend(self.align(self.DESrefPressure, DES_blankMain))										
					DESaligned_blank_norm_list.extend(self.aligned_des_blank[blankNum1])
					
					for y in range(len(DESaligned_blank_norm_list[0])):
						
						i = DESaligned_blank_weight2_vals[y]
						j = DESaligned_blank_norm_list[1][y]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_blank_list.append(DESdelta_mass_val)
					self.DES_Aliq2_blankMain.append(DESdelta_mass_blank_list)

				blankNum2 += 1		

	def analyseAll(self):
		self.analyseAliq()
		self.analyseBlank()
		self.mainPlotsAliq()
		self.mainPlotsBlank()
		self.DESPlotsCombine()
		self.desPlotsCombine()
		# self.mainPlotsCombine()
		# print '################  DES: aliq2 w/blank aliq1  ################'
		# print 'Raw data list: %s'%self.DESaliq2_DES_list1
		# print 'BlankCorr: %s'%self.DESaliq2_DES_list_BlankCorr1	
		# print '################  DES: aliq2 w/blank aliq2  ################'
		# print 'Raw data list: %s'%self.DESaliq2_DES_list2
		# print 'BlankCorr: %s'%self.DESaliq2_DES_list_BlankCorr2
		# print '################  DES: aliq2 w/blank aliq1  ################'
		# print 'Raw data list: %s'%self.DESaliq2_des_list1
		# print 'BlankCorr: %s'%self.DESaliq2_des_list_BlankCorr1	
		# print '################  DES: aliq2 w/blank aliq2  ################'
		# print 'Raw data list: %s'%self.DESaliq2_des_list2
		# print 'BlankCorr: %s'%self.DESaliq2_des_list_BlankCorr2

################################################ Lists for referernce ################################################

		# print "######################## aliqMain ###################################"
		# print self.DES_aliqMain 
		# print self.DES_aliqMain 
		# # print "######################## origins blanks/aliqs ###################################"
		# # print self.origin_blanks 
		# # print self.origin_aliqs 
		# print "######################## blank data ###################################"
		# # blanks data
		# print self.DES_blank 
		# print self.des_blank 
		# print "######################## aliq data ###################################"
		# # aliqs data
		# print self.DES_aliq[0][1]
		# print self.des_aliq[0][1]
		# # print "######################## diff/diff2 blank ###################################"
		# # # diff blanks data
		# # print self.diff_DES_blank 
		# # print self.diff_des_blank 
		# # print self.diff_DES_blank 
		# # print self.diff_des_blank 
		# print "######################## diff/diff2 aliq ###################################"
		# # diff aliqs data
		# print self.diff_DES_aliq[0]['diff'][1]
		# print self.diff_des_aliq[0]['diff'][1]
		# print self.diff_DES_aliq2 
		# print self.diff_des_aliq2 
		# # print "######################## average blank ###################################"
		# # # average blanks data
		# # print self.average_DES_blank 
		# # print self.average_des_blank 
		# print "######################## average aliq ###################################"
		# # average aliqs data
		# print self.average_DES_aliq 
		# print self.average_des_aliq 
		# print "######################## average diff blank ###################################"
		# # average diffs blanks data
		# print self.average_diff_DES_blank[1]
		# print self.average_diff_des_blank[1] 
		# print "######################## average diff aliq ###################################"
		# # average diffs aliqs data
		# print self.average_diff_DES_aliq 
		# print self.average_diff_des_aliq 
	
		

		


		


		








