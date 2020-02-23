# PyPOVLed python control library

This python library can be used to control an Arduino using the Saccadic_POV code.  Usage:

```
import pypovled
pov = pypovled.Pypovled('COM7')  // Arduino's serial port
pov.brightness(200)              // brightness out of 255
pov.time(5000)                   // time to present image, in milliseconds
pov.cycle()                      // cycle between all available images, showing each for "time"
pov.off()                        // turn off display
pov.pick(1)                      // pick an image to show
pov.show()                       // show selected image
pov.sequence([1,2])              // alternate rapidly between images in list
```
