//Rotates servo motor 10 degrees clockwise 10deg and then counterclockwise 10deg after receiving a serial "x"

#include <PWMServo.h> //servo library 

PWMServo myservo; 

int serialState = 0;  

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9); //servo attached to pin 
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()>0){
    serialState = Serial.read();
    Serial.print(serialState);
      if (serialState=='x') { 
      for (pos = 10; pos >= 0; pos -= 1) { 
    // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(4);                       // waits for the servo to reach the position
  }
      delay(100);
        for (pos = 0; pos <= 10; pos += 1) { // goes from 10 degrees to 0 degrees
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(4);                       // waits for the servo to reach the position
  }
  delay(100);
//  serialState=0;
  }
}


}
