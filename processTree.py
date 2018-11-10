# preliminary, probably not right

'''
	1 - Iris-versicolor (red)
	2 - Iris-virginica (green)
'''

import pandas as pd
#import subprocess
from Payload import Payload

VERSICOLOR = 1
VIRGINICA = 2

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
	return bestCutoff, lessFalse

def getJ(cutoff, feature, data):
	# Youden's J Statistic
	# Returns the correct J, as well as whether to split with less than as negative or positive
	num1 = 0
	num2 = 0
	num3 = 0
	num4 = 0

	for index, row in data.iterrows():
		if(row[feature] < cutoff and row[len(row)-1] == VERSICOLOR):
			num1 += 1
		elif(row[feature] < cutoff and row[len(row)-1] == VIRGINICA):
			num2 += 1
		elif(row[feature] >= cutoff and row[len(row)-1] == VERSICOLOR):
			num3 += 1
		else:
			num4 += 1

	if(num4 + num2 == 0 or num1 + num3 == 0):
		print "error"
		return -2, False

	j1 = num4 / ((num4 + num2) * 1.0) + num1 / ((num1 + num3) * 1.0) - 1.0
	j2 = num2 / ((num2 + num4) * 1.0) + num3 / ((num1 + num3) * 1.0) - 1.0

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
	cutoffPayloads = [Payload() for i in range(length)] # stores cutoffs of each feature
	getCutoffs(0, length, data, data.shape[0], featureOrientation, cutoffPayloads) # stores cutoffs in cutoffs

	return cutoffPayloads;

# getCutoffs(index, length, data, dataSize, featureOrientation, cutoffPayloads) determines cutoff (and children cutoffs)
# 	 based on featureOrientation at index
# side effect: updates cutoffs
def getCutoffs(index, length, data, dataSize, featureOrientation, cutoffPayloads):
	if(index < length and featureOrientation[index] != None):
		cutoffPayloads[index].cutoff, lessFalse = computeCutoff(featureOrientation[index], data) # pass by reference apparently (treats as list I guess?)

		# check if children need to be evaluated
		if(2 * index + 2 < length):
			leftData, rightData = filterData(featureOrientation[index], cutoffPayloads[index].cutoff, data)

			# set dominant trait
			if(leftData.shape[0] >= rightData.shape[0]):
				cutoffPayloads[2 * index + 1].classification = VERSICOLOR
				cutoffPayloads[2 * index + 2].classification = VIRGINICA
			else:
				cutoffPayloads[2 * index + 1].classification = VIRGINICA
				cutoffPayloads[2 * index + 2].classification = VERSICOLOR

			# set weight
			print "size of left data: " + str(leftData.shape[0])
			print "size of right data: " + str(rightData.shape[0])
			cutoffPayloads[2 * index + 1].absoluteWeight = leftData.shape[0] / (dataSize * 1.0);
			cutoffPayloads[2 * index + 2].absoluteWeight = rightData.shape[0] / (dataSize * 1.0);

			getCutoffs(2 * index + 1, length, leftData,
					   dataSize, featureOrientation, cutoffPayloads)  # compute cutoff for left child
			getCutoffs(2 * index + 2, length, rightData,
					   dataSize, featureOrientation, cutoffPayloads) # compute cutoff for right child


# filterData(feature, cutoff, data) filters data based on the feature (index)
# side effect: updates cutoff dominant trait
def filterData(feature, cutoff, data):
	leftData = data.copy()
	rightData = data.copy()
	for row_index, row in data.iterrows():
			if(row[feature] >= cutoff):
				leftData.drop(row_index, inplace=True)
			else:
				rightData.drop(row_index, inplace=True)
	return leftData, rightData;

def main():
	data = pd.read_csv("iris.csv", encoding = "utf-8")

	while(True):
		#subprocess.check_output(["raspistill", "-o", "img.jpg"])
		# featureOrientation = processImg("img.jpg")

		featureOrientation = [0, 1, None, 2, 3, 1, 3]
		payloads = processTree(featureOrientation, data)

		# last 4 are the leaves
		for payload in payloads:
			print "-------------------------"
			if(payload != None):
				print "Cutoff: " + str(payload.cutoff)
				print "Absolute weight: " + str(payload.absoluteWeight)
				print "Classification: " + str(payload.classification)
			print "-------------------------"
		break
main()