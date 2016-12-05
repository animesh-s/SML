import matplotlib.pyplot as plt
import numpy as np
import os

import sys

def save(path, ext='png', close=True, verbose=True):
		"""Save a figure from pyplot.
		Parameters
		----------
		path : string
		The path (and filename, without the extension) to save the
		figure to.
		ext : string (default='png')
		The file extension. This must be supported by the active
		matplotlib backend (see matplotlib.backends module).  Most
		backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.
		close : boolean (default=True)
		Whether to close the figure after saving.  If you want to save
		the figure multiple times (e.g., to multiple formats), you
		should NOT close it in between saves or you will have to
		re-plot it.
		verbose : boolean (default=True)
		Whether to print information about when and where the image
		has been saved.
		"""
		
		# Extract the directory and filename from the given path
		directory =DATA_PATH# os.path.split(path)[0]
		filename = "%s.%s" % (os.path.split(path)[1], ext)
		if directory == '':
			directory = '.'

		# If the directory does not exist, create it
		if not os.path.exists(directory):
			os.makedirs(directory)

		# The final path to save to
		savepath = os.path.join(directory, filename)

		if verbose:
			print("Saving figure to '%s'..." % savepath),

		# Actually save the figure
		plt.savefig(savepath)
		
		# Close it
		if close:
			plt.close()

		if verbose:
			print("Done")


DATA_PATH = "/home/akhil/smlProject/Graphs/ONECLASSSVM/"
FILE_NAME="one_class_svm_pca"
#DATA_FILE = "/home/akhil/smlProject/Graphs/SVM/SVMLINEAR/svm_linear_0__TrueResult.txt"
DELIMITER = ' '

X_LABEL = "C"
Y_LABEL = "f_measure"


if __name__ == "__main__":
	kArray=[1]
	for k in kArray:	
		file_pointer = open(DATA_PATH+FILE_NAME,'r')
		parameter1 = []
		parameter2 = []
		f_measure = []
		precision = []
		recall = []
		for line in file_pointer:
			values = line.split(DELIMITER)
			print values[0]
			print values[1]
			print values[2]
			parameter1.append(float(values[0]))
			parameter2.append(float(values[1]))
			#recall.append(float(values[3])/100)
			#precision.append(float(values[2])/100)
			f_measure.append(float(values[2]))
		#print parameter1
		x_min = min(parameter1)
		x_max = max(parameter1)
		y_min = min(parameter2)
		y_max = max(parameter2)
		plt.hexbin(parameter1,parameter2,C = f_measure,cmap= plt.cm.YlOrRd,xscale='log',yscale='log',gridsize=4)
		plt.axis([x_min, x_max, y_min, y_max])

		plt.ylabel("Gamma")
		plt.xlabel("Nu")

		cb = plt.colorbar()
		cb.set_label(Y_LABEL)

		#plt.show()
		save(FILE_NAME, ext="png", close=False, verbose=True)
