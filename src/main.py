# GPIO pins used by the PiCowBell
# GPIO5 = Clock SCL i2c
# GPIO4 = Clock SDA i2c
# GPIO16 = SD SPI MISO
# GPIO18 = SD SPI SCK
# GPIO18 = SD SDI MOSI
# GPIO17 = SD SDI CS# Write your code here :-)

import board
import busio
import digitalio
import time
import adafruit_pcf8523
import sdcardio
import storage
import adafruit_mcp9808
from set_time import set_time

####################################################
# SETUP VARIABLES - CHANGE CODE HERE ONLY!
####################################################

###### Enable this line to set time: #######
# year, month, day, hour, minut, second, weekday (Mon=0)
# leave the two -1 at the end as is
set_time(tm_year=2023, tm_mon=7, tm_mday=12, tm_hour=9, tm_min=23, tm_wday=2, tm_yday=-1, tm_isdst=-1)

start_count = 1

####################################################

##### Defining connections and devices

# Distance Sensor via UART0
dist_uart = busio.UART(baudrate=9600, tx=board.GP12, rx=board.GP13)

# RTC clock via i2c
I2C = busio.I2C(board.GP5, board.GP4)
rtc = adafruit_pcf8523.PCF8523(I2C)

# Internal LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# SD card via SPI
SD_CS = board.GP17
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
try:
    storage.mount(vfs, "/sd")
    print("sd card mounted")
except ValueError:
    print("no SD card")

#### Helper functions

## LED Blinker

def blink_led(times):
    for _ in range(times):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)
        

### SD write
def sd_write(count,t,fname="/sd/log.txt",mode="a"):
    try:
        with open(fname,mode) as f:
            date_str = "%d-%d-%d" % (t.tm_year, t.tm_mon, t.tm_mday)
            time_str = "%d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
            f.write(f'{count},{date_str},{time_str}\n')
            print(f"Writing to SD card complete on {date_str} {time_str}")
    except ValueError:
        print("initial write to SD card failed - check card")

print('Setup finished - starting loop\n')
blink_led(5)
led.value = False

#### Action loop
count = start_count

while True: #count < 5:
    t = rtc.datetime
    dist_data = dist_uart.read(4)
    dist = int.from_bytes(dist_data[1:3],'big')/10
    if dist < 50:
        print("Motion detected at %f cm on %d:%02d:%02d" % (dist,t.tm_hour, t.tm_min, t.tm_sec))
        sd_write(count=count,t=t)
        blink_led(2)
        count += 1
        time.sleep(2)
    else:
        print(f'No motion, distance is {dist} cm')

