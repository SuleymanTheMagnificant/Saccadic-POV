/*
*Persistence of Vision for use in saccade-based presentations. Uses APA102 (Dotstar) leds, sending colour values from
*an array held in flash memory (designated by 'const'). 
API for M5Stack is here https://docs.m5stack.com/#/en/api/lcd
Documentation for FastLed is here: https://github.com/FastLED/FastLED/wiki

This version is for a Teensy 4.0 and accepts serial input to present a gnome or a sword
*/

#include "images.c"
#include "FastLED.h"

#define NUM_LEDS 64 //number of leds in strip 
#define DATA_PIN 11// spi data 
#define CLOCK_PIN 13//spi clock
#define COLOR_ORDER BGR //otherwise B&R get swapped

int numberOfSlices = 64;
int PsyPi_Byte;

CRGB leds[NUM_LEDS];


void setup() {
  Serial.begin(9600);
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalSMD5050);// http://fastled.io/docs/3.1/group___color_enums.html
  delay(200);
  FastLED.setTemperature(TypicalSMD5050); // http://fastled.io/docs/3.1/group___color_enums.html
  Serial.println("Enter g for a gnome, or m for a Minecraft sword");
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
  if(Serial.available() >0){
    PsyPi_Byte=Serial.read();
    if(PsyPi_Byte == 'g'){
      PresentImage(4000, gnome);
    }
      if(PsyPi_Byte == 'm'){
      PresentImage(4000, minecraft);
    }
    }
  }
 //   PresentImage(4000,gnome);
 //   PresentImage(4000,minecraft);
 
 
