# preliminary, probably not right

'''
	1 - Iris-versicolor (red)
	2 - Iris-virginica (green)
'''
import pickle
import pandas as pd
import subprocess
import serial
import serial.tools.list_ports
import os.path
import time

from PayloadWrapperList import PayloadWrapperList
from StoragePayloadWrapper import StoragePayloadWrapper
from Payload import Payload

DATA_FILE = "iris.csv"
STORAGE_FILE = "preprocessed_data.txt"
BRIGHTNESS_SCALE = 9
VERSICOLOR = 1
VIRGINICA = 2
NUM_NODES = 7

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
		#print "error"
		return -2, False

	j1 = num4 / ((num4 + num2) * 1.0) + num1 / ((num1 + num3) * 1.0) - 1.0
	j2 = num2 / ((num2 + num4) * 1.0) + num3 / ((num1 + num3) * 1.0) - 1.0

	if(j1>j2):
		return j1, True
	return j2, False

# getFeatureOrientationKey(featureOrientation) creates simple key to identify unique orientation
def getFeatureOrientationKey(featureOrientation):
	featureOrientationKey = str(featureOrientation[0])
	SPLITTER = ","
	for index, feature in enumerate(featureOrientation):
		if (index == NUM_NODES): break
		if (index > 0):
			featureOrientationKey = featureOrientationKey + SPLITTER + str(feature)
		# the last 8 None are just to make it easier to use algorithm

	return featureOrientationKey

# getOrientationFromFile(featureOrientation) gets the payloads from file
# return payloads from file or None if nothing is there
def getOrientationFromFile(featureOrientation):
	if os.path.isfile(STORAGE_FILE):
		with open(STORAGE_FILE, "rb") as fp:
			storageWrappers = pickle.load(fp)
		if(storageWrappers == None): return None

		featureOrientationKey = getFeatureOrientationKey(featureOrientation)
		for storageWrapper in storageWrappers.payloadWrappers:
			if (storageWrapper.featureOrientationKey == featureOrientationKey):
				print "found payloads"
				return storageWrapper.payloads

	return None

# storeNewPayloads(cutoffPayloads, featureOrientation) stores new cutoffPayloads to file and uses featureOrientation to create key
def storeNewPayloads(cutoffPayloads, featureOrientation):
	storageWrappers = PayloadWrapperList()
	storageWrappers.payloadWrappers = []
	if os.path.isfile(STORAGE_FILE):
		with open(STORAGE_FILE, "rb") as fp:
			storageWrappers = pickle.load(fp)

	# create new element to add to file
	payloadWrapper = StoragePayloadWrapper()
	payloadWrapper.featureOrientationKey = getFeatureOrientationKey(featureOrientation)
	payloadWrapper.payloads = cutoffPayloads

	# store in list
	storageWrappers.payloadWrappers.append(payloadWrapper)

	with open(STORAGE_FILE, "wb") as fp:
		pickle.dump(storageWrappers, fp)

# processTree(featureOrientation, data) returns heap of cutoff values indexed corresponding to featureOrientation
# 	based on data
#	assumption: binary tree
#	assumption: featureOrientation stores features as the indices in the data
#	return: heap of cutoff values
def processTree(featureOrientation, data):
	cutoffPayloads = getOrientationFromFile(featureOrientation)
	if(cutoffPayloads != None): return cutoffPayloads

	# orientation not found, must create
	length = len(featureOrientation) # arbritrary but for our case is 15
	cutoffPayloads = [Payload() for i in range(length)] # stores cutoffs of each feature
	getCutoffs(0, length, data, data.shape[0], featureOrientation, cutoffPayloads) # stores cutoffs in cutoffs

	storeNewPayloads(cutoffPayloads, featureOrientation)

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

# sendToArduino(payloads) sends information from the payloads to the arduino
def sendToArduino(payloads):
	ser = serial.Serial('com3', 9600)
	time.sleep(2) # allow serial communication to establish

	# get serial port being used
	# ports = list(serial.tools.list_ports.comports())
	# hiddenSerial = '855393139313517121F1'
	# arduino = [p[0] for p in ports if (hiddenSerial in p[2])]
	# ser = serial.Serial(arduino[0], timeout=0)

	# begin writing to serial port
	ser.write(b's') # start bit

	print "-------------------------"
	print "Sending weights"
	# send weights (brightness)
	for index, payload in enumerate(payloads):
		if(index != 0):
			print "Absolute weight (scaled by 9): " + str(BRIGHTNESS_SCALE * payload.absoluteWeight)
			ser.write(str(payload.absoluteWeight * BRIGHTNESS_SCALE).encode())
			time.sleep(2)

	print "-------------------------"
	print "Sending classifications"

	# send classifications of nodes
	for index, payload in enumerate(payloads):
		if(index != 0):
			print "Classification: " + str(payload.classification)
			ser.write(str(payload.classification))
			time.sleep(2)

	time.sleep(5)
	print "-------------------------"

	ser.write(b'e') # end bit

def main():
	data = pd.read_csv(DATA_FILE, encoding = "utf-8")

	while(True):
		#subprocess.check_output(["raspistill", "-o", "img.jpg"])
		# featureOrientation = processImg("img.jpg")

		featureOrientation = [0, 1, 2, None, 3, 3, 1, None, None, None, None, None, None, None, None]

		payloads = processTree(featureOrientation, data)

		sendToArduino(payloads)
		break

main()