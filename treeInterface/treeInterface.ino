/**
 * This is the Arduino to RPi interface for controlling decision
 * tree LEDs. Communication is done serially, where individual bytes
 * indicate the brightness of each branch, or Red/Green/Off of each node.
 */

#define MAX_BRIGHTNESS 255

int allPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 44, 46, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41};
int edgePins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 44, 46};
int greenPins[] = {14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40};
int redPins[] = {15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41};
int numEdgePins = 14;
int numGreenPins = 14;
int numRedPins = 14;
int numPins = 42;

int indBranch = 0; /* index of current branch */
int indNode = 0;   /* index of current node */

void setup() {
  /*** RESET LEDs ***/
  for (int j = 0; j < numEdgePins; j++) {
    pinMode(edgePins[j], OUTPUT);   // sets the pin as output
  }

  for (int j = 0; j < numGreenPins; j++) {
    pinMode(greenPins[j], OUTPUT);   // sets the pin as output
  }

  for (int j = 0; j < numRedPins; j++) {
    pinMode(redPins[j], OUTPUT);   // sets the pin as output
  }

  for (int j = 0; j < numPins; j++) {
    digitalWrite(allPins[j], LOW);
  }  


  /*** SERIAL PORT ***/
  // baudrate of 9600 for serial communication
  Serial.begin(9600);
  
  // don't wait for serial communication, 
  // allows for faster matrix display update
  Serial.setTimeout(0);
}

void setBranch(int branchI, int amount) {
  analogWrite(edgePins[branchI], (amount * MAX_BRIGHTNESS) / 9);
}

void setNode(int nodeI, int mode) {
  switch (mode) {
    case 1:
      digitalWrite(greenPins[nodeI], HIGH);
      break;
    case 2:
      digitalWrite(redPins[nodeI], HIGH);
      break;
    default: 
      digitalWrite(greenPins[nodeI], LOW);
      digitalWrite(redPins[nodeI], LOW);
  }
}

void loop() {
  if(Serial.available()) {
    // read input from serial
    int in = Serial.read();
    
    /** 
     * Interpret serial communication.
     * 
     * We set the branch lights before the nodes.
     */
    if(in == 's') {
      indBranch = 0;
      indNode = 0;
    } else if (indBranch < 14) { 
      setBranch(indBranch, in - '0');
      indBranch++;
    } else if (indNode < 14) {
      setNode(indNode, in - '0');
      indBranch++;
    } else {
      // expect end of packet 'e'
    }
  }
}
