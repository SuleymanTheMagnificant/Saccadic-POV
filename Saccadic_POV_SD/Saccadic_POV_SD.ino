/*
*Persistence of Vision for use in saccade-based presentations. Uses APA102 (Dotstar) leds, 
reading BMP files from an attached SD card and displaying them.
Serial input is used to control the images shown.

Uses Teensy 4.1.

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

static char imagelist[] = "imagelist.txt";
//#define IMAGELIST "imagelist.txt"


/* Global Variables */
CRGB leds[NUM_PIXELS];
POV staff(NUM_PIXELS, leds);
uint32_t nextImageChange=0; //in milliseconds


// ======================================================================
// ========================  Serial Handling ============================
// ======================================================================

// Serial command verbs
#define POV_NO_MSG 0
#define POV_BRIGHTNESS 'b'
#define POV_SET_SPEED 'v'
#define POV_CYCLE 'c'
#define POV_PICK 'p'
#define POV_NEXT '+'
#define POV_PREV '-'
#define POV_OFF 'o'
#define POV_SHOW 's'
#define POV_TIME 't'
#define POV_PRINT_SEQUENCE 'q'
#define POV_READ_SEQUENCE 'r'
#define POV_CLEAR_SEQUENCE 'x'
#define POV_LIST_FILES 'l'
#define POV_ADDFILE 'a'
#define POV_HELP '?'

enum showStates {SHOW_OFF, SHOW_ONCE, SHOW_CYCLE};

enum showStates state = SHOW_CYCLE;

// Persistent serial variables
byte lastmsg; // Last command verb received
int expect; // Should we expect a numerical argument to follow?

void serial_handler() {
  int brightness, speed, pick, dur;
  String filestr;
  char fname[MAX_FILENAME];

  byte msg = 0;   // Serial message verb id
  if (expect) {
    expect--;
    switch (lastmsg) {
      case POV_BRIGHTNESS:
        brightness = Serial.parseInt();
        if (brightness >= 255)
          brightness = 255;
        Serial.println(brightness);
        FastLED.setBrightness(brightness);
        lastmsg = POV_NO_MSG;
        break;
      case POV_SET_SPEED:
        speed = Serial.parseInt();
        Serial.println(speed);
        interval=1000000/speed;
        lastmsg = POV_NO_MSG;
        break;
      case POV_PICK:
        pick = Serial.parseInt();
        staff.selectImage(pick);
        Serial.print(pick); Serial.print(": ");
        staff.imageList.current()->getFilename(fname);
        Serial.println(fname);
        lastmsg = POV_NO_MSG;
        break;
      case POV_TIME:
        dur = Serial.parseInt();
        Serial.println(dur);
        staff.imageList.setDuration(dur);
        lastmsg = POV_NO_MSG;
        break;
      case POV_ADDFILE:
        filestr = Serial.readString(MAX_FILENAME).trim();
        Serial.println(filestr);
        filestr.toCharArray(fname,MAX_FILENAME);
        staff.addImage(fname,2);
        lastmsg = POV_NO_MSG;
        break;
      case POV_READ_SEQUENCE:
        filestr = Serial.readString(MAX_FILENAME).trim();
        Serial.println(filestr);
        filestr.toCharArray(fname,MAX_FILENAME);
        staff.addImageList(fname);
        lastmsg = POV_NO_MSG;
        break;

      default:
        break;
    }
  }
  if (Serial.available()) {
    msg = Serial.read();
    switch (msg) {
      case POV_SHOW:
        Serial.print("Displaying image ");
        staff.imageList.current()->getFilename(fname);
        Serial.println(fname);
        state = SHOW_ONCE;
        nextImageChange=millis()+staff.imageList.currentDuration()*1000;
        break;
      case POV_BRIGHTNESS:
        Serial.print("Setting brightness to ");
        expect = 1;
        break;
      case POV_SET_SPEED:
        Serial.print("Setting display speed to ");
        expect = 1;
        break;
      case POV_OFF:
        Serial.println("Turning display off.");
        state = SHOW_OFF;
        staff.blank();
        break;
      case POV_PICK: 
        Serial.print("Selecting image ");
        expect = 1;
        break;
      case POV_NEXT: 
        Serial.print("Selecting image ");
        staff.nextImage();
        staff.imageList.current()->getFilename(fname);
        Serial.println(fname);
        break;
      case POV_PREV: 
        Serial.print("Selecting image ");
        staff.nextImage();
        staff.imageList.current()->getFilename(fname);
        Serial.println(fname);
        break;
      case POV_CYCLE:
        Serial.println("Cycling through all images.");
        state = SHOW_CYCLE;
        nextImageChange=millis()+staff.imageList.currentDuration()*1000;
        break;
      case POV_TIME: 
        Serial.print("Setting display duration to ");
        expect = 1;
        break;
      case POV_PRINT_SEQUENCE:
        Serial.println("Current image sequence:");
        staff.imageList.print();
        break;
      case POV_CLEAR_SEQUENCE:
        Serial.println("Erasing image sequence!");
        staff.imageList.reset();
        break;
      case POV_READ_SEQUENCE:
        Serial.println("Reading image sequence from ");
        expect=1;
        break;
      case POV_LIST_FILES:
        Serial.println("Files on SD card:");
        SD.sdfs.ls();
        break;
      case POV_ADDFILE:
        Serial.print("Adding image to sequence: ");
        expect=1;
        break;
      case POV_HELP:
        Serial.println(F("Available commands:"));
        Serial.print(POV_CYCLE);Serial.println(F(": Cycle through image list"));
        Serial.print(POV_BRIGHTNESS);Serial.println(F(" <n>: Set brightness to <n>"));
        Serial.print(POV_SET_SPEED);Serial.println(F(" <n>: Set display speed (lines/sec) to <n>"));
        Serial.print(POV_PICK);Serial.println(F(" <n>: Select image <n> from list"));
        Serial.print(POV_NEXT);Serial.println(F(": Select next image from list"));
        Serial.print(POV_PREV);Serial.println(F(": Select previous image from list"));
        Serial.print(POV_OFF);Serial.println(F(": Turn off display"));
        Serial.print(POV_SHOW);Serial.println(F(": Show selected image once"));
        Serial.print(POV_TIME);Serial.println(F(" <n>: Set duration of selected image to <n> seconds"));
        Serial.print(POV_PRINT_SEQUENCE);Serial.println(F(": Show list of images to be shown"));
        Serial.print(POV_CLEAR_SEQUENCE);Serial.println(F(": Clear list images to be shown"));
        Serial.print(POV_READ_SEQUENCE);Serial.println(F(" <file>: Read list of images from <file>"));
        Serial.print(POV_ADDFILE);Serial.println(F(" <file>: Add <file> to list of images to be shown"));
        Serial.print(POV_LIST_FILES);Serial.println(F(": List all available files on SD card"));
        Serial.print(POV_HELP);Serial.println(F(": Display this help message"));
      default:
        break;
    }
    lastmsg = msg;
  }
}
// ======================================================================
// ========================  Setup ========= ============================
// ======================================================================


void setup(){
  FastLED.addLeds<DOTSTAR, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_PIXELS);

  staff.begin();
  // blink to indicate that staff is alive and working.
  // You can use any of predefined CRGB colors: https://github.com/FastLED/FastLED/wiki/Pixel-reference#predefined-colors-list
  // You can also omit the color; in this case, it will default to red.
  staff.blink(CRGB::Red);
//  staff.addImage(IMAGE);
// staff.addImageList(IMAGELIST);
  staff.addImageList(imagelist);
  nextImageChange=millis()+staff.imageList.currentDuration()*1000;
}

// ======================================================================
// ========================  Loop  ======================================
// ======================================================================


void loop(){

  char fname[MAX_FILENAME];

  serial_handler();

  if (state!=SHOW_OFF) {
    if (millis()>nextImageChange){
      if (state==SHOW_CYCLE) {
        staff.nextImage();
        Serial.print("Showing image ");
        staff.imageList.current()->getFilename(fname);
        Serial.println(fname);
        //determine when we will need to change the image
        nextImageChange=millis()+staff.imageList.currentDuration()*1000;
      } else {  // state was SHOW_ONCE, stop showing
        staff.blank();
        state=SHOW_OFF;
      }
    }
    if ((staff.timeSinceUpdate()>interval) && (state != SHOW_OFF)) {
        staff.showNextLine();
    }
  } 
}
