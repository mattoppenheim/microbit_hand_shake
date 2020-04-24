/*
keyboardLeo takes characters from the serial i/p, then o/ps
them as keyboard strokes.
Written to enable communication with Sensory Software's Grid2 through keyboard interface
leostick VID=9914 PID=32770
 Matt Oppenheim April 2013
 v2 responds to query string 'L' with 'S' to enable identification
 of the com port that the Leo is on
 v3 June 2017 rewritten for use with microbit. pin 2 does not need to be held high
 Identify leostick using VID and PID, then handshake
 */
 

void setup() {
  // make pin 2 an input and turn on the
  // pullup resistor so it goes high unless
  // connected to ground:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  flash();
}

void loop() {
if (Serial.available() > 0) 
  { // check for incoming serial data:
    char inChar = Serial.read(); // read incoming serial data
    // to identify the LeoStick, send an 'L', receive an 'S'
    if (inChar == 'L')
    {
      sendS();
    }// ~if 
    else
    {
        Keyboard.begin(); // for keyboard HID spoofing
        Keyboard.write(inChar); //Type the message on PC keyboard
        Keyboard.end();
    } // ~else
  }// ~if
} // ~loop

// flash LED
void flash() {
  digitalWrite(13, LOW);    // set the LED off
  delay(200);  
  digitalWrite(13, HIGH);   // set the LED on
  delay(200);              // wait for 200ms
  digitalWrite(13, LOW);    // set the LED off
  delay(200);              
}

void sendS(){
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  Serial.write("S");
}
  
