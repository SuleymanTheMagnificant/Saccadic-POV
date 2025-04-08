

#include <PWMServo.h> //servo library 

PWMServo myservo; 
const int buttonPin = 2;  
int buttonState = 0;  

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9); //servo attached to pin 
  pinMode(buttonPin, INPUT);   
}

void loop() {
 buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) { 
  for (pos = 10; pos >= 0; pos -= 1) { 
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(4);                       // waits for the servo to reach the position
  }
  delay(1000);
  for (pos = 0; pos <= 10; pos += 1) { // goes from 10 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(4);                       // waits for the servo to reach the position
  }
  delay(1000);
  }


}
