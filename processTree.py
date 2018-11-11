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
#from detect_circles_template import getFeaturesFromImage

DATA_FILE = "iris.csv"
STORAGE_FILE = "preprocessed_data.txt"
BRIGHTNESS_SCALE = 255
VERSICOLOR = 1
VIRGINICA = 2
NUM_NODES = 7

SUCCESSES = 0

ports = list(serial.tools.list_ports.comports())

hiddenSerial = '557353237353514072A1'
arduinoAccuracyHiddenSerial = '75439323735351513111'

arduino = [p[0] for p in ports if (hiddenSerial in p[2])]
ser = serial.Serial(arduino[0], timeout=0)

arduinoAccuracy = [p[0] for p in ports if (arduinoAccuracyHiddenSerial in p[2])]
arduinoAccuracySer = serial.Serial(arduinoAccuracy[0], timeout=0)

# to find the serial number...
#for p in ports:
#	print(p[2])

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
				print("found payloads")
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
	# cutoffPayloads = getOrientationFromFile(featureOrientation)
	# if(cutoffPayloads != None): return cutoffPayloads

	# orientation not found, must create
	length = len(featureOrientation) # arbritrary but for our case is 15
	cutoffPayloads = [Payload() for i in range(length)] # stores cutoffs of each feature
	getCutoffs(0, length, data, data.shape[0], featureOrientation, cutoffPayloads) # stores cutoffs in cutoffs

	# storeNewPayloads(cutoffPayloads, featureOrientation)

	return cutoffPayloads;

# countSuccesses(data, payloads) increments successes based on number of successfuly guessed classifications
def countSuccesses(data, payloads, featureOrientation, index):
	global SUCCESSES
	for row_index, row in data.iterrows():
		if(row[len(row) - 1] == payloads[index].classification):
			SUCCESSES = SUCCESSES + 1

# isLeaf(featureOrientation, index) checks if leaf node
def isLeaf(featureOrientation, index):
	return featureOrientation[index] == None

# classifyNode(cutoffPayloads, index, data) classifies node based on dominant trait
def classifyNode(cutoffPayloads, index, data):
	type1 = VERSICOLOR
	type2 = VIRGINICA
	numType1 = 0
	numType2 = 0
	for row_index, row in data.iterrows():
		if(row[len(row) - 1] == type1):
			numType1 = numType1 + 1
		else:
			numType2 = numType2 + 1

	if(numType1 >= numType2): cutoffPayloads[index].classification = type1
	else: cutoffPayloads[index].classification = type2


# getCutoffs(index, length, data, dataSize, featureOrientation, cutoffPayloads) determines cutoff (and children cutoffs)
# 	 based on featureOrientation at index
# side effect: updates cutoffs
def getCutoffs(index, length, data, dataSize, featureOrientation, cutoffPayloads):
	if(index < length and featureOrientation[index] != None):
		cutoffPayloads[index].cutoff, lessFalse = computeCutoff(featureOrientation[index], data) # pass by reference apparently (treats as list I guess?)

		# check if children need to be evaluated
		if(2 * index + 2 < length):
			leftData, rightData = filterData(featureOrientation[index], cutoffPayloads[index].cutoff, data)

			# check if either children is a leaf 
			if(isLeaf(featureOrientation, 2 * index + 1)):	
				classifyNode(cutoffPayloads, 2 * index + 1, leftData)
				# counts the number of successfuly guessed classifications	
				countSuccesses(leftData, cutoffPayloads, featureOrientation, 2 * index + 1)
			if(isLeaf(featureOrientation, 2 * index + 2)):	
				classifyNode(cutoffPayloads, 2 * index + 2, rightData)
				countSuccesses(rightData, cutoffPayloads, featureOrientation, 2 * index + 2)	
			

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

# sendToMasterArduino(payloads) sends information from the payloads to the arduino
def sendToMasterArduino(payloads):

	# begin writing to serial port
	print('begin to write') 
	ser.write(b's') # start bit
        
	print("-------------------------")
	print("Sending weights")
	# send weights (brightness)
	for index, payload in enumerate(payloads):
		if(index != 0):
			print("Absolute weight (scaled by 255): ", max(0,(int(BRIGHTNESS_SCALE * payload.absoluteWeight))))
			ser.write(chr(max(0,(int(payload.absoluteWeight * BRIGHTNESS_SCALE)))))

	print("-------------------------")
	print("Sending classifications")

	# send classifications of nodes
	for index, payload in enumerate(payloads):
		if(index != 0):
			print("Classification: " + str(payload.classification))
			ser.write(str(payload.classification).encode())

	print("-------------------------")

	ser.write(b'e') # end bit

# sentToAccuracyArduino(accuracy) sends accuracy report to Arduino Uno
def sendToAccuracyArduino(accuracy):
	
	arduinoAccuracySer.write(b's')

	NUM_DIGITS = 4 # standardize number of digits

	print("-------------------------")

	print("Sending accuracy")
	print("Accuracy: " + str(accuracy)) # precision to 2 decimal pllaces

	accuracy = accuracy * 100 # scale by 100 to be in percent

	if(float(accuracy) >= 100): accuracy = str(99.00)
	if(float(accuracy) < 10): accuracy = str(0) + str(accuracy)

	numDigits = 0
	for index, digit in enumerate(str(accuracy)):
		if(numDigits < NUM_DIGITS):
			if(digit != '.'):
				arduinoAccuracySer.write(digit.encode())
				print ("Digit: " + str(numDigits) + " -> " + str(digit))
				numDigits = numDigits + 1

	if(numDigits < NUM_DIGITS): # number of digits to have at end
		for index in range(0, NUM_DIGITS - numDigits):
			print ("Digit: " + str(numDigits) + " -> " + str(0))
			numDigits = numDigits + 1
			arduinoAccuracySer.write(str(0).encode())

	print("-------------------------")

	arduinoAccuracySer.write(b'e')

def main():
	data = pd.read_csv(DATA_FILE, encoding = "utf-8")

	while(True):
		#subprocess.check_output(["raspistill", "-o", "img.jpg"])
		# featureOrientation = processImg("img.jpg")
		
		featureOrientation = [0, 1, 3, 2, 3, 1, 3]

		#featureOrientation = getFeaturesFromImage(imageName)

		for i in range(0, 8): #8 children
			featureOrientation.append(None)

		payloads = processTree(featureOrientation, data)

		accuracy = SUCCESSES / (1.0 * data.shape[0])

		sendToMasterArduino(payloads)
		sendToAccuracyArduino(accuracy)
		break

main()
