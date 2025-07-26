#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys 
import time
import logging
import random
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont

sys.path.append("..")
from lib import LCD_1inch14

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 

logging.basicConfig(level=logging.DEBUG)

try:
    # Initialize display
    disp = LCD_1inch14.LCD_1inch14()
    disp.Init()
    disp.clear()
    disp.bl_DutyCycle(50)

    # Load fonts
    Font_large = ImageFont.truetype("../Font/Font00.ttf", 20)
    Font_small = ImageFont.truetype("../Font/Font02.ttf", 15)

    # Quotes to show
    quotes = [
        "Stay curious!",
        "Code. Debug. Repeat.",
        "Build something awesome.",
        "Push your limits!",
        "WaveShare rocks!",
        "Think. Tinker. Triumph.",
    ]

    # Setup ball animation
    x, y = 20, 20
    dx, dy = 3, 2
    radius = 10

    logging.info("Starting loop")
    while True:
        # Create image buffer
        image = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)

        # Draw a bouncing ball
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="RED")

        # Draw a random quote
        quote = random.choice(quotes)
        draw.text((5, 60), quote, font=Font_small, fill="BLUE")

        # Display to screen
        disp.ShowImage(image)

        # Bounce logic
        x += dx
        y += dy

        if x + radius >= disp.width or x - radius <= 0:
            dx = -dx
        if y + radius >= disp.height or y - radius <= 0:
            dy = -dy

        time.sleep(0.05)

except KeyboardInterrupt:
    disp.module_exit()
    logging.info("Exiting cleanly.")
except Exception as e:
    logging.exception("Unhandled error:")
    disp.module_exit()
