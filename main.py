from processTree import *
from detect_circles_template import getFeaturesFromImage
import subprocess 

filename = "otImg.jpg"

i = 0 # iteration counter

DATA_FILE = "iris.csv"

data = pd.read_csv(DATA_FILE, encoding = "utf-8")

### MAIN SCRIPT ###
while True:
	global SUCCESSES
	# get the feature list
	print("Taking photo")
	subprocess.check_output(["raspistill", "-o", filename])
	print("Parsing photo")
	featureOrientation = getFeaturesFromImage(filename)
	
	# featureOrientation = [0, None, 1, None, None, None, 2]
	print(featureOrientation)

	for i in range(0, 8): # 8 children
		featureOrientation.append(None)

	print("Training...")
	payloads = processTree(featureOrientation, data)
	
	#print "SUCCESSES: "  + str(SUCCESSES)
	#accuracy = SUCCESSES / (1.0 * data.shape[0])

	#print "accuracy: " + str(accuracy)
	print("Send outputs to arduino")
	#sendToMasterArduino(payloads)
	#sendToAccuracyArduino(accuracy)

	i += 1
	# keeps on going
	print("Done with iteration", i)
