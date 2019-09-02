/*
*Persistence of Vision for use in saccade-based presentations. Uses APA102 (Dotstar) leds, sending colour values from
*an array held in flash memory (designated by 'const'). 
API for M5Stack is here https://docs.m5stack.com/#/en/api/lcd
Documentation for FastLed is here: https://github.com/FastLED/FastLED/wiki
*/

#include "images.c"
#include "FastLED.h"

#define NUM_LEDS 32 //number of leds in strip 
#define DATA_PIN 21// spi data 
#define CLOCK_PIN 22//spi clock
#define COLOR_ORDER BGR //otherwise B&R get swapped

int numberOfSlices = 32;

CRGB leds[NUM_LEDS];


void setup() {
  Serial.begin(115200);
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalSMD5050);// http://fastled.io/docs/3.1/group___color_enums.html
  delay(200);
  FastLED.setTemperature(TypicalSMD5050); // http://fastled.io/docs/3.1/group___color_enums.html
}
    
void PresentImage(unsigned long time, const unsigned int array[]){
  unsigned long currentTime = millis();
  while (millis()< currentTime + (time)) {
  int f= numberOfSlices;
  int z; //a counter
  int j=NUM_LEDS;
    for (int x=0;x<f;x++){
     for(z=NUM_LEDS;z>0;z--){
     leds[z-1]=array[x+((j-z)*f)];}
     FastLED.show();
     delayMicroseconds(40); //increase / decrease depending on presentation rate
     }       
    delayMicroseconds(1000); //increase / decrease depending on presentation rate
   }
 }

void loop() {  
    PresentImage(4000,cross); //show image for 4 secs
    PresentImage(4000,zero);
    PresentImage(4000,mario);
 }
 }
