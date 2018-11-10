# preliminary, probably not right

import pd
import subprocess

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
	num1, num2, num3, num4 = 0
	data[0][len(data[0])-1]
	for index, row in data.iterrows():
		if(row[feature] < cutoff and row[len(row)-1] == 0):
			num1 += 1
		elif(row[feature] < cutoff and row[len(row)-1] == 1):
			num2 += 1
		elif(row[feature] >= cutoff and row[len(row)-1] == 0):
			num3 += 1
		else:
			num4 += 1
	j1 = num4 / (num4 + num2) + num1 / (num1 + num3) - 1.0
	j2 = num2 / (num2 + num2) + num3 / (num1 + num3) - 1.0
	if(j1>j2):
		return j1, True
	return j2, False

def processTree(featureOrientation):
	

def main():
	data = pd.read_csv("iris.csv", encoding = "utf-8")
	while(True):
		subprocess.check_output(["raspistill", "-o", "img.jpg"])
		featureOrientation = processImg("img.jpg")
		processTree(featureOrientation)
	computeCutoff(1, data)