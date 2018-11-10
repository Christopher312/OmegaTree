# preliminary, probably not right

'''
	0 - Iris-versicolor
	1 - Iris-virginica
'''

import pandas as pd
#import subprocess

def computeCutoff(feature, data):
	bestCutoff = 0
	bestJ = 0
	lessFalse = True
	for index, row in data.iterrows():
		cutoff = row[feature]

		j, lessFalse = getJ(cutoff, feature, data)
		if(j > bestJ):
			bestCutoff = cutoff
			bestJ = j
	#print "bestCutoff: " + str(bestCutoff)
	return bestCutoff, lessFalse

def getJ(cutoff, feature, data):
	# Youden's J Statistic
	# Returns the correct J, as well as whether to split with less than as negative or positive
	num1 = 0
	num2 = 0
	num3 = 0
	num4 = 0

	for index, row in data.iterrows():
		if(row[feature] < cutoff and row[len(row)-1] == 0):
			num1 += 1
		elif(row[feature] < cutoff and row[len(row)-1] == 1):
			num2 += 1
		elif(row[feature] >= cutoff and row[len(row)-1] == 0):
			num3 += 1
		else:
			num4 += 1

	#print "cutoff: " + str(cutoff)

	#print "num1: " + str(num1)
	#print "num2: " + str(num2)
	#print "num3: " + str(num3)
	#print "num4: " + str(num4)

	if(num4 + num2 == 0 or num1 + num3 == 0): return -2, False

	j1 = num4 / ((num4 + num2) * 1.0) + num1 / ((num1 + num3) * 1.0) - 1.0
	j2 = num2 / ((num2 + num4) * 1.0) + num3 / ((num1 + num3) * 1.0) - 1.0

	#print "j1: " + str(j1)
	#print "j2: " + str(j2)

	if(j1>j2):
		return j1, True
	return j2, False

# processTree(featureOrientation, data) returns heap of cutoff values indexed corresponding to featureOrientation
# 	based on data
#	assumption: binary tree
#	assumption: featureOrientation stores features as the indices in the data
#	return: heap of cutoff values
def processTree(featureOrientation, data):
	if(False): # return preprocessed (stored) heap
		return False
	length = 7 # arbritrary but for our case is 7
	cutoffs = [-1] * length  # stores cutoffs of each feature
	getCutoffs(0, length, data, featureOrientation, cutoffs) # stores cutoffs in cutoffs
	return cutoffs;

# getCutoffs(index, length, data, featureOrientation, cutoffs) determines cutoff (and children cutoffs)
# 	 based on featureOrientation at index
# side effect: updates cutoffs
def getCutoffs(index, length, data, featureOrientation, cutoffs):
	if(index < length and featureOrientation[index] != None):
		cutoffs[index], lessFalse = computeCutoff(featureOrientation[index], data) # pass by reference apparently (treats as list I guess?)
		#print "cutoff: " + str(cutoffs[index])
		leftData = filterData(featureOrientation[index], cutoffs[index], data.copy(), True)
		rightData = filterData(featureOrientation[index], cutoffs[index], data.copy(), False) # filtered data to cutoff

		getCutoffs(2 * index + 1, length, leftData, featureOrientation, cutoffs) # compute cutoff for left child
		getCutoffs(2 * index + 2, length, rightData, featureOrientation, cutoffs) # compute cutoff for right child
	elif(index < length and featureOrientation[index] == None): cutoffs[index] = None
# filterData(feature, cutoff, data) filters data based on the feature (index)
def filterData(feature, cutoff, data, getSmaller):
	for row_index, row in data.iterrows():
		if (getSmaller):
			if(row[feature] >= cutoff):
				data.drop(row_index, inplace=True)
		else:
			if(row[feature] < cutoff):
				data.drop(row_index, inplace=True)

	return data;

def main():
	data = pd.read_csv("iris.csv", encoding = "utf-8")

	while(True):
		#subprocess.check_output(["raspistill", "-o", "img.jpg"])
		# featureOrientation = processImg("img.jpg")

		featureOrientation = [2, None, 0, 2, 3, 1, None]
		cutoffs = processTree(featureOrientation, data)

		for cutoffValue in cutoffs:
			print cutoffValue

		break
main()