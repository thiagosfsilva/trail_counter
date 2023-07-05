# Open Source outdoor people count

This project documents the steps necessary to build an automated people counter that can be used to track people trafic outdoors. It was origimally developed to track trail users on the Ben Lawers region of Scotland. 

## Bill of Materials
- Raspberry Pi Pico
- Adafruit PiCowbell Adalogger.
- Waterproof Ultrasonic Distance Sensor
- 5V BuckBoost converter
- 3AA battery case
- 3D printed inner and outer case

## Software

The controller logic was implemnented using CircuitPython. The ma.py script contains the regular operation logic, while the set_time.py script can be used to se the time on the PiCowbell Real Time Clock (RTC).
