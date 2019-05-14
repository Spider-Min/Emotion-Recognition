#!/usr/bin/env python

import sys
import os
from subprocess import *


def predict_emotion_paef(file_url):
# svm, grid, and gnuplot executable files

	is_win32 = (sys.platform == 'win32')
	if not is_win32:
		svmscale_exe = "../svm-scale"
		svmtrain_exe = "../svm-train"
		svmpredict_exe = "../svm-predict"
		grid_py = "./grid.py"
		gnuplot_exe = "/usr/local/bin/gnuplot"
	else:
		# example for windows
		svmscale_exe = r".\libsvm\windows\svm-scale.exe"
		svmtrain_exe = r".\libsvm\windows\svm-train.exe"
		svmpredict_exe = r".\libsvm\windows\svm-predict.exe"
		# gnuplot_exe = r"c:\tmp\gnuplot\binary\pgnuplot.exe"
		grid_py = r".\grid.py"

	assert os.path.exists(svmscale_exe),"svm-scale executable not found"
	assert os.path.exists(svmtrain_exe),"svm-train executable not found"
	assert os.path.exists(svmpredict_exe),"svm-predict executable not found"
	# assert os.path.exists(gnuplot_exe),"gnuplot executable not found"
	assert os.path.exists(grid_py),"grid.py not found"

	test_pathname = file_url
	assert os.path.exists(test_pathname),"testing file not found"

	file_name = os.path.split(file_url)[1]
	scaled_file = file_name + ".scale"
	model_file = "trained_models/paef_models/artphoto_train.txt.model"
	range_file = "trained_models/paef_models/artphoto_train.txt.range"
	scaled_test_file = file_name + ".scale"
	predict_test_file = file_name + ".predict"

	# test_pathname = sys.argv[1]
	cmd = '{0} -r "{1}" "{2}" > "{3}"'.format(svmscale_exe, range_file, test_pathname, scaled_test_file)
	print('Scaling testing data...')
	Popen(cmd, shell = True, stdout = PIPE).communicate()

	cmd = '{0} "{1}" "{2}" "{3}"'.format(svmpredict_exe, scaled_test_file, model_file, predict_test_file)
	print('Testing...')
	Popen(cmd, shell = True).communicate()

	print('Output prediction: {0}'.format(predict_test_file))


	mapping = {
		0: "happy",
		2: "fear",
		3: "excitement",
		4: "disgust",
		6: "anger",
		7: "sad"
	}

	with open('image_data.txt.predict', 'r') as feature:
		labs = []
		for line in feature:
			line = line.strip()
			labs.append(line)
		print(int(labs[0]))
		return mapping[int(labs[0])]
