

#include <PWMServo.h> //servo library 

PWMServo myservo; 
const int buttonPin = 2;  
int buttonState = 0;  

int distance_deg, ms_per_degree, pause_ms;  // Slew parameters


int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  myservo.attach(9); //servo attached to pin 
  pinMode(buttonPin, INPUT_PULLUP);   
  distance_deg = 10;
  ms_per_degree = 4;
  pause_ms = 100;
}

// ======================================================================
// ========================  Serial Handling ============================
// ======================================================================

// Serial command verbs
#define SERVO_NO_MSG 0
#define SERVO_DISTANCE_DEG 'd'
#define SERVO_MS_PER_DEGREE 's'
#define SERVO_PAUSE_MS 'p'
#define SERVO_BEGIN 'x'
#define SERVO_HELP '?'

// Persistent serial variables
byte lastmsg; // Last command verb received
int expect; // Should we expect a numerical argument to follow?

bool servo_serial_handler() {

  byte msg = 0;   // Serial message verb id
  if (expect) {
    expect--;
    switch (lastmsg) {
      case SERVO_DISTANCE_DEG:
        distance_deg = Serial.parseInt();
        Serial.println(distance_deg);
        lastmsg = SERVO_NO_MSG;
        break;
      case SERVO_PAUSE_MS:
        pause_ms = Serial.parseInt();
        Serial.println(pause_ms);
        lastmsg = SERVO_NO_MSG;
        break;
      case SERVO_MS_PER_DEGREE:
        ms_per_degree = Serial.parseInt();
        Serial.println(ms_per_degree);
        lastmsg = SERVO_NO_MSG;
        break;
      default:
        break;
    }
  }
  if (Serial.available()) {
    msg = Serial.read();
    switch (msg) {
      case SERVO_DISTANCE_DEG:
        Serial.print("Setting slew distance to ");
        expect = 1;
        break;
      case SERVO_MS_PER_DEGREE:
        Serial.print("Setting slew ms per degree to ");
        expect = 1;
        break;
      case SERVO_PAUSE_MS:
        Serial.print("Setting pause time to ");
        expect = 1;
        break;
      case SERVO_BEGIN:
        Serial.print("Slewing servo ");
        Serial.print(distance_deg);
        Serial.print(" degrees at ");
        Serial.print(ms_per_degree);
        Serial.println(" ms per degree.");
        break;
      case SERVO_HELP:
        Serial.println(F("Available commands:"));
        Serial.print(SERVO_BEGIN);Serial.println(F(": Begin servo slew"));
        Serial.print(SERVO_DISTANCE_DEG);Serial.println(F("<n>: Set slew distance to <n> degrees"));
        Serial.print(SERVO_MS_PER_DEGREE);Serial.println(F("<n>: Set slew speed to <n> milliseconds per degree"));
        Serial.print(SERVO_PAUSE_MS);Serial.println(F("<n>: Set slew pause to <n> milliseconds"));
        Serial.print(SERVO_HELP);Serial.println(F(": Display this help message"));
      default:
        break;
    }

    lastmsg = msg;

    if (msg == SERVO_BEGIN) {
      return true;
    } else {
      return false;
    }

  } else {
    return false;  // if no key is pressed
  }

}

void loop() {
 buttonState = digitalRead(buttonPin);
  if (servo_serial_handler() || (buttonState == LOW)) { // Handle serial input or button press
  for (pos = distance_deg; pos >= 0; pos -= 1) { 
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
  }


}
