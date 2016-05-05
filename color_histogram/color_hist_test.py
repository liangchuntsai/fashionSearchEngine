import os
import glob
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image
# from matplotlib import pyplot as plt
import numpy as np
import math
import type_classification.py

def store_as_csv (directory=""):
	files = []
	# directory for read files.
	directory = "/Users/cyan/Desktop/color_hist_py/crawlImages_large/"
	for infile in glob.glob(os.path.join(directory,'*.jpg')):
		files.append(infile)
	# print "current file is " + infile
	for i in range(len(files)):
		print i
		id1 = files[i].rfind('/')
		id2 = files[i].rfind('.')
		idx = int(files[i][id1+1:id2])
		temp =[]*2

		hist = color_hist(nBins,files[i])
		temp.append(idx)
		temp.append(hist)
		result_idx.append(temp)
		# result.append(hist)

	# with open("color_model.csv","wb") as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(result)

	with open("color_model_idx.csv","wb") as f:
		writer = csv.writer(f)
		writer.writerow(result_idx)
	return

def store_as_array (directory="", nBins=3):
	nBins = 3
	nFiles = 28582
	val_num = math.pow(nBins,3)

	files = []
	# directory for read files.
	directory = "/Users/cyan/Desktop/color_hist_py/crawlImages_large/"
	for infile in glob.glob(os.path.join(directory,'*.jpg')):
		files.append(infile)
		# print "current file is " + infile


	result_idx = np.empty([nFiles, val_num])
	print "There are " + str(len(files)) +  " images."


	# hist = color_hist(nBins,files[0])
	# result_idx[0, ] = hist
	# print result_idx

	# store the filename in a list.
	# store the histogram array(vector) to result.
	for i in range(len(files)):
		print i
		id1 = files[i].rfind('/')
		id2 = files[i].rfind('.')
		idx = int(files[i][id1+1:id2])
		hist = color_hist(nBins,files[i])
		result_idx[idx-1, ] = hist

	# delete all-zeros rows.
	result = result_idx[~(result_idx==0).all(1)]
	print "final size " + str(result.shape[0])
	np.save(open("color_hist.npy", 'wb'), result)
	return

def color_hist (bins, img):
	"compute the color histogram of an image."
	range_ = 256.0/bins;
	color_hist = np.zeros((1,int(math.pow(bins,3))))
	# color_hist = [0]*int(math.pow(bins,3))
	base = 0.0

	im = Image.open(img).convert('RGB')

	w, h = im.size  
	colors = im.getcolors(w*h)

	for item in colors:
		count = item[0]
		rgb = item[1]
		p0 = int(math.floor(rgb[0]/range_))
		p1 = int(math.floor(rgb[1]/range_))
		p2 = int(math.floor(rgb[2]/range_))
		for i in range(count):
			color_hist[0, p0*bins*bins+p1*bins+p2] = color_hist[0, p0*bins*bins+p1*bins+p2]+1

	# for i in range(len(color_hist)):
	# 	base = base + math.pow(color_hist[i],2)
	# base = math.sqrt(base)
	# compute the normalized base.
	base = np.linalg.norm(color_hist)

	# normalize.
	for i in range(color_hist.shape[1]):
		# print color_hist[i]
		color_hist[0, i] = color_hist[0, i] / base ; 
		# print color_hist[i]
	return color_hist

def getDist(target, query):
	return np.linalg.norm(query - target)

def colDistance (bins, query_path):
	"get the distance for each image in database"
	query_ht = color_hist(bins, query_path)
	query_array = np.array(query_ht)

	# open the matrix for color histogram
	hist = np.load("color_hist(no crop).npy")

	dist = np.apply_along_axis(getDist, 1, hist, query_array)
	# print dist

	return dist
	# return (list(dist.argsort()[:20]+1))

def getDistance(factor, query_path):
	bins = 3;
	cnn_dist = type_classification.getNeighbor(query_path)
	color_hist = colDistance(bins, query_path)

	result = np.zeros((cnn_dist.shape[0],1))
	for i in range(color_hist.shape[0]):
		result[i] = factor * cnn_dist[i] + (1 - factor) * color_hist[i]

	return (list(result.argsort()[:20]+1))

""" for debug
query_path = "/Users/cyan/Desktop/color_hist_py/1.jpg"
ind_list = colDistance(3, query_path)
print ind_list
"""










