// Servo Saccade
// by Jason Goodman
// based on code by BARRAGAN <http://barraganstudio.com>
//
// Slew a servo at a rate similar to the saccade of a human eye.
// Note that for saccades of more than 20 degrees, a standard servo may not be able
// to move fast enough!
//
// Saccade time us = 2200 * degrees of slew + 21000
// Time for each degree us = 2200 + 21000/degrees
//
// Slew speed for 20 degree saccade: 2200+21000/20 = 3200 us/degree
// Max slew speed for my servo (unloaded): 90 degrees in 300 ms = 3300 us/degree

// Hookups:
// Brown servo wire (-) to GND
// Red servo wire (+) to 5v
// Yellow/orange wire (S) to pin 9 via 3v-5v level shifter

#include <PWMServo.h>

typedef enum {STD, DS760} servotypes;

const servotypes servo_type = DS760;

PWMServo myservo;  // create servo object to control a servo

float pos = 0.;    // variable to store the servo position

int slewdegrees = 60;
int delaymicros = 2200 + 2100/slewdegrees;
// int delaymicros = 10; // Super fast, for testing

float scalefactor = 1.0;  // Compensates for servos whose full travel is not 180 degrees

void setup() {
  if (servo_type == DS760) {
    myservo.attach(9,400,1100);  // attaches the servo on pin 9 to the servo object -- MKS DS760 servo timings
    scalefactor = 180.0/120.0;  // DS760 only goes 120 degrees
  } else {
    myservo.attach(9);  // attaches the servo on pin 9 to the servo object -- Standard servo
  }
  delaymicros = 2200+2100/slewdegrees;
}

void loop() {
  for(pos = 0.; pos < slewdegrees*scalefactor; pos += 1*scalefactor) { // 1 degree steps
    myservo.write(20+pos);              // tell servo to go to position in variable 'pos'
    delayMicroseconds(delaymicros);                       // wait for the servo to reach the position
  }
  delay(1000); // wait a second
  for(pos = slewdegrees*scalefactor; pos > 0.; pos -= 1*scalefactor) { // 1 degree steps
    myservo.write(20+pos);              // tell servo to go to position in variable 'pos'
    delayMicroseconds(delaymicros);                       // wait for the servo to reach the position
  }
  delay(1000); // wait a second
}
