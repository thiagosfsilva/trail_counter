import board
import busio
import adafruit_pcf8523
import digitalio
import time

###### Add time to set here: #######
# year, month, day, hour, minut, second, weekday (Mon=0)
# leave the two -1 at the end as is
t = time.struct_time(tm_year=2023, tm_mon=7, tm_mday=12, tm_hour=9, tm_min=23, tm_wday=2, tm_yday=-1, tm_isdst=-1)
######################################

# Internal LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# RTC clock via i2c
I2C = busio.I2C(board.GP5, board.GP4)
rtc = adafruit_pcf8523.PCF8523(I2C)

# Set the time and blink LEDS to confirm
rtc.datetime = t
print("Setting time to:", t)