/*
*Persistence of Vision for use in saccade-based presentations. Uses APA102 (Dotstar) leds, 
reading BMP files from an attached SD card and displaying them.
Serial input is used to control the images shown.

Uses Teensy 4.0.

Uses code from POV library by Alexander Kirillov <shurik179@gmail.com>
 * See github.com/shurik179/pov-library for details

 *  Requires the following libraries:
 *  FastLED
Documentation for FastLed is here: https://github.com/FastLED/FastLED/wiki
*/

#include <FastLED.h>
#include "pov.h"
//number of pixels in your strip/wand
#define NUM_PIXELS 32
// Strip type. Common options are DOTSTAR (APA102, SK9822) and NEOPIXEL (WS2812B, SK6812 and
// compatible). For other options, see FastLED documentation
#define LED_TYPE DOTSTAR
// color order. For DOTSTAR (APA102), common order is BGR
// For NeoPixel (WS2812B), most common is  GRB
#define COLOR_ORDER BGR

#define DATA_PIN 26
#define CLOCK_PIN 27


// frame rate
//#define LINES_PER_SEC 150.0f
#define LINES_PER_SEC 5000.0f

uint32_t interval=1000000/LINES_PER_SEC; //interval between lines of image, in microseconds

#define IMAGE "Mario.bmp"


/* Global Variables */
CRGB leds[NUM_PIXELS];
POV staff(NUM_PIXELS, leds);



void setup(){
// If using hardware SPI, use this version
//    FastLED.addLeds<LED_TYPE, COLOR_ORDER>(leds, NUM_PIXELS);
//If NOT using hardware SPI, comment the previous line. Instead,
// use one of the versions below,
// replacing DATA_PIN and CLOCK_PIN by correct pin numbers
  FastLED.addLeds<DOTSTAR, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_PIXELS);
// FastLED.addLeds<NEOPIXEL, DATA_PIN, COLOR_ORDER>(leds, NUM_PIXELS);

  //otherwise, regular show
  staff.begin(MODE_SHOW);
  // blink to indicate that staff is alive and working.
  // You can use any of predefined CRGB colors: https://github.com/FastLED/FastLED/wiki/Pixel-reference#predefined-colors-list
  // You can also omit the color; in this case, it will default to red.
  staff.blink(CRGB::Red);
  staff.addImage(IMAGE);

}

void loop(){
    if (staff.timeSinceUpdate()>interval) {
        staff.showNextLine();
    }
}
