from TGA_analyse import TGA_Analyse
import simplejson as json 
from TGA_plot import TGA_Plot



if __name__ == '__main__':
	analyse = TGA_Analyse()
	analyse.load()
	analyse.analyseAll()

	plot = TGA_Plot()

	# Note: Replace all the prints by the plots. To see run this like: python run.py > check.txt

	# Many plots: blank diffs.
	print "blanks_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps([ diff['diff'] for diff in analyse.diff_ads_blank])
	plot.blankManyPlot(json.dumps([ diff['diff'] for diff in analyse.diff_ads_blank]), 'adsorption')
	plot.blankManyPlot(json.dumps([ diff['diff'] for diff in analyse.diff_des_blank]), 'desorption')
	print "+++++++++++++++++++++++++++++++++++++++++++++++blanks_diffs"

	# Diff plot: blanks and their diffs.
	print "blanks_and_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps([ {'blank1':analyse.ads_blank[diff['i']], 'blank2':analyse.ads_blank[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_ads_blank])
	print json.dumps([ {'blank1':analyse.des_blank[diff['i']], 'blank2':analyse.des_blank[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_des_blank])
	print "+++++++++++++++++++++++++++++++++++++++++++++++blanks_and_diffs"

	# Simple plot: blanks average diffs.
	print "average_diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.average_diff_ads_blank)
	print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_ads_blank"

	print "average_diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.average_diff_des_blank)
	print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_des_blank"

	# Simple plot: blanks average.
	print "average_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.average_ads_blank)
	print "+++++++++++++++++++++++++++++++++++++++++++++++average_ads_blank"

	print "average_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.average_des_blank)
	print "+++++++++++++++++++++++++++++++++++++++++++++++average_des_blank"

	# Many plots: aliq diffs.
	print "aliqs_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps([ diff['diff'] for diff in analyse.diff_ads_aliq])
	print json.dumps(analyse.average_ads_blank)
	print json.dumps([ diff['diff'] for diff in analyse.diff_des_aliq])
	print json.dumps(analyse.average_des_blank)
	print "+++++++++++++++++++++++++++++++++++++++++++++++aliqs_diffs"

	# Diff plot: aliqs and their diffs.
	print "aliqs_and_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps([ {'aliq1':analyse.ads_aliq[diff['i']], 'aliq2':analyse.ads_aliq[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_ads_aliq])
	print json.dumps([ {'aliq1':analyse.des_aliq[diff['i']], 'aliq2':analyse.des_aliq[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_des_aliq])
	print "+++++++++++++++++++++++++++++++++++++++++++++++aliqs_and_diffs"

	# Many plots: aliqs corrected.
	print "corrected_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.corrected_ads_aliq)
	print "+++++++++++++++++++++++++++++++++++++++++++++++corrected_ads_aliq"

	print "corrected_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.corrected_des_aliq)
	print "+++++++++++++++++++++++++++++++++++++++++++++++corrected_des_aliq"

	# Simple plot: aliqs corrected average.
	print "average_corrected_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.average_corrected_ads_aliq)
	print "+++++++++++++++++++++++++++++++++++++++++++++++average_corrected_ads_aliq"

	print "average_corrected_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
	print json.dumps(analyse.average_corrected_des_aliq)
	print "+++++++++++++++++++++++++++++++++++++++++++++++average_corrected_des_aliq"

