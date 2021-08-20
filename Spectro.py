import numpy as np
from scipy.io.wavfile import read
from scipy.signal import spectrogram
import math
import os

def rmp_range (val_list):								# A function for remapping the values of Sxx to a managble range, uses logarithmic scaling.
	val_rmp = []										# list for remapped results
	i = 0
	while i < len(val_list):					 		# iterate over all list members.
		x = val_list[i]						
		if x == 0:								 		# avoid division by 0!
			val_rmp.append(int(x))
			i = i + 1
		else:
			logi = math.log(x,16)						# a number can be described as a float multiplied by 16 in some power (16 can be replaced by other values, but was chosen for faster calculation).
			tmp = x/16**logi							# this operation replaces the number 16 in this formula with a smaller number, thus greatly reducing it.
			norm = int(tmp*1.43**logi)			 		# 1.43 is a value defined by trial and error to achieve a maximum remapped value of around 100.
			val_rmp.append(norm)				 		# add normalized value to the output list.
			i = i + 1
	maxval = max(val_rmp)								# find the largest normalized value for control purposes.
	print ('Largest value in spec_dat.txt is', maxval)
	return val_rmp										# list of remapped values.

abs_path = os.path.realpath(__file__)					# determine absolute path of script file.
folder = abs_path.rsplit('\\', 1)[0]			 		# find the relative path to the script folder.
print ('folder is', folder)
print ('file is', abs_path)

wav_in_file = os.path.join(folder,'wav_in.txt')			# create a path to input path from a path relative to the script location.
wav_in = open(wav_in_file, 'r')							# open txt file with path to wav file.
wav_dat = wav_in.read() 								# read path to wav from txt file.
dat = read(str(wav_dat))						 		# read data from wav file. Note that this read function is different from the one used to read txt files.
spec_in = np.array(dat[1],dtype=float) 			 		# arrange data as ndarray to  be used as input in the spectrogram function.

# compute spectrogram. Receive lists of frequencies, time steps and magnitudes. In this application of spectral data we are only interested in the magnitudes.
f,t,Sxx = spectrogram(spec_in, fs = 44100, return_onesided = True, window = 'hann', scaling = 'density')

spec_dim_file = os.path.join(folder,'spec_dim.txt')		# make sure the file is written in the same path as the script.
spec_dim = open(spec_dim_file, 'w') 					# file for grid dimensions.
spec_dim.write(str(Sxx.shape[0])+','+str(Sxx.shape[1])) # write in the txt file the number of frequencies and number of time steps.
spec_dim.close()

val_list = [] 											# list for magnitude values.
for i in range(0, Sxx.shape[1]): 						# write values from nparray into a list.
	for j in range(0, Sxx.shape[0]):
		val_list.append(Sxx[j][i])

val_rmp = rmp_range(val_list)							# remap all values to managble range

spec_dat_file = os.path.join(folder,'spec_dat.txt')		# make sure the file is written in the same path as the script
spec_dat = open(spec_dat_file, 'w') 					# prepare txt file for transfering result back to gh.
for i in range(len(val_rmp)):
	spec_dat.write(str(val_rmp[i]) + ',')				# write all remapped magnitude values to txt file
spec_dat.close()