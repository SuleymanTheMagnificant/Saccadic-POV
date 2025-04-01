#ifndef _FLASHSTORAGE_H
#define _FLASHSTORAGE_H
#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

//general file access functions
//read 16-bit (2 byte) unsigned int from file
uint16_t read16(File &f);
//read 32-bit (4 byte) unsigned int from file
uint32_t read32(File &f);
//read line (until \n ) from file and save it to l
//skips all whitespace (including CR and tab)
int readLine(File &f, char  l[]);

const int chipSelect = 10;

//Global variables

#endif
