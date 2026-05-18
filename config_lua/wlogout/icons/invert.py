#!/usr/bin/env python3

from PIL import Image
import sys

image_name = sys.argv[1]

image = Image.open(image_name)
image = image.convert('RGBA') # Ensure image has an alpha channel

pixels = image.load()
width, height = image.size

for x in range(width):
    for y in range(height):
        r, g, b, a = pixels[x, y]
        # Check if the pixel is white (or close to white)
        if r > 200 and g > 200 and b > 200: # Adjust threshold as needed
            pixels[x, y] = (0, 0, 0, a) # Change to black, keep original alpha

image.save("dark_" + image_name)
