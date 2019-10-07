/* by Jason Goodman (Servo control) and Rolf Nelson (NES controller, LCD screen)
 based on a mash-up of code by: 
A)SERVO CONTROL: BARRAGAN <http://barraganstudio.com> 
B)NES CONTROLLER: https://www.digikey.com/en/maker/projects/make-an-nes-controller-interface-for-arduino-uno/6d21560a571b490caa2642e87852dacb

Uses a classic Nintendo NES controller to adjust degrees of rotation of an "electronic eye" (USB webcam on a servo)
"Right" adjusts degrees of rotation UP FIVE DEGREES
"Left" adjusts degrees of rotation DOWN FIVE DEGREES
"A" button EXECUTES A SACCADE rightward the displayed number of degrees, waits 1 second, then a leftward saccade back to the starting point
 Display is a basic 16x2 LED with a backpack allowing i2c communication
Works successfully on an Arduino Nano. A faster processor may be desired if timing is critical
Intended for MKS-DS760P Ultra Speed Servo (http://www.mksservosusa.com/product.php?productid=25) with a top speed of approx .03sec/60deg

SERVO FUNCTION:
Slew a servo at a rate similar to the saccade of a human eye.
 Note that for saccades of more than 20 degrees, a standard servo may not be able
 to move fast enough!

Saccade time us = 2200 * degrees of slew + 21000
Time for each degree us = 2200 + 21000/degrees
Slew speed for 20 degree saccade: 2200+21000/20 = 3200 us/degree
Max slew speed for my servo (unloaded): 90 degrees in 300 ms = 3300 us/degree

Hookups:
SERVO:
Brown servo wire (-) to GND
Red servo wire (+) to 5v
Yellow/orange wire (S) to pin 9 (use lvl shifter for 3.3v boards)
NES:
Brown wire from NES controller (-) to GND
White wire from NES controller (+) to 5v
Yellow wire from NES controller to D4
Orange wire from NES controller to D3
Red wire from NES controller to D2
LED:
GND to GND
5v to 5v
DAT to A4
CLK to A5
*/

#include <PWMServo.h>
#include "Wire.h"
#include "Adafruit_LiquidCrystal.h"
Adafruit_LiquidCrystal lcd(0);

PWMServo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position

const int A_BUTTON         = 0;
const int B_BUTTON         = 1;
const int SELECT_BUTTON    = 2;
const int START_BUTTON     = 3;
const int UP_BUTTON        = 4;
const int DOWN_BUTTON      = 5;
const int LEFT_BUTTON      = 6;
const int RIGHT_BUTTON     = 7;
byte nesRegister  = 0;    // To hold current button states
int nesData       = 4;    // The data pin for the NES controller
int nesClock      = 2;    // The clock pin for the NES controller
int nesLatch      = 3;    // The latch pin for the NES controller


void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  
lcd.begin(16, 2);
lcd.setBacklight(HIGH);
lcd.setCursor(1,0);
lcd.print("Saccade degrees:");
  
  Serial.begin(9600);
  pinMode(nesData, INPUT);
  pinMode(nesClock, OUTPUT);
  pinMode(nesLatch, OUTPUT);
  digitalWrite(nesClock, LOW);
  digitalWrite(nesLatch, LOW);
}

int slewdegrees = 20;
int delaymicros = 2200 + 21000/slewdegrees;

void loop() {
  nesRegister = readNesController();
   lcd.setCursor(2,1);
  lcd.print(slewdegrees);

  if (bitRead(nesRegister, A_BUTTON) == 0)
    moveServo(slewdegrees);    
  if (bitRead(nesRegister, LEFT_BUTTON) == 0)
    slewdegrees = slewdegrees-5;  //move saccade degrees down by 5 if left button is pushed
  if (bitRead(nesRegister, RIGHT_BUTTON) == 0)  //can add more controls for NES; left out here because they are not used
    slewdegrees = slewdegrees+5; //move saccade degrees up by 5 if right button is pushed
  delay(50);
}

byte readNesController() 
{  
  // Pre-load a variable with all 1's which assumes all buttons are not
  // pressed. But while we cycle through the bits, if we detect a LOW, which is
  // a 0, we clear that bit. In the end, we find all the buttons states at once.
  int tempData = 255;
    
  // Quickly pulse the nesLatch pin so that the register grab what it see on
  // its parallel data pins.
  digitalWrite(nesLatch, HIGH);
  digitalWrite(nesLatch, LOW);
 
  // Upon latching, the first bit is available to look at, which is the state
  // of the A button. We see if it is low, and if it is, we clear out variable's
  // first bit to indicate this is so.
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, A_BUTTON);
    
  // Clock the next bit which is the B button and determine its state just like
  // we did above.
  digitalWrite(nesClock, HIGH);
  digitalWrite(nesClock, LOW);
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, B_BUTTON);
  
  // Now do this for the rest of them!
  
  // Select button
  digitalWrite(nesClock, HIGH);
  digitalWrite(nesClock, LOW);
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, SELECT_BUTTON);

  // Start button
  digitalWrite(nesClock, HIGH);
  digitalWrite(nesClock, LOW);
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, START_BUTTON);

  // Up button
  digitalWrite(nesClock, HIGH);
  digitalWrite(nesClock, LOW);
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, UP_BUTTON);
    
  // Down button
  digitalWrite(nesClock, HIGH);
  digitalWrite(nesClock, LOW);
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, DOWN_BUTTON);

  // Left button
  digitalWrite(nesClock, HIGH);
  digitalWrite(nesClock, LOW);
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, LEFT_BUTTON);  
    
  // Right button
  digitalWrite(nesClock, HIGH);
  digitalWrite(nesClock, LOW);
  if (digitalRead(nesData) == LOW)
    bitClear(tempData, RIGHT_BUTTON);
    
  // After all of this, we now have our variable all bundled up
  // with all of the NES button states.*/
  return tempData;
}

void moveServo(int) {
    for(pos = 0; pos < slewdegrees; pos += 1) { // 1 degree steps
    myservo.write(90+pos);              // tell servo to go to position in variable 'pos'
    delayMicroseconds(delaymicros);                       // wait for the servo to reach the position
  }
  delay(1000); // wait a second
  for(pos = slewdegrees; pos > 0; pos -= 1) { // 1 degree steps
    myservo.write(90+pos);              // tell servo to go to position in variable 'pos'
    delayMicroseconds(delaymicros);                       // wait for the servo to reach the position
  }
  //delay(1000); // wait a second
}
