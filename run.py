#### Run both file conversion script and plotting script ####

import os







if __name__ == '__main__':
	
	curr_path = os.getcwd()
	print curr_path

	IGA_scripts_path =  os.path.dirname('%s/IGA_Files/Scripts/'%curr_path)
	IGAplot_path = os.chdir(IGA_scripts_path)

	os.system('python IGAplot.py')

	os.system('python main.py')


	# os.chdir(os.path.dirname('%s'%curr_path))
	# print os.getcwd()

