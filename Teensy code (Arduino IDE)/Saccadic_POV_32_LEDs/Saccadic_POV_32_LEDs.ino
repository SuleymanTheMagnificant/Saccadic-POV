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

bool cycle = true;
int numberOfSlices = 32;
uint8_t CurrentBrightness = 255; //scaling function
int display_duration = 4000;
unsigned long time_to_stop = millis()+display_duration;

unsigned int CurrentImage = 0;
const unsigned int *imagelib[3] = {mario,zero,cross};

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
int expect; // How many more bytes to expect for lastmsg
bool showing; // Is image currently being displayed?

void serial_handler() {
  // put your main code here, to run repeatedly:
  byte msg = 0;   // Serial message verb id
  if (msg = Serial.read()) {
    if (expect) {
      expect--;
      switch (lastmsg) {
        case POV_BRIGHTNESS:
          CurrentBrightness = (msg-'0')*255/9;
          Serial.println(CurrentBrightness);
          FastLED.setBrightness(CurrentBrightness);
          lastmsg = POV_NO_MSG;
          break;
        case POV_PICK:
          CurrentImage = msg-'0';
          Serial.println(CurrentImage);
          lastmsg = POV_NO_MSG;
          break;
        case POV_TIME:
          display_duration = (msg-'0')*1000;
          Serial.println(display_duration);
          lastmsg = POV_NO_MSG;
          break;
        default:
          break;
      }
    }
    switch (msg) {
      case POV_SHOW:
        Serial.println("Displaying picture.");
        showing = true;
        cycle = false;
        time_to_stop = millis() + display_duration;
        break;
      case POV_BRIGHTNESS:
        Serial.print("Setting brightness to ");
        expect = 1;
        break;
      case POV_OFF:
        Serial.println("Turning display off.");
        showing = false;
        cycle = false;
        BlankImage();
        break;
      case POV_PICK: 
        Serial.print("Selecting image ");
        expect = 1;
        break;
      case POV_CYCLE:
        Serial.println("Cycling through all images.");
        cycle = true;
        showing = false;
        break;
      case POV_TIME: 
        Serial.print("Setting display time to ");
        expect = 1;
        break;
      default:
        break;
    }
    lastmsg = msg;
  }
}

void setup() {
  Serial.begin(9600);
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
  if (showing && (millis() > time_to_stop)) {
    Serial.println("Turning off picture.");
    showing = false;
    BlankImage();
  }
   if (cycle && (millis() > time_to_stop)) {
    if (CurrentImage > 1)
      CurrentImage = 0;
    else
      CurrentImage++;
      time_to_stop = millis() +display_duration;
  }
  if (showing || cycle) {
    PresentImage(imagelib[CurrentImage]); //show image once
  }
}
