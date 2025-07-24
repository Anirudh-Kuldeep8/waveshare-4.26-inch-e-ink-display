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
LOGO_FILE = 'logo.bmp' # <<< YOUR LOGO FILENAME HERE

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Starting E-Ink Logo and Text Looper")
    
    # Initialize the e-paper display
    epd = epd4in26.EPD()
    
    logging.info("Initializing display for the first time...")
    epd.init()
    epd.Clear()
    logging.info("Initialization and initial clear complete.")

    # Load fonts (sizes increased)
    # Make sure 'Font.ttc' is present in your 'pic' directory
    font_large = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 50)
    font_medium = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

    # --- Load the logo ---
    logo_path = os.path.join(picdir, LOGO_FILE)
    if not os.path.exists(logo_path):
        logging.error(f"Logo file not found at {logo_path}. Please ensure it exists.")
        # Create a dummy empty image if logo is not found, so the script can run.
        logo_image = Image.new('1', (1, 1), 255) 
    else:
        logging.info(f"Loading logo from {logo_path}")
        logo_image = Image.open(logo_path)

    # --- Main Loop ---
    while True:
        # --- Display First Text: "ThinkRobotics" ---
        logging.info(f"Displaying: '{TEXT_1}' with logo")
        
        # A full init and clear is recommended before each full refresh to prevent ghosting
        epd.init()
        # epd.Clear() # The new image overwrites the whole screen, so clear is optional here
        
        # Create a new blank image in horizontal mode
        h_image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(h_image)
        
        # --- Paste Logo ---
        logo_x = (epd.width - logo_image.width) // 2
        logo_y = 20 # Padding from the top
        h_image.paste(logo_image, (logo_x, logo_y))
        
        # --- Draw Text ---
        # Calculate text position to center it below the logo
        bbox = draw.textbbox((0, 0), TEXT_1, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_x = (epd.width - text_width) // 2
        text_y = logo_y + logo_image.height + 20 # Position text below logo with padding
        
        draw.text((text_x, text_y), TEXT_1, font=font_large, fill=0)
        
        # Send the image to the display
        epd.display(epd.getbuffer(h_image))
        time.sleep(DELAY_SECONDS)

        # --- Display Second Text: "this is where you begin" ---
        logging.info(f"Displaying: '{TEXT_2}' with logo")
        
        epd.init()
        # epd.Clear()

        h_image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(h_image)

        # --- Paste Logo ---
        h_image.paste(logo_image, (logo_x, logo_y))

        # --- Draw Text ---
        bbox = draw.textbbox((0, 0), TEXT_2, font=font_medium)
        text_width = bbox[2] - bbox[0]
        text_x = (epd.width - text_width) // 2
        text_y = logo_y + logo_image.height + 20

        draw.text((text_x, text_y), TEXT_2, font=font_medium, fill=0)
        
        epd.display(epd.getbuffer(h_image))
        time.sleep(DELAY_SECONDS)

except KeyboardInterrupt:    
    logging.info("Ctrl+C detected. Exiting gracefully.")
    logging.info("Clearing display...")
    epd.init()
    epd.Clear()
    logging.info("Putting display to sleep.")
    epd.sleep()
    epd4in26.epdconfig.module_exit(cleanup=True)
    exit()
    
except IOError as e:
    logging.info(e)
    
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
    traceback.print_exc()

