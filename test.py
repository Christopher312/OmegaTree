import serial
import serial.tools.list_ports
import time

ports = list(serial.tools.list_ports.comports())

hiddenSerial = '557353237353514072A1'
arduinoAccuracyHiddenSerial = '75439323735351513111'

arduino = [p[0] for p in ports if (hiddenSerial in p[2])]
ser = serial.Serial(arduino[0], timeout=0)

arduinoAccuracy = [p[0] for p in ports if (arduinoAccuracyHiddenSerial in p[2])]
arduinoAccuracySer = serial.Serial(arduinoAccuracy[0], timeout=0)


ser.write(b's')
for i in range(14):
	ser.write(chr(255))
for i in range(14):
	ser.write(chr(1))

arduinoAccuracySer.write(b's')
arduinoAccuracySer.write(b'1')
arduinoAccuracySer.write(b'2')
arduinoAccuracySer.write(b'3')
arduinoAccuracySer.write(b'0')

time.sleep(1)
