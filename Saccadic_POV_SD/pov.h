#ifndef _STAFF_H
#define _STAFF_H
#include <Arduino.h>
#include <SPI.h>
#include <FastLED.h>
#include "config.h"
#include "flashstorage.h"
#include "bmpimage.h"


class POV {
    public:
        CRGB * leds;
        bool paused;

        POV(uint16_t length, CRGB * l);
        void begin();


        void setPixel(uint16_t i, uint32_t c);
        void blank();
        void show();
        void setBrightness(uint8_t b);

        /* quickly blink each 8th LED red, for "I am alive" indication */
        void blink(CRGB color=CRGB::Red);

        /* shows a value (0 -1.0) using LED staff as bar graph */
        void showValue(float v);

        /* Shows one line. line should be pointer to array which holds  pixel colors
         * (3 bytes per pixel, in BGR order). Note: 3, not 4!!!
         *  size should be size of array (number of pixels, not number of bytes)
         */
        void showLine(byte * line, uint16_t size);

        /* Reads from file an image and adds it to  the list, making it current
          image */
        void addImage(char * filename, uint16_t duration=0);

        /*
         reads list of images from file and adds it to the staff  imageList
         */
        uint8_t addImageList(char * filename);
        //remove all images from imagelist
        void clearImageList();
        
        // Select a new image to be current
        void selectImage(int selection);

        //make first image of image list current
        void firstImage();

        /* moves to the next image, making it current. If reached the end
         continues from first image
        */
        void nextImage();
        void prevImage();

        void restartImage(){currentLine = 0; lastLineUpdate=micros();}
        /* Show next line of active image
           Retunrs the index of next line to be shown (not yet shown!)
           If it retunrs 0, it means we have completed showing the image and
            next call will start again
        */
        int16_t showNextLine();

        //time since strip was last updated, in micro sec
        uint32_t timeSinceUpdate() {return (micros()-lastLineUpdate);}

        BMPimageList  imageList;

    private:
        uint16_t numPixels;
        int16_t currentLine=0;     //next line to be shown
        uint32_t lastLineUpdate=0; //time in microseconds

};



#endif
