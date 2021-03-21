#!/usr/bin/env python3

import time
import sys
import Adafruit_SSD1306
import Adafruit_DHT

from mqtt import HealthMQTT
from heartrate_monitor import HeartRateMonitor

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# import subprocess

# DHT Settings
sensor = Adafruit_DHT.DHT22
pin = 4

# SSD1306 Settings
RST = None  # on the PiOLED this pin isnt used

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Connect to AWS
connect = HealthMQTT("dmmargu_rpi-700d", "a3qcaf2g3pxx6x-ats.iot.us-east-1.amazonaws.com", "iothealth-topic")
message = {}

hrm = HeartRateMonitor(print_raw=False, print_result=False)
hrm.start_sensor()

# IoT HealthStation Variables
deviceid = "rpi-700d"  # modify this to provide device ID
latitude = 42.329  # modify this to provide healthstation latitude
longitude = -71.247  # modify this to provide healthstation longitude
msg = "dmargulies#11115555"  # modify this to provide healthstation message (eg patientid)

try:
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if temperature is None:
            continue
        temperaturef = (temperature * 9 / 5) + 32
        bpm, spo2 = hrm.read()

        message["deviceid"] = deviceid
        message["bpm"] = bpm
        message["spo2"] = spo2
        message["temperaturef"] = temperaturef
        message["humidity"] = humidity
        message["latitude"] = latitude
        message["longitude"] = longitude
        message["msg"] = msg

        # Write two lines of text.
        draw.text((x, top), "HW: {0}".format(deviceid), font=font, fill=255)
        draw.text((x, top + 8), "ID: {0}".format(msg), font=font, fill=255)
        draw.text((x, top + 16), "BPM: {0: >4.1f} SpO2: {1: >3.1f}".format(bpm, spo2), font=font, fill=255)
        draw.text((x, top + 25), "T={0:0.1f}*F H={1:0.1f}%".format(temperaturef, humidity), font=font, fill=255)

        # Send message
        connect.sendmsg(message)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(0.2)

except KeyboardInterrupt:
    hrm.stop_sensor()
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # clear the screen on exit
    sys.exit(1)
