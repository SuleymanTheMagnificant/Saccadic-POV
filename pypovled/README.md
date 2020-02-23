# PyPOVLed python control library

This python library can be used to control an Arduino using the Saccadic_POV code.  Usage:

```
import pypovled
pov = pypovled.Pypovled('COM7')  // Arduino's serial port
pov.brightness(200)
pov.time(5000)
pov.cycle()
pov.off()
pov.pick(1)
pov.show()
pov.sequence([1,2])
```
