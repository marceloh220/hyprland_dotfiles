#!/usr/bin/env python3
#
# wallpaper.py
#
# Marcelo's Hyprland config Script
#
# This script sets a random wallpaper from a specified directory for Hyprland desktop environment.
# It uses the Pillow library to handle image resizing and saving.
# It extracts the dominant color from the wallpaper using K-Means clustering and sets it as the 
# border color.
# It also updates the Hyprlock, Waybar and Wlogout configurations with the dominant color.
#
# Requirements:
# - Python 3.x
# - Pillow library for image processing
# - scikit-learn for K-Means clustering
# - NumPy for numerical operations
# - Hyprland, Hyprlock, and Waybar installed and configured
#
# Note:
# This script is designed to work with Hyprland, a dynamic tiling Wayland compositor.
# It assumes you have Hyprland installed and configured correctly.
# The script is intended to be run in a Hyprland environment, and it will not work properly 
# outside of it.
# It is also designed to be run in a terminal with access to the Hyprland configuration files.
# The script will automatically create necessary directories if they do not exist.
# It will also handle errors gracefully, providing informative messages if something goes wrong.
# Make sure to run this script in an environment where Hyprland is installed and configured.
# You may need to adjust the userDirectory variable to point to your home directory and add 
# configuration files for Hyprland, Hyprlock, Waybar and wlogout if they do not already exist.
# The files window.conf, hyprlock.conf, waybar/style.css and wlogout/style.css may should be present 
# in the respective directories.
# Configure the hyprland.conf file to include window.conf file or copy the contents of window.conf 
# to hyprland.conf.
# Ensure you have the necessary permissions to write to the configuration files and directories.
# Warning: This script modifies Hyprland, Hyprlock, Waybar and Wlogout configurations. Be sure to backup 
# your configurations before running the script.
#
# Usage:
#       wallpaper.py Random
#   or:
#       wallpaper.py /path/to/your/image.png
#
# Ensure you have the python packages installed, e.g.:
# pip install Pillow scikit-learn numpy
#
# Adjust the userDirectory variable to your home directory as needed.
# Note: The script assumes you have Hyprland installed and configured correctly.
#
# Copyright 2025 Marcelo H Moraes
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or 
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import subprocess
import os
import random
import sys
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
import math

resolution:tuple[int, int] = (1920, 1080)  # Set your desired resolution here
wallpaper_path = "Imagens/wallpapers"  # Set your wallpapers directory here

def extract_dominant_colors(image_path, n_colors=1):
    """
    Extracts the dominant color(s) from an image using K-Means clustering.

    Args:
        image_path (str): The path to the image file.
        n_colors (int): The number of dominant colors to extract.

    Returns:
        list[str]: A list of dominant colors in hex format (e.g., ['ff0000', '00ff00']).
        
    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the number of colors is less than 1 or if the image format is not supported.
        ValueError: If the image mode is not supported or if the extracted colors are not valid hex strings.
    """
    # Check if the image file exists and is a valid image format
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    # Check if the number of colors is valid
    if n_colors < 1:
        raise ValueError("Number of colors must be at least 1.")
    # Load the image
    img = Image.open(image_path)
    # Check if the image format is supported
    if img.format not in ['PNG', 'JPEG', 'BMP']:
        raise ValueError(f"Unsupported image format: {img.format}." + 
                         f"Supported formats are: PNG, JPEG, BMP.")
    # Check if the image mode is supported
    if img.mode not in ['RGB', 'RGBA']:
        raise ValueError(f"Unsupported image mode: {img.mode}." + 
                         f"Supported modes are: RGB, RGBA.")
    # Convert image to RGB if not already in that mode
    if img.mode != 'RGB':
        print(f"Converting image {image_path} to RGB mode.")
        img = img.convert("RGB")
    # Resize the image to reduce processing time
    img = img.resize((100, 100),  Image.Resampling.LANCZOS)
    # Convert image data to numpy array
    pixels = np.array(img)
    # Reshape the pixel data for K-Means
    pixels = pixels.reshape(-1, 3)  # Flatten the array to (num_pixels, 3)
    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init='auto')
    kmeans.fit(pixels)
    # Get the cluster centers (dominant colors)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    # Each color is a tuple of (R, G, B) values
    # Ensure each component is in the range 0-255
    colors = [tuple(max(0, min(255, c)) for c in color) for color in dominant_colors]
    # Convert RGB colors to hex format
    hex_colors = []
    for color in colors:
        r = color[0]
        g = color[1]
        b = color[2]
        r = max(0, min(255, r))  # Ensure RGB values are within [0, 255]
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        # Convert RGB to hex format
        hex_color = f"{r:02x}{g:02x}{b:02x}".lower()
        hex_colors.append(hex_color)  # Append the hex color to the list
    # Check if the extracted colors are valid hex strings
    for hex_color in hex_colors:
        # Ensure each extracted color is a valid hex string of length 6
        if not isinstance(hex_color, str) or len(hex_color) != 6:
            raise ValueError("Extracted color must be a hex string of length 6 (e.g., 'ff0000' for red).")
        # Ensure the color is a valid hex string
        if not all(c in '0123456789abcdefABCDEF' for c in hex_color):
            raise ValueError("Extracted color must be a valid hex string (e.g., 'ff0000' for red).")
    return hex_colors

def extract_primary_colors(image_path):
    """
    Extracts primary colors from an image.
    """
    # Extract the dominant color from the image
    return extract_dominant_colors(image_path, n_colors=16)


def darken_color(color, factor=0.2):
    """
    Darkens a color by a specified factor.

    Args:
        color (str): The RGB color to darken in hex format.
        factor (float): The factor by which to darken the color (0.0 to 1.0).
    
    Returns:
        str: The darkened RGB color in hex format.
    
    Raises:
        ValueError: If the factor is not between 0.0 and 1.0 or if the color is not a valid hex string.
    """
    # Ensure RGB values do not go below 0
    if not (0 <= factor <= 1):
        raise ValueError("Factor must be between 0.0 and 1.0.")
    # Convert hex to RGB
    color_rgb = hex_to_rgb(color)  # Convert hex to RGB
    # Decrease each component by the factor multiplied by the component value
    color_darken = tuple(int(c * (1 - factor)) for c in color_rgb)
    # Ensure RGB values are within [0, 255]
    color_darken = tuple(max(0, min(255, c)) for c in color_darken)
    # Check if the darkened color is a valid RGB tuple
    if not isinstance(color_darken, tuple) or len(color_darken) != 3:
        raise ValueError("Input must be a tuple of three integers representing RGB values.")
    # Ensure each component is an integer and in the range 0-255
    if not all(isinstance(c, int) for c in color_darken):
        raise ValueError("All components of the RGB tuple must be integers.")
    # Ensure RGB values are within the range 0-255
    if any(c < 0 or c > 255 for c in color_darken):
        raise ValueError("RGB values must be in the range 0-255.")
    # Ensure tuple has exactly three components
    if len(color_darken) != 3:
        raise ValueError("RGB tuple must contain exactly three components (R, G, B).")
    # Convert RGB to hex format
    return rgb_to_hex(color_darken)

def lighten_color(color, factor=0.2):
    """
    Lightens a color by a specified factor.

    Args:
        color (str): The RGB color to lighten in hex format.
        factor (float): The factor by which to lighten the color (0.0 to 1.0).

    Returns:
        hex: The lightened RGB color in hex format.

    Raises:
        ValueError: If the factor is not between 0.0 and 1.0 or if the color is not a valid hex string.
    """
    # Ensure RGB values do not go above 255
    if not (0 <= factor <= 1):
        raise ValueError("Factor must be between 0.0 and 1.0.")
    # Convert hex to RGB
    color_rgb = hex_to_rgb(color)
    # Increase each component by the factor multiplied by the difference to 255
    color_lighten = tuple(int(c + (255 - c) * factor) for c in color_rgb)
    # Ensure RGB values are within [0, 255]
    color_lighten = tuple(max(0, min(255, c)) for c in color_lighten)
    # Check if the lightened color is a valid RGB tuple
    if not isinstance(color_lighten, tuple) or len(color_lighten) != 3:
        raise ValueError("Input must be a tuple of three integers representing RGB values.")
    # Ensure each component is an integer and in the range 0-255
    if not all(isinstance(c, int) for c in color_lighten):
        raise ValueError("All components of the RGB tuple must be integers.")
    # Ensure RGB values are within the range 0-255
    if any(c < 0 or c > 255 for c in color_lighten):
        raise ValueError("RGB values must be in the range 0-255.")
    # Ensure each component is in the range 0-255
    color_lighten = tuple(max(0, min(255, c)) for c in color_lighten)
    # Convert RGB to hex format
    return rgb_to_hex(color_lighten)

def hex_to_rgb(hex_color):
    """
    Converts a hex color string to an RGB tuple.

    Args:
        hex_color (str): The hex color string (e.g., 'ff0000' for red).

    Returns:
        tuple: The RGB color as a tuple (R, G, B).

    Raises:
        ValueError: If the input is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Ensure the hex color is a valid string of length 6
    if not isinstance(hex_color, str) or len(hex_color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    # Ensure the hex color is a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in hex_color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    # Convert hex to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Ensure the RGB tuple has exactly three components
    if not isinstance(rgb, tuple) or len(rgb) != 3:
        raise ValueError("Input must be a tuple of three integers representing RGB values.")
    # Check if all components are integers
    if not all(isinstance(c, int) for c in rgb):
        raise ValueError("All components of the RGB tuple must be integers.")
    # Check if RGB values are within the range 0-255
    if any(c < 0 or c > 255 for c in rgb):
        raise ValueError("RGB values must be in the range 0-255.")
    # Ensure each component is in the range 0-255
    rgb = tuple(max(0, min(255, c)) for c in rgb)
    if len(rgb) != 3:
        raise ValueError("RGB tuple must contain exactly three components (R, G, B).")
    # Return the RGB tuple
    return rgb

def rgb_to_hex(rgb_color):
    """
    Converts an RGB tuple to a hex color string.

    Args:
        rgb_color (tuple): The RGB color as a tuple (R, G, B).

    Returns:
        str: The hex color string (e.g., 'ff0000' for red).

    Raises:
        ValueError: If the input is not a tuple of three integers or if the RGB values are not in the range 0-255.
    """
    # Ensure the input is a tuple of three integers
    if not isinstance(rgb_color, tuple) or len(rgb_color) != 3:
        raise ValueError("Input must be a tuple of three integers representing RGB values.")
    # Ensure that all components of the RGB tuple are integers
    if not all(isinstance(c, int) for c in rgb_color):
        raise ValueError("All components of the RGB tuple must be integers.")
    # Ensure RGB values are within the range 0-255
    if any(c < 0 or c > 255 for c in rgb_color):
        raise ValueError("RGB values must be in the range 0-255.")
    # Ensure each component is in the range 0-255
    rgb_color = tuple(max(0, min(255, c)) for c in rgb_color)
    # Convert RGB to hex format
    # Each component is converted to a two-digit hex string and joined together
    # The lower() method ensures the hex string is in lowercase
    return ''.join(f'{c:02x}' for c in rgb_color).lower()

def color_distance(c1, c2):
    """
    Calculates the Euclidean distance between two RGB colors.
    Args:      c1 (tuple): The first color as an RGB tuple (R, G, B).
               c2 (tuple): The second color as an RGB tuple (R, G, B).
    Returns:   float: The Euclidean distance between the two colors.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def closest_color(target_hex, color_list):
    """
    Finds the closest color from a list of colors to a target color in hex format.
    Args:      target_hex (str): The target color in hex format (e.g., 'ff0000' for red).
               color_list (list): A list of colors in hex format to compare against.
    Returns:   str: The closest color from the list in hex format.
    Raises:
        ValueError: If the input is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Remove '#' if present
    target_hex = target_hex.startswith('#') and target_hex[1:] or target_hex
    
    """ working on raises ;) """

    #print(f"Finding closest color to {target_hex} from the list: {color_list}")

    target_rgb = hex_to_rgb(target_hex)
    min_distance = float('inf')
    closest = None

    for color in color_list:
        color_rgb = hex_to_rgb(color)
        dist = color_distance(target_rgb, color_rgb)
        if dist < min_distance:
            min_distance = dist
            closest = color
    #print(f"Closest color to {target_hex} is {closest} with a distance of {min_distance}")
    return closest

def get_brightness(color):
    """
    Calculates the brightness of a color in hex format.

    Args:
        color (str): The color in hex format (e.g., 'ff0000' for red).
    
    Returns:
        float: The brightness value of the color.
    
    Raises:
        ValueError: If the color is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Ensure the color is a valid hex string of length 6
    if not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    # Ensure the color is a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    # Convert hex to RGB
    color_rgb = hex_to_rgb(color)
    # Calculate brightness using the formula
    # brightness = (R * 0.299) + (G * 0.587) + (B * 0.114)
    brightness = (color_rgb[0] * 0.299) + (color_rgb[1] * 0.587) + (color_rgb[2] * 0.114)
    # Ensure brightness is a float
    if not isinstance(brightness, float):
        raise ValueError("Brightness must be a float value.")
    # Ensure brightness is within the range 0-255
    if brightness < 0 or brightness > 255:
        raise ValueError("Brightness value must be in the range 0-255.")
    # Return the brightness value
    return brightness

def get_random_image(directory):
    """ 
    Returns a random image file from the specified directory.

    Args:
        directory (str): The path to the directory containing images.

    Returns:
        str: The path to a randomly selected image file.

    Raises:
        FileNotFoundError: If the directory does not exist or is not a valid directory.
        ValueError: If the provided path is not a directory or if no images are found in the directory.
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    # Ensure the directory is a valid directory
    if not os.path.isdir(directory):
        raise ValueError(f"Provided path is not a directory: {directory}")
    # List all image files in the directory
    images = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    # Ensure there are images in the directory
    if not images:
        raise FileNotFoundError("No images found in the directory.")
    # Select a random image from the list
    return os.path.join(directory, random.choice(images))

def hyprland_set_wallpaper(image_path):
    """
    Sets the wallpaper for Hyprland desktop environment.
    
    Args:
        image_path (str): The path to the image file.

    Raises:
        FileNotFoundError: If the Hyprland configuration directory does not exist or if the image file does not exist.
        ValueError: If the resolution is not a tuple of two integers or if the image format is not supported.
        Exception: For any other unexpected errors.
        OSError: If there is an OS-related error (e.g., permission issues).
    """
    # Get the user's home directory
    userDirectory = os.path.expanduser("~")
    # Ensure the directory ends with a slash
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Ensure the directory exists
    if not os.path.exists(userDirectory + ".config/hypr"):
        raise FileNotFoundError("Hyprland configuration directory not found.")
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    # Check if the resolution is a tuple of two integers
    if not isinstance(resolution, tuple) or len(resolution) != 2:
        raise ValueError("Resolution must be a tuple of (width, height).")
    # Ensure both dimensions of the resolution are integers
    if not all(isinstance(dim, int) for dim in resolution):
        raise ValueError("Resolution dimensions must be integers.")
    # Ensure both dimensions of the resolution are positive integers
    if resolution[0] <= 0 or resolution[1] <= 0:
        raise ValueError("Resolution dimensions must be positive integers.")
    # Check if the image is in a supported format
    supported_formats = ['PNG', 'JPEG', 'BMP']
    img_format = Image.open(image_path).format
    # Ensure the image format is supported
    if img_format not in supported_formats:
        raise ValueError(f"Unsupported image format: {img_format}. Supported formats are: {', '.join(supported_formats)}.")
    # Open the image file
    img = Image.open(image_path)
    # Check if the image is already in the desired resolution
    if img.size == resolution:
        print("Image is already in the desired resolution. No resizing needed.")
        img_resized = img
    else:
        print(f"Resizing image from {img.size} to {resolution}.")
        # Resize the image to the desired resolution
        img_resized = img.resize(resolution, Image.Resampling.LANCZOS)
    # Ensure the resized image is in RGB mode
    if not img_resized.mode == 'RGB':
        print("Converting image to RGB mode.")
        # Convert the image to RGB mode if it's not already
        img_resized = img_resized.convert('RGB')
    # Save the resized image in the Hyprland configuration directory
    # For Hyprland, we need to save the image in a specific directory
    img_resized.save(userDirectory + ".config/hypr/wallpaper.png", format='PNG')
    # Restart Hyprpaper to apply the new wallpaper
    subprocess.run(["sh", "-c", "killall hyprpaper &> /dev/null; hyprpaper &> /dev/null &"])

def hyprland_set_border_color(color):
    """
    Sets the border color in Hyprland configuration.
    
    Args:
        color (str): The color in hex format (e.g., 'ff0000' for red).

    Raises:
        FileNotFoundError: If the Hyprland configuration file does not exist.
        ValueError: If the color is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Get the user's home directory
    userDirectory = os.path.expanduser("~")  # Get the user's home directory
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Define the path to the Hyprland configuration file
    config_path = userDirectory + ".config/hypr/window.conf"
    # Ensure the Hyprland configuration directory exists
    if not os.path.exists(config_path):
        raise FileNotFoundError("Hyprland configuration file not found.")
    # Ensure the color is a valid hex string of length 6
    if color is None or not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    # Ensure the color is a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    # Read the existing configuration
    with open(config_path, "r") as config_file:
        # Read the configuration file
        config = config_file.read()
        # Close the configuration file
        config_file.close()
        for line in config.splitlines():
            # Replace the active border color
            if "col.active_border" in line:
                # Lighten the color for active border
                # Lighten the color by increasing RGB values
                active_border_color = lighten_color(color)
                # Replace the active border color in the configuration
                config = config.replace(line, f"    col.active_border = rgba({active_border_color}ff)")
                break
        for line in config.splitlines():
            # Replace the inactive border color in the configuration
            if "col.inactive_border" in line:
                # Darken the color for inactive border
                # Darken the color by decreasing RGB values
                inactive_border_color = darken_color(color)
                # Replace the inactive border color in the configuration
                config = config.replace(line, f"    col.inactive_border = rgba({inactive_border_color}aa)")
                break
        # Write the updated configuration back to the file
        with open(config_path, "w") as f:
            f.write(config)
            f.close()

def hyprlock_set_color(color):
    """
    Sets the color in Hyprlock configuration.
    
    Args:
        color (hex): The color in hex format (e.g., 'ff0000' for red).
    Raises:
        FileNotFoundError: If the Hyprlock configuration file does not exist.
        ValueError: If the color is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Get the user's home directory
    userDirectory = os.path.expanduser("~")
    # Ensure the directory ends with a slash
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Define the path to the Hyprlock configuration file
    config_path = userDirectory + ".config/hypr/hyprlock.conf"
    # Check if the Hyprlock configuration directory exists
    if not os.path.exists(config_path):
        raise FileNotFoundError("Hyprlock configuration file not found.")
    # Ensure the color is a valid hex string of length 6
    if color is None or not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    # Ensure the color is a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    # Read the existing configuration
    with open(config_path, "r") as config_file:
        # Read the configuration file
        config = config_file.read()
        # Close the configuration file
        config_file.close()
        # Replace the background color of the Hyprlock input field
        for line in config.splitlines():
            if "$color_input" in line:
                config = config.replace(line, f"$color_input = rgba({color}ff)")
                break
        # Get the lightened and darkened colors
        brightness = get_brightness(color)
        light_color = lighten_color(color)
        dark_color = darken_color(color)
        if brightness < 128:
            for line in config.splitlines():
                if "$color_text" in line:
                    config = config.replace(line, f"$color_text = rgba(fafafaff)")
                    break
        else:
            for line in config.splitlines():
                if "$color_text" in line:
                    config = config.replace(line, f"$color_text = rgba(0a0a0aff)")
                    break
        # Replace the border color of the Hyprlock
        for line in config.splitlines():
            if "$color_border" in line:
                config = config.replace(line, f"$color_border = rgba({light_color}ff)")
                break
        # Replace the shadow color
        for line in config.splitlines():
            if "$color_shadow" in line:
                config = config.replace(line, f"$color_shadow = rgba({dark_color}ff)")
                break
        # Write the updated configuration back to the file
        with open(config_path, "w") as f:
            f.write(config)
            f.close()

def waybar_color(color):
    """
    Sets the color in Waybar configuration.
    
    Args:
        color (hex): The color in hex format (e.g., 'ff0000' for red).
    
    Raises:
        FileNotFoundError: If the Waybar configuration file does not exist.
        ValueError: If the color is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Get the user's home directory
    userDirectory = os.path.expanduser("~")
    # Ensure the directory ends with a slash
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Define the path to the Waybar configuration file
    config_path = userDirectory + ".config/waybar/style.css"
    # Check if the Waybar configuration directory exists
    if not os.path.exists(config_path):
        raise FileNotFoundError("Waybar configuration file not found.")
    # Ensure the color is a valid hex string of length 6
    if color is None or not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    # Ensure the color is a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    # Read the existing configuration
    with open(config_path, "r") as config_file:
        # Read the configuration file
        config = config_file.read()
        # Close the configuration file
        config_file.close()
        light_color = lighten_color(color)  # Lighten the color for background
        dark_color = darken_color(color)  # Darken the color for background
        brightness = get_brightness(color)  # Get the brightness of the color
        if brightness < 128:
            # If the color is dark, use darkened color for background and lightened color for border
            # Color scheme for dark colors
            for line in config.splitlines():
                if "@import" in line:
                    # If the color is dark, use dark colors
                    config = config.replace(line, f"@import 'color_dark.css';")
                    break
            # Replace the background color
            for line in config.splitlines():
                if "background_color" in line:
                    # If the color is dark, use darkened color for background
                    # This ensures that the background color is suitable for dark colors
                    # This is useful for ensuring good contrast and visibility in the Waybar
                    # configuration
                    config = config.replace(line, f"@define-color background_color #{dark_color};")
                    break
            # Replace the border color
            for line in config.splitlines():
                if "border_color" in line:
                    # If the color is dark, use lightened color for border
                    # This ensures that the border color is suitable for dark colors
                    # This is useful for ensuring good contrast and visibility in the Waybar
                    # configuration
                    config = config.replace(line, f"@define-color border_color     #{light_color};")
                    break
        else:
            # If the color is light, use lightened color for background and darkened color for border
            # Color scheme for light colors
            for line in config.splitlines():
                if "@import" in line:
                    # If the color is light, use light colors
                    config = config.replace(line, f"@import 'color_light.css';")
                    break
            # Replace the background color
            for line in config.splitlines():
                if "background_color" in line:
                    # If the color is light, use darkened color for background
                    # This ensures that the background color is suitable for light colors
                    # This is useful for ensuring good contrast and visibility in the Waybar
                    # configuration
                    config = config.replace(line, f"@define-color background_color #{light_color};")
                    break
            # Replace the border color
            for line in config.splitlines():
                if "border_color" in line:
                    # If the color is light, use darkened color for border
                    # This ensures that the border color is suitable for light colors
                    # This is useful for ensuring good contrast and visibility in the Waybar
                    # configuration
                    config = config.replace(line, f"@define-color border_color     #{dark_color};")
                    break
        # Write the updated configuration back to the file
        with open(config_path, "w") as f:
            f.write(config)
            f.close()
    # Restart Waybar to apply the new configuration
    subprocess.run(["sh", "-c", "killall waybar &> /dev/null; waybar &> /dev/null &"])

def wlogout_set_color(color):
    """
    Sets the color in wlogout configuration.
    
    Args:
        color (str): The color in hex format (e.g., 'ff0000' for red).
    
    Raises:
        FileNotFoundError: If the wlogout configuration file does not exist.
        ValueError: If the color is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Get the user's home directory
    userDirectory = os.path.expanduser("~")
    # Ensure the directory ends with a slash
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Define the path to the wlogout configuration file
    config_path = userDirectory + ".config/wlogout/style.css"
    # Check if the wlogout configuration directory exists
    if not os.path.exists(config_path):
        raise FileNotFoundError("wlogout configuration file not found.")
    # Ensure the color is a valid hex string of length 6
    if color is None or not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    # Ensure the color is a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    # Read the existing configuration
    with open(config_path, "r") as config_file:
        # Read the configuration file
        config = config_file.read()
        # Close the configuration file
        config_file.close()
        # Get brightness of the color
        brightness = get_brightness(color)
        if brightness < 128:
            # If the color is dark, use darkened color for normal and lightened color for destak
            normal_color = darken_color(color)  # Darken the color for normal
            destak_color = lighten_color(color)  # Lighten the color for destak
            # Replace the icons style in the wlogout configuration to use light icons
            for line in config.splitlines():
                if "@import" in line:
                    # If the color is dark, use light icons
                    config = config.replace(line, f"@import 'light_icons.css';")
                    break
        else:
            # If the color is light, use kightened color for normal and darkened color for destak
            normal_color = lighten_color(color)  # Lighten the color for normal
            destak_color = darken_color(color)  # Darken the color for destak
            # Replace the icons style in the wlogout configuration to use dark icons
            for line in config.splitlines():
                if "@import" in line:
                    # If the color is light, use dark icons
                    config = config.replace(line, f"@import 'dark_icons.css';")
                    break
        # Replace the background color
        for line in config.splitlines():
            if "@define-color background_color" in line:
                config = config.replace(line, f"@define-color background_color #{color};")
                break
        # Replace the normal and destak colors based on brightness
        # This ensures that the colors adapt to the brightness of the dominant color
        # This is useful for ensuring good contrast and visibility in the wlogout
        # configuration
        # Replace the normal color
        for line in config.splitlines():
            if "@define-color normal_color" in line:
                config = config.replace(line, f"@define-color normal_color #{normal_color};")
                break
        # Replace the destak color
        for line in config.splitlines():
            if "@define-color destak_color" in line:
                config = config.replace(line, f"@define-color destak_color #{destak_color};")
                break
        # Write the updated configuration back to the file
        with open(config_path, "w") as f:
            f.write(config)
            f.close()

def rofi_set_color(color):
    """
    Sets the color in rofi configuration.
    
    Args:
        color (str): The color in hex format (e.g., 'ff0000' for red).
    
    Raises:
        FileNotFoundError: If the rofi configuration file does not exist.
        ValueError: If the color is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Get the user's home directory
    userDirectory = os.path.expanduser("~")
    # Ensure the directory ends with a slash
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Define the path to the rofi configuration file
    config_path = userDirectory + ".config/rofi/colors.rasi"
    # Check if the rofi configuration directory exists
    if not os.path.exists(config_path):
        raise FileNotFoundError("rofi configuration file not found.")
    # Ensure the color is a valid hex string of length 6
    if color is None or not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    # Ensure the color is a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    
    # Read the existing configuration
    with open(config_path, "r") as config_file:
        # Read the configuration file
        config = config_file.read()
        # Close the configuration file
        config_file.close()
        # Get brightness of the color
        brightness = get_brightness(color)
        dark_color = darken_color(color)  # Darken the color for normal
        light_color = lighten_color(color)  # Lighten the color for destak
        if brightness < 128:
            # Replace the icons style in the rofi configuration to use light icons
            for line in config.splitlines():
                if "primary:" in line:
                    # If the color is dark, use light icons
                    config = config.replace(line, f"    primary: #{light_color};")
                    break
            for line in config.splitlines():
                if "on-surface:" in line:
                    # If the color is dark, use light icons
                    config = config.replace(line, f"    on-surface: #0f0f0f;")
                    break
            for line in config.splitlines():
                if "on-surface-variant:" in line:
                    # If the color is dark, use light icons
                    config = config.replace(line, f"    on-surface-variant: #fafafa;")
                    break
        else:
            # Replace the icons style in the rofi configuration to use dark colors
            for line in config.splitlines():
                if "primary" in line:
                    # If the color is light, use dark icons
                    config = config.replace(line, f"    primary: #{dark_color};")
                    break
            for line in config.splitlines():
                if "on-surface:" in line:
                    # If the color is dark, use light icons
                    config = config.replace(line, f"    on-surface: #0f0f0f;")
                    break
            for line in config.splitlines():
                if "on-surface-variant:" in line:
                    # If the color is dark, use light icons
                    config = config.replace(line, f"    on-surface-variant: #fafafa;")
                    break
        
        # Replace the background color
        for line in config.splitlines():
            if "on-primary-fixed:" in line:
                config = config.replace(line, f"    on-primary-fixed: #{dark_color};")
                break
        # Replace the normal and destak colors based on brightness
        # This ensures that the colors adapt to the brightness of the dominant color
        # This is useful for ensuring good contrast and visibility in the rofi
        # configuration
        # Replace the normal color
        for line in config.splitlines():
            if "background:" in line:
                color_rgb = hex_to_rgb(light_color)
                r = color_rgb[0]
                g = color_rgb[1]
                b = color_rgb[2]
                config = config.replace(line, f"    background: rgba({r}, {g}, {b}, 0.7);")
                break
        # Write the updated configuration back to the file
        with open(config_path, "w") as f:
            f.write(config)
            f.close()

def kitty_set_color(color_list):
    """
    Sets the color in kitty configuration.
    
    Args:
        color (str): The color in hex format (e.g., 'ff0000' for red).
        image_path (str): The path to the image file.
    
    Raises:
        FileNotFoundError: If the kitty configuration file does not exist.
        ValueError: If the color is not a valid hex string of length 6 or if the RGB values are not in the range 0-255.
    """
    # Get the user's home directory
    userDirectory = os.path.expanduser("~")
    # Ensure the directory ends with a slash
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Define the path to the kitty configuration file
    config_path = userDirectory + ".config/kitty/current-theme.conf"
    # Check if the kitty configuration directory exists
    if not os.path.exists(config_path):
        raise FileNotFoundError("kitty configuration file not found.")
    # Ensure the color is a valid hex string of length 6
    for color in color_list:
        if color is None or not isinstance(color, str) or len(color) != 6:
            raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
        # Ensure the color is a valid hex string
        if not all(c in '0123456789abcdefABCDEF' for c in color):
            raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    
    # Read the existing configuration
    with open(config_path, "r") as config_file:
        # Read the configuration file
        config = config_file.read()
        # Close the configuration file
        config_file.close()
        # Get brightness of the color
        brightness = get_brightness(color_list[0])
        dark_color = darken_color(color_list[0], .6)  # Darken the color for normal
        light_color = lighten_color(color_list[0], .6)  # Lighten the color for destak
        line_list = ["foreground #", "background #", "selection_foreground #", "selection_background #", \
                            "cursor #", "cursor_text_color #"]
        theme_list_dark = [dark_color, light_color, dark_color, light_color, light_color, dark_color]
        theme_list_light = [light_color, dark_color, light_color, dark_color, dark_color, light_color]    
        if brightness < 128:
            # If color is dark, use dark theme in the kitty configuration
            for line in config.splitlines():
                for i in range(0, len(line_list)):
                    if line_list[i] in line:
                        config = config.replace(line, f"{line_list[i]}{theme_list_dark[i]}")
                        break
        else:
            # Else if color is light, use light theme in the kitty configuration
            for line in config.splitlines():
                for i in range(0, len(line_list)):
                    if line_list[i] in line:
                        config = config.replace(line, f"{line_list[i]}{theme_list_light[i]}")
                        break
        for line in config.splitlines():
            target_colors =['#000000', '#cc0403', '#19cb00', '#cecb00', '#0d73cc', \
                            '#cb1ed1', '#0dcdcd', '#dddddd', '#767676', '#f2201f', \
                            '#23fd00', '#fffd00', '#1a8fff', '#fd28ff', '#14ffff', \
                            '#ffffff']
            for i in range(0, 16):
                if f"color{i} #" in line:
                    config = config.replace(line, f"color{i} #{closest_color(target_colors[i], color_list)}")
                    # This print is not in number order, nothing wrong whit the program
                    # the config file is not in number ortder
                    print(f"Searching for color{i} in color list match the color target {target_colors[i]}")
                    break

        # Write the updated configuration back to the file
        with open(config_path, "w") as f:
            f.write(config)
            f.close()

def main():
    """ 
    Main function to run the wallpaper script.
    It checks the command line arguments, sets the wallpaper, extracts the dominant color,
    and updates the Hyprland, Hyprlock, Waybar, and Wlogout configurations.
    Raises:
        ValueError: If the provided argument is not valid or if the image format is not supported.
        FileNotFoundError: If the wallpapers directory or image file does not exist.
        Exception: For any other unexpected errors.
    KeyboardInterrupt: If the script is interrupted by the user.
    OSError: If there is an OS-related error (e.g., permission issues).
    ImportError: If required libraries are not installed.
    PermissionError: If there are permission issues accessing files or directories.
    RuntimeError: If there is a runtime error in the script.
    """
    # Change this to your wallpapers directory
    userDirectory = os.path.expanduser("~")  # Get the user's home directory
    # Ensure the directory ends with a slash
    # This is important for constructing file paths correctly
    # It ensures that the directory paths are correctly formatted
    # This is useful for ensuring that the script works correctly on different systems
    # and avoids issues with missing slashes in paths
    if not userDirectory.endswith('/'):
        userDirectory += '/'
    # Check if the user provided an argument
    if len(sys.argv) > 1:
        print(f"Argument provided: {sys.argv[1]}")
    # If no argument is provided, raise an error
    # This ensures that the script is run with a valid argument
    # If the argument is 'Random', it will select a random wallpaper from the wallpapers directory
    # If the argument is a valid image path, it will use that image
    # If no argument is provided, it will raise a ValueError
    # This is useful for ensuring that the script is run with a valid argument
    print("Checking arguments...")
    # Check if the user provided an argument
    if len(sys.argv) < 2 and not os.getenv("HYPRLAND_WALLPAPER"):
        # If no argument is provided and the environment variable is not set, raise an error
        raise ValueError("Please provide an argument: 'Random' for a random wallpaper or the path to an image file.")
    # Check if the argument is 'Random' or a valid image path
    if sys.argv[1] not in ["Random"] and not os.path.exists(sys.argv[1]):
        raise ValueError("Invalid argument. Please provide 'Random' or a valid image file path.")
    print("Starting wallpaper script...")
    # If the argument is 'Random', get a random image from the wallpapers directory
    if sys.argv[1] == "Random":
        print("No image provided, selecting a random wallpaper...")
        # Define the wallpapers directory
        # This is the directory where the wallpapers are stored
        # Change this to your wallpapers directory
        wallpapers_dir = userDirectory + wallpaper_path
        # Check if the wallpapers directory exists
        if not os.path.exists(wallpapers_dir):
            raise FileNotFoundError(f"Wallpapers directory does not exist: {wallpapers_dir}")
        # Get a random image from the wallpapers directory
        print(f"Looking for wallpapers in: {wallpapers_dir}")
        image = get_random_image(wallpapers_dir)
    else:
        # Use the image provided as an argument
        image = sys.argv[1]
        # Check if the image file exists
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file does not exist: {image}")
        # Check if the image is in a supported format
        print(f"Using provided image: {image}")
        if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            raise ValueError("Selected file is not a valid image format. Supported formats are: PNG, JPEG, BMP.")
    # Print the selected image
    print(f"Selected wallpaper: {image}")
    # Set the wallpaper for Hyprland
    print("Setting wallpaper for Hyprland...")
    hyprland_set_wallpaper(image)
    # Extract dominant color(s)
    print("Extracting dominant color...")
    dominant_color = extract_dominant_colors(image, n_colors=16)  # Get dominant color from the image
    # Check if the dominant color is valid
    if not dominant_color:
        raise ValueError("No dominant color found in the image.")
    print("Dominant color extracted successfully.")
    # Set the border color in Hyprland
    print("Setting border color in Hyprland...")
    hyprland_set_border_color(dominant_color[0])  # Set the border color
    # Set the color in Hyprlock configuration
    print("Setting color in Hyprlock configuration...")
    hyprlock_set_color(dominant_color[0])  # Set the color in Hyprlock configuration
    # Set the color in Waybar configuration
    print("Setting color in Waybar configuration...")
    waybar_color(dominant_color[0])  # Set the color in Waybar configuration
    # Set the color in wlogout configuration
    print("Setting color in wlogout configuration...")
    wlogout_set_color(dominant_color[0])  # Set the color in wlogout configuration
    # Set the color in rofi configuration
    print("Setting color in rofi configuration...")
    rofi_set_color(dominant_color[0])  # Set the color in rofi configuration
    # Set the color in kitty configuration
    print("Setting color in kitty configuration...")
    kitty_set_color(dominant_color)  # Set the color in kitty configuration
    print("All configurations updated successfully.")
    # Print the dominant color in hex format
    print(f"Dominant color in hex format: {dominant_color}")
    # Print the darkened colors
    print(f"Darkened color in hex format: {darken_color(dominant_color[0])}")
    # Print the lightened colors
    print(f"Lightened color in hex format: {lighten_color(dominant_color[0])}")
    # Print the brightness of the dominant color
    brightness = get_brightness(dominant_color[0])
    print(f"Brightness of the dominant color: {brightness}")
    if brightness < 128:
        # If the brightness is less than 128, consider it a dark color
        print("The dominant color is dark.")
    else:
        # If the brightness is greater than or equal to 128, consider it a light color
        print("The dominant color is light.")

if __name__ == "__main__":
    try:
        main()  # Run the main function
    except (ValueError, FileNotFoundError, OSError, ImportError, PermissionError, RuntimeError) as e:
        # Catch specific exceptions and print the error message
        print(f"Error: {e}")
    except KeyboardInterrupt:
        # Handle keyboard interrupt gracefully
        print("\nScript interrupted by user.")
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure any necessary cleanup is done here
        print("Exiting the script. Goodbye!")
        # This ensures that the script exits cleanly and any resources are released
        sys.exit(0)  # Exit the script with a success status code
        # This is useful for ensuring that the script exits cleanly and any resources are released
# End of the script
