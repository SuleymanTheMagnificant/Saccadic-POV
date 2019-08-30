/*
*Persistence of Vision for use in saccade-based presentations. Uses APA102 (Dotstar) leds, sending colour values from
*an array held in flash memory (designated by 'const'). 
API for M5Stack is here https://docs.m5stack.com/#/en/api/lcd
*/

#include "images.c"
#include "FastLED.h"
#include <M5Stack.h>

#define NUM_LEDS 32 //number of leds in strip 
#define DATA_PIN 21// spi data
#define CLOCK_PIN 22//spi clock
CRGB leds[NUM_LEDS];
int numberOfSlices = 32;


void setup() {
  Serial.begin(115200);
  M5.begin();
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN>(leds, NUM_LEDS);
  delay(200);
  
}
/*if(Serial.available()> 0){
    Serial.write("Enter which image you want to present");
    int ImageNumber = Serial.read();
    switch (ImageNumber) {
      case '1':
        Image=mario;
      case '2':
        Image=cross;
      case '3':
        Image=zero;
    }}};*/
    
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
  
//    M5.Lcd.drawBmpFile(SD,"/cross.bmp", 0, 0);
    PresentImage(4000,cross); //show image for 4 secs
//    M5.Lcd.fillScreen(TFT_BLACK);
//    M5.Lcd.drawBmpFile(SD,"/zero.bmp", 0, 0);
    PresentImage(4000,zero);
    M5.Lcd.fillScreen(TFT_BLACK);
    M5.Lcd.drawBmpFile(SD,"/mario.bmp", 100,100);
    PresentImage(4000,mario);
    M5.Lcd.fillScreen(TFT_BLACK);
 
 }
