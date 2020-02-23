/*
*Persistence of Vision for use in saccade-based presentations. Uses APA102 (Dotstar) leds, sending colour values from
*an array held in flash memory (designated by 'const'). 
Documentation for FastLed is here: https://github.com/FastLED/FastLED/wiki
*/


#include "images.c"
#include "FastLED.h"

#define NUM_LEDS 32 //number of leds in strip 
#define DATA_PIN 11// spi data 
#define CLOCK_PIN 13//spi clock
#define COLOR_ORDER BGR //otherwise B&R get swapped

// Serial command verbs
#define POV_NO_MSG 0
#define POV_BRIGHTNESS 'b'
#define POV_CYCLE 'c'
#define POV_PICK 'p'
#define POV_OFF 'o'
#define POV_SHOW 's'
#define POV_TIME 't'
#define POV_NIMAGES 'n'
#define POV_SEQUENCE 'q'

#define MAX_SEQUENCE 100

enum showStates {SHOW_OFF, SHOW_ON, SHOW_CYCLE, SHOW_SEQUENCE};

enum showStates state = SHOW_CYCLE;

int numberOfSlices = 32;
uint8_t CurrentBrightness = 255; //scaling function
int display_duration = 4000;
unsigned long time_to_stop = millis()+display_duration;

unsigned int CurrentImage = 0;
#define NUM_IMAGES 3
const unsigned int *imagelib[NUM_IMAGES] = {mario,zero,cross};

// Sequencing variables
char sequencetext[4*MAX_SEQUENCE];
int sequence[MAX_SEQUENCE];
int sequence_pointer = 0;
int sequence_length = 0;
char *pch; // Pointer to tokens

/* Put variables to be controlled by PsychoPy via Serial.read() here
CurrentImage  --> what image is being presented
Brightness   --> 0-255
LineDelayMicroseconds   --> Delay between each line presented
ImageDelayMicroseconds   --> Delay between images
uint8_t CurrentBrightness = 255 --> Scaling function   

*/
CRGB leds[NUM_LEDS];

 
// Persistent serial variables
byte lastmsg; // Last command verb received
int expect; // Should we expect a numerical argument to follow?

void serial_handler() {
  // put your main code here, to run repeatedly:
  byte msg = 0;   // Serial message verb id
  if (expect) {
    expect--;
    switch (lastmsg) {
      case POV_BRIGHTNESS:
        CurrentBrightness = Serial.parseInt();
        if (CurrentBrightness >= 255)
          CurrentBrightness = 255;
        Serial.println(CurrentBrightness);
        FastLED.setBrightness(CurrentBrightness);
        lastmsg = POV_NO_MSG;
        break;
      case POV_PICK:
        CurrentImage = Serial.parseInt();
        if (CurrentImage >= NUM_IMAGES)
          CurrentImage = NUM_IMAGES-1;
        Serial.println(CurrentImage);
        lastmsg = POV_NO_MSG;
        break;
      case POV_TIME:
        display_duration = Serial.parseInt();
        Serial.println(display_duration);
        lastmsg = POV_NO_MSG;
        break;
      case POV_SEQUENCE:
        sequence_pointer = 0;
        while (Serial.available() > 1) {
          sequence[sequence_pointer++] = Serial.parseInt();
        }
        sequence_length = sequence_pointer;
        sequence_pointer = 0;
        for (sequence_pointer = 0; sequence_pointer < sequence_length; sequence_pointer++) {
          Serial.print(sequence[sequence_pointer]);
          Serial.print(",");
        }
        Serial.println("...");
        sequence_pointer = 0;
        lastmsg = POV_NO_MSG;
        state = SHOW_SEQUENCE;
        break;
      default:
        break;
    }
  }
  if (msg = Serial.read()) {
    switch (msg) {
      case POV_SHOW:
        Serial.println("Displaying picture.");
        state = SHOW_ON;
        time_to_stop = millis() + display_duration;
        break;
      case POV_BRIGHTNESS:
        Serial.print("Setting brightness to ");
        expect = 1;
        break;
      case POV_OFF:
        Serial.println("Turning display off.");
        state = SHOW_OFF;
        BlankImage();
        break;
      case POV_PICK: 
        Serial.print("Selecting image ");
        expect = 1;
        break;
      case POV_CYCLE:
        Serial.println("Cycling through all images.");
        state = SHOW_CYCLE;
        break;
      case POV_SEQUENCE:
        Serial.print("Showing image sequence  ");
        time_to_stop = millis() + display_duration;
        expect = 1;
        break;
      case POV_TIME: 
        Serial.print("Setting display time to ");
        expect = 1;
        break;
      case POV_NIMAGES:
        Serial.println(NUM_IMAGES);
        break;
      default:
        break;
    }
    lastmsg = msg;
  }
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(400);
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);  // enable access to LEDs on Prop Shield
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalSMD5050);// http://fastled.io/docs/3.1/group___color_enums.html
  delay(200);
  FastLED.setTemperature(TypicalSMD5050); // http://fastled.io/docs/3.1/group___color_enums.html
  FastLED.setBrightness(CurrentBrightness);
  lastmsg = POV_NO_MSG;
}

void BlankImage(){
     for(int z=NUM_LEDS;z>0;z--){
     leds[z-1]=0;}
     FastLED.show();
}

void PresentImage(const unsigned int array[]){
  int f= numberOfSlices;
  int z; //a counter
  int j=NUM_LEDS;
    for (int x=0;x<f;x++){
     for(z=NUM_LEDS;z>0;z--){
     leds[z-1]=array[x+((j-z)*f)];}
     FastLED.show();
     delayMicroseconds(40); //increase / testing indicates that this adds a constant to a 136microsecond line drawing time
    }
    delayMicroseconds(1000); //increase / Testing indicates this adds a constant to a 2 microsecond delay between presentations
}


void loop() {
  serial_handler();
  if ((state == SHOW_ON) && (millis() > time_to_stop)) {
    Serial.println("Turning off picture.");
    state = SHOW_OFF;
    BlankImage();
  }
   if ((state == SHOW_CYCLE) && (millis() > time_to_stop)) {
    CurrentImage++;
    time_to_stop = millis() +display_duration;
    if (CurrentImage >= NUM_IMAGES)
      CurrentImage = 0;
  }
  if (state == SHOW_SEQUENCE) {
    if (millis() > time_to_stop) {
      Serial.println("Turning off picture.");
      state = SHOW_OFF;
      BlankImage();
    } else {
      if (sequence_pointer >= sequence_length) {
        sequence_pointer = 0;
      }
      CurrentImage = sequence[sequence_pointer++];   
    }
  }
  if (state != SHOW_OFF) {
    PresentImage(imagelib[CurrentImage]); //show image once
  }
}
