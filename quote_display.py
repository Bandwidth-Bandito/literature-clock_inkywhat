#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import random
import logging
import time
import json
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT

# Logging setup
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

# Font size settings
large_quote_font_size = 36
medium_quote_font_size = 28
small_quote_font_size = 20
min_quote_font_size = 14  # Set a reasonable minimum for readability
base_author_font_size = 14  # Make author font size smaller for single-line display
line_spacing = 6  # Line spacing between lines
max_display_width = 400  # Maximum width for the text
max_display_height = 280  # Maximum height for the text (excluding author text)

class QuoteDisplay:
    """Class to manage the quotes and display on InkyWHAT"""

    inky_display = InkyWHAT('red')  # Use 'red' as the color variant

    def __init__(self, fixedTime=''):
        self.fixedTime = fixedTime
        self.currentMin = -1
        self.quote_data = {}
        self.loadData()
        self.update_display()

    def loadData(self):
        """Load quote data from JSON files"""
        self.quote_data = {}
        base_path = "/home/pi/literature-clock_inkywhat/docs/times"
        for hours in range(24):
            for mins in range(60):
                time_str = "{:02d}_{:02d}".format(hours, mins)
                filename = f"{base_path}/{time_str}.json"
                if os.path.exists(filename):
                    try:
                        with open(filename, 'r') as jfile:
                            self.quote_data[time_str] = json.load(jfile)
                    except Exception as e:
                        log.error(f"Cannot load {filename}: {e}")

    def get_quote(self, time_str):
        """Get a quote for a specific time"""
        if time_str in self.quote_data:
            return random.choice(self.quote_data[time_str])
        else:
            return {"quote_first": f"There is no quote for {time_str}", "quote_time_case": "", "quote_last": "", "title": "N/A", "author": "Marcel Kurtz"}

    def update_display(self):
        """Update the display with the current time and quote"""
        while True:
            now = datetime.now()
            current_time = now.strftime('%H_%M')

            if now.minute != self.currentMin:
                self.currentMin = now.minute
                log.debug(f'Updating display for {current_time}')

                quote_info = self.get_quote(current_time if not self.fixedTime else self.fixedTime)

                img = Image.new("P", (400, 300), QuoteDisplay.inky_display.WHITE)
                draw = ImageDraw.Draw(img)

                # Process the text and handle <br> tags
                quote_first = quote_info['quote_first'].replace('<br>', '\n').replace('<br/>', '\n')
                quote_time = quote_info['quote_time_case'].strip()  # Remove any leading/trailing spaces
                quote_last = quote_info['quote_last'].replace('<br>', '\n').replace('<br/>', '\n')

                # Separate the time to be on its own line
                full_quote = f"{quote_first}\n{quote_time}\n{quote_last}"

                # Choose font size based on the length of the quote
                quote_length = len(full_quote)
                if quote_length < 100:
                    quote_font_size = large_quote_font_size
                elif quote_length < 200:
                    quote_font_size = medium_quote_font_size
                else:
                    quote_font_size = small_quote_font_size

                quote_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', quote_font_size)
                wrapped_quote = self.wrap_text(full_quote, quote_font, max_display_width)

                # Center the text vertically within the available space
                total_text_height = self.calculate_text_height(wrapped_quote, quote_font)
                y_position = (max_display_height - total_text_height) // 2

                lines = wrapped_quote.split('\n')
                for line in lines:
                    # Calculate x_position to ensure the text is centered but fully uses the available width
                    text_width = draw.textlength(line, font=quote_font)
                    x_position = max((max_display_width - text_width) // 2, 0)  # Center text horizontally, ensure no negative value
                    draw.text((x_position, y_position), line, fill=QuoteDisplay.inky_display.BLACK, font=quote_font)
                    y_position += quote_font_size + line_spacing

                # Author text and positioning - Ensure it's in one line at the bottom
                author_text = f"{quote_info['title']} - {quote_info['author']}"
                author_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', base_author_font_size)
                author_text_width, author_text_height = draw.textbbox((0, 0), author_text, font=author_font)[2:4]

                # Positioning the author text at the bottom-left corner
                draw.text((10, 300 - author_text_height - 10), author_text, fill=QuoteDisplay.inky_display.BLACK, font=author_font)

                # Rotate the image and display it
                img = img.rotate(180, expand=True)
                QuoteDisplay.inky_display.set_image(img)
                QuoteDisplay.inky_display.show()

            time.sleep(60)

    def wrap_text(self, text, font, max_width):
        """Wrap text for drawing on the display"""
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            # Test if adding the word exceeds the maximum width
            if font.getbbox(current_line + word)[2] <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return "\n".join(lines)

    def calculate_text_height(self, text, font):
        """Calculate the height of the wrapped text"""
        lines = text.split('\n')
        return len(lines) * (font.size + line_spacing) - line_spacing

if __name__ == "__main__":
    QuoteDisplay()
