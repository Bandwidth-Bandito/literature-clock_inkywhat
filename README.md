# Literature Clock Quote Display
This Python script is designed to display literary quotes on an InkyWHAT e-ink screen for every minute of the day. The script fetches quotes from JSON files stored for each specific time and dynamically adjusts the text size to fit the display.

# How does the script work?
Displaying the Quote: It selects a random quote for each time slot and displays it on the InkyWHAT e-ink display. If no quote is found, a default fallback message is used.
Text Wrapping and Centering: Text is wrapped to fit within the display width, and the entire quote is centered on the screen to ensure optimal readability.
Service Integration: This script is designed to run as a system service to ensure it continuously updates the display, even after reboots or crashes.

# Requirements
InkyWHAT Display: The script is specifically designed for the InkyWHAT e-ink screen with a 'red' color variant.
Python Dependencies: Requires Pillow for image manipulation, Inky for controlling the e-ink display, and standard libraries like datetime, os, and json.
Usage:
The script should be run on a Raspberry Pi connected to the InkyWHAT display. It is recommended to set this up as a service that starts at boot to ensure continuous operation.









# The work is based on:

The work of JohannesNE.
The work of tafj0.

Clock using time quotes from the literature, based on work and idea by
        [Jaap Meijers](http://www.eerlijkemedia.nl/) ([E-reader clock](https://www.instructables.com/id/Literary-Clock-Made-From-E-reader/)).
