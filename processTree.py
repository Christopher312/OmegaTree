# preliminary, probably not right

import pd

def computeCutoff(feature, data):
	bestCutoff = 0
	bestJ = 0
	for index, row in data.iterrows():
		cutoff = row[feature]
		j = getJ(cutoff, feature, data)
		if(entropy > bestEntropy):
			bestCutoff = cutoff
			bestJ = j
	return bestCutoff

def getJ(cutoff, feature, data):
	num1, num2, num3, num4 = 0
	for index, row in data.iterrows():
		if(row[feature] < cutoff and row[len(row)-1] == 0):
			num1 += 1
		elif(row[feature] < cutoff and row[len(row)-1] == 1):
			num2 += 1
		elif(row[feature] >= cutoff and row[len(row)-1] == 0):
			num3 += 1
		else:
			num4 += 1
	return num1 / (num1 + num3) + num4 / (num4 + num2) - 1.0

def main():
	data = pd.read_csv("iris.csv", encoding = "utf-8")
	computeCutoff(feature, data)