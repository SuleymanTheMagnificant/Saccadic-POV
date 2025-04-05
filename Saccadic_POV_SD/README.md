# Saccadic POV SD

This Arduino project creates a persistence-of-vision display that can read .bmp image files from an attached SD card, and allows the operator to
interactively change the display using serial port commands.

Parts List:
* Teensy 4.1
* DotStar APA102 RGB LED strip

Connections:
* Teensy Pin 26 --> LED strip DATA
* Teensy Pin 27 --> LED strip CLK
* Teensy GND --> LED GND
* External 5V power --> LED strip VCC
* External 5V GND --> LED strip GND
* USB-serial connection to PC (9600 baud)

Libraries:
* FastLED https://github.com/FastLED/FastLED

SD card files:
* `imagelist.txt` : A list of BMP images to show.  Each line should contain a valid filename and a duration in seconds to show that file, separated by whitespace.
* BMP files: 24-bit format only.
  
Serial commands:
* `c`: Cycle through image list
* `b <n>`: Set brightness to `<n>`
* `v <n>`: Set display speed (lines/sec) to `<n>`
* `p <n>`: Select image `<n>` from list
* `+`: Select next image from list
* `-`: Select previous image from list
* `o`: Turn off display
* `s`: Show selected image once
* `t <n>`: Set duration of selected image to `<n>` seconds
* `q`: Show list of images to be shown
* `x`: Clear list images to be shown
* `r <file>`: Read list of images from `<file>`
* `a <file>`: Add `<file>` to list of images to be shown
* `l`: List all available files on SD card
* `?`: Display this help message

Author: Jason Goodman <goodman_jason@wheatoncollege.edu> (2025)

BMP display and SD-card code adapted from POV-Library (https://docs.arduino.cc/libraries/pov-library/) by Alexander Krillov (2022).