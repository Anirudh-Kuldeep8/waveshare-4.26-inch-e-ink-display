#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import logging
from PIL import Image, ImageDraw, ImageFont
import traceback

# Define paths for picture and library directories
# This assumes your script is in a directory, and 'pic' and 'lib' are in the parent directory.
# Adjust these paths if your project structure is different.
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd4in26

# --- Configuration ---
TEXT_1 = "ThinkRobotics"
TEXT_2 = "this is where you begin"
DELAY_SECONDS = 3

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Starting E-Ink Text Looper")
    
    # Initialize the e-paper display
    epd = epd4in26.EPD()
    
    logging.info("Initializing display for the first time...")
    epd.init()
    epd.Clear()
    logging.info("Initialization and initial clear complete.")

    # Load fonts
    # Make sure 'Font.ttc' is present in your 'pic' directory
    font_large = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
    font_medium = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 28)

    # --- Main Loop ---
    while True:
        # --- Display First Text: "ThinkRobotics" ---
        logging.info(f"Displaying: '{TEXT_1}'")
        
        # A full init and clear is recommended before each full refresh to prevent ghosting
        epd.init()
        epd.Clear()
        
        # Create a new blank image in horizontal mode
        # '1' for 1-bit monochrome, 255 for white background
        h_image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(h_image)
        
        # Calculate text position to center it
        bbox = draw.textbbox((0, 0), TEXT_1, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x_pos = (epd.width - text_width) // 2
        y_pos = (epd.height - text_height) // 2
        
        # Draw the text
        draw.text((x_pos, y_pos), TEXT_1, font=font_large, fill=0)
        
        # Send the image to the display
        epd.display(epd.getbuffer(h_image))
        
        # Wait for the specified delay
        time.sleep(DELAY_SECONDS)

        # --- Display Second Text: "this is where you begin" ---
        logging.info(f"Displaying: '{TEXT_2}'")
        
        # Re-initialize and clear for the next refresh
        epd.init()
        epd.Clear()
        
        # Create a new blank image
        h_image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(h_image)
        
        # Calculate text position to center it
        bbox = draw.textbbox((0, 0), TEXT_2, font=font_medium)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x_pos = (epd.width - text_width) // 2
        y_pos = (epd.height - text_height) // 2
        
        # Draw the text
        draw.text((x_pos, y_pos), TEXT_2, font=font_medium, fill=0)
        
        # Send the image to the display
        epd.display(epd.getbuffer(h_image))
        
        # Wait for the specified delay
        time.sleep(DELAY_SECONDS)

except KeyboardInterrupt:    
    logging.info("Ctrl+C detected. Exiting gracefully.")
    logging.info("Clearing display...")
    epd.init()
    epd.Clear()
    logging.info("Putting display to sleep.")
    epd.sleep()
    # Safely exit the script
    epd4in26.epdconfig.module_exit(cleanup=True)
    exit()
    
except IOError as e:
    logging.info(e)
    
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
    traceback.print_exc()

