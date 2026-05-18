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
import re
import json
import hashlib
from typing import Optional, Tuple, List, Dict
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
import math

RESOLUTION: Tuple[int, int] = (1920, 1080)
WALLPAPER_PATH = "Imagens/wallpapers"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "wallpaper_script")
CACHE_FILE = os.path.join(CACHE_DIR, "colors.json")
testing_config_path = "../../"

kitty_modes = ["Default", "Precise", "Random", "Monochrome", "Complementary"]

def save_config(config_path: str) -> None:
    subprocess.run(["cp", config_path, config_path+".bak"], check=True)

def diff_configs(config_path: str) -> None:
    with open(config_path, "r") as f:
        config = f.read()
    with open(config_path+".bak", "r") as f:
        config_bak = f.read()
    
    if config != config_bak:
        print(f"\nConfiguration file {config_path.split('/')[-1]} updated:")
        for line, line_bak in zip(config.splitlines(), config_bak.splitlines()):
            if line != line_bak:
                print(f"  - {line.strip()} (was: {line_bak.strip()})")
    else:
        print(f"\nNo changes detected in the configuration file {config_path.split('/')[-1]}.")


def get_config_dir() -> str:
    home = os.path.expanduser("~")
    return os.path.join(home, ".config")


def validate_hex_color(color: str) -> None:
    if not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")


def restart_service(service_name: str) -> None:
    """Restart a service gracefully."""
    subprocess.run(
        ["sh", "-c", f"killall {service_name} &> /dev/null; {service_name} &> /dev/null &"],
        capture_output=True,
    )


def get_image_hash(image_path: str) -> str:
    """Generate SHA256 hash of image file for caching."""
    sha256_hash = hashlib.sha256()
    with open(image_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_cached_dominant_colors(image_path: str, n_colors: int = 16) -> List[str]:
    """Get dominant colors from cache or extract them from image."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    image_hash = get_image_hash(image_path)
    cache_key = f"{image_hash}_{n_colors}"
    
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
                if cache_key in cache:
                    return cache[cache_key]
        except (json.JSONDecodeError, IOError):
            pass
    
    colors = extract_dominant_colors(image_path, n_colors)
    
    try:
        cache = {}
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
        cache[cache_key] = colors
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except (IOError, OSError):
        pass
    
    return colors


def update_config_file(config_path: str, updates: Dict[str, str], restart_svc: Optional[str] = None) -> None:
    """Generic function to update config file with multiple regex substitutions.
    
    Args:
        config_path: Path to the config file
        updates: Dictionary of regex patterns and replacements
        restart_svc: Optional service name to restart after update
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, "r") as f:
        config = f.read()
    
    for pattern, replacement in updates.items():
        config = re.sub(pattern, replacement, config)
    
    with open(config_path, "w") as f:
        f.write(config)
    
    if restart_svc:
        restart_service(restart_svc)

def extract_dominant_colors(image_path: str, n_colors: int = 1) -> List[str]:
    """
    Extracts the dominant color(s) from an image using K-Means clustering.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if n_colors < 1:
        raise ValueError("Number of colors must be at least 1.")

    img = Image.open(image_path)
    if img.format not in ['PNG', 'JPEG', 'BMP']:
        raise ValueError(f"Unsupported image format: {img.format}. Supported formats are: PNG, JPEG, BMP.")
    if img.mode not in ['RGB', 'RGBA']:
        raise ValueError(f"Unsupported image mode: {img.mode}. Supported modes are: RGB, RGBA.")

    if img.mode != 'RGB':
        print(f"Converting image {image_path} to RGB mode.")
        img = img.convert("RGB")

    img = img.resize((100, 100), Image.Resampling.LANCZOS)
    pixels = np.array(img)
    pixels = pixels.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init='auto')
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    colors = [tuple(max(0, min(255, c)) for c in color) for color in dominant_colors]

    hex_colors = [f"{color[0]:02x}{color[1]:02x}{color[2]:02x}".lower() for color in colors]

    for hex_color in hex_colors:
        if not isinstance(hex_color, str) or len(hex_color) != 6:
            raise ValueError("Extracted color must be a hex string of length 6 (e.g., 'ff0000' for red).")
        if not all(c in '0123456789abcdefABCDEF' for c in hex_color):
            raise ValueError("Extracted color must be a valid hex string (e.g., 'ff0000' for red).")
    return hex_colors

def extract_primary_colors(image_path):
    """
    Extracts primary colors from an image.
    """
    # Extract the dominant color from the image
    return extract_dominant_colors(image_path, n_colors=16)


def darken_color(color: str, factor: float = 0.2) -> str:
    """Darkens a color by a specified factor."""
    if not (0 <= factor <= 1):
        raise ValueError("Factor must be between 0.0 and 1.0.")
    r, g, b = hex_to_rgb(color)
    r, g, b = (int(r * (1 - factor)), int(g * (1 - factor)), int(b * (1 - factor)))
    r, g, b = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    return rgb_to_hex((r, g, b))

def lighten_color(color: str, factor: float = 0.2) -> str:
    """Lightens a color by a specified factor."""
    if not (0 <= factor <= 1):
        raise ValueError("Factor must be between 0.0 and 1.0.")
    r, g, b = hex_to_rgb(color)
    r, g, b = (int(r + (255 - r) * factor), int(g + (255 - g) * factor), int(b + (255 - b) * factor))
    r, g, b = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    return rgb_to_hex((r, g, b))

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Converts a hex color string to an RGB tuple."""
    if not isinstance(hex_color, str) or len(hex_color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    if not all(c in '0123456789abcdefABCDEF' for c in hex_color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (r, g, b)

def rgb_to_hex(rgb_color: Tuple[int, int, int]) -> str:
    """Converts an RGB tuple to a hex color string."""
    if not isinstance(rgb_color, tuple) or len(rgb_color) != 3:
        raise ValueError("Input must be a tuple of three integers representing RGB values.")
    if not all(isinstance(c, int) for c in rgb_color):
        raise ValueError("All components of the RGB tuple must be integers.")
    if any(c < 0 or c > 255 for c in rgb_color):
        raise ValueError("RGB values must be in the range 0-255.")
    r, g, b = (max(0, min(255, c)) for c in rgb_color)
    return ''.join(f'{c:02x}' for c in (r, g, b)).lower()

def color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Calculates the Euclidean distance between two RGB colors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def closest_color(target_hex: str, color_list: List[str]) -> Optional[str]:
    """Finds the closest color from a list of colors to a target color."""
    target_hex = target_hex.lstrip('#')
    target_rgb = hex_to_rgb(target_hex)
    min_distance = float('inf')
    closest: Optional[str] = None
    for color in color_list:
        color_rgb = hex_to_rgb(color)
        dist = color_distance(target_rgb, color_rgb)
        if dist < min_distance:
            min_distance = dist
            closest = color
    return closest


def get_brightness(color: str) -> float:
    """Calculates the brightness of a color in hex format."""
    validate_hex_color(color)
    color_rgb = hex_to_rgb(color)
    return (color_rgb[0] * 0.299) + (color_rgb[1] * 0.587) + (color_rgb[2] * 0.114)

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

def hyprland_set_wallpaper(image_path: str) -> None:
    """Sets the wallpaper for Hyprland desktop environment."""
    config_base = get_config_dir()
    if not os.path.exists(os.path.join(config_base, "hypr")):
        raise FileNotFoundError("Hyprland configuration directory not found.")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    if not isinstance(RESOLUTION, tuple) or len(RESOLUTION) != 2:
        raise ValueError("Resolution must be a tuple of (width, height).")
    if not all(isinstance(dim, int) for dim in RESOLUTION):
        raise ValueError("Resolution dimensions must be integers.")
    if RESOLUTION[0] <= 0 or RESOLUTION[1] <= 0:
        raise ValueError("Resolution dimensions must be positive integers.")
    
    supported_formats = ['PNG', 'JPEG', 'BMP']
    img_format = Image.open(image_path).format
    if img_format not in supported_formats:
        raise ValueError(f"Unsupported image format: {img_format}. Supported formats are: {', '.join(supported_formats)}.")
    
    img = Image.open(image_path)
    if img.size == RESOLUTION:
        print("Image is already in the desired resolution. No resizing needed.")
        img_resized = img
    else:
        print(f"Resizing image from {img.size} to {RESOLUTION}.")
        img_resized = img.resize(RESOLUTION, Image.Resampling.LANCZOS)
    
    if not img_resized.mode == 'RGB':
        print("Converting image to RGB mode.")
        img_resized = img_resized.convert('RGB')
    
    wallpaper_file = os.path.join(config_base, "hypr", "wallpaper.png")
    img_resized.save(wallpaper_file, format='PNG')
    restart_service("hyprpaper")

def hyprland_set_border_color(color: str) -> None:
    """Sets the border color in Hyprland configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "hypr", "modules", "decorator.lua")
    save_config(config_path)
    
    active_border_color = lighten_color(color)
    active_border_color1 = color
    inactive_border_color = darken_color(color)
    
    updates = {
        r"(?m)^\s*active_border\s*=.*$": (
            f"            active_border   = {{ colors = {{\"rgba({active_border_color}ee)\", "
            f"\"rgba({active_border_color1}ee)\"}}, angle = 45 }},"
        ),
        r"(?m)^\s*inactive_border\s*=.*$": f"            inactive_border = \"rgba({inactive_border_color}aa)\",",
    }
    update_config_file(config_path, updates)
    diff_configs(config_path)

def hyprlock_set_color(color: str) -> None:
    """Sets the color in Hyprlock configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "hypr", "hyprlock.conf")
    save_config(config_path)

    with open(config_path, "r") as f:
        current_config = f.read()

    brightness = get_brightness(color)
    light_color = lighten_color(color,.8)
    dark_color = darken_color(color,.5)
    text_color = "fafafaff" if brightness < 128 else "0a0a0aff"

    # Support both hyprlock variable schemas used in this repo.
    if "$color_input" in current_config:
        updates = {
            r"\$color_input\s*=.*": f"$color_input = rgba({color}ff)",
            r"\$color_text\s*=.*": f"$color_text = rgba({text_color})",
            r"\$color_border\s*=.*": f"$color_border = rgba({light_color}ff)",
            r"\$color_shadow\s*=.*": f"$color_shadow = rgba({dark_color}ff)",
        }
    else:
        if brightness < 128:
            normal_color = dark_color
            destak_color = light_color
        else:
            normal_color = light_color
            destak_color = dark_color

        updates = {
            r"\$color_normal\s*=.*": f"$color_normal = rgba({normal_color}ff)",
            r"\$color_destak\s*=.*": f"$color_destak = rgba({destak_color}ff)",
        }

    update_config_file(config_path, updates)
    diff_configs(config_path)


def waybar_color(color: str) -> None:
    """Sets the color in Waybar configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "waybar", "style.css")
    save_config(config_path)
    
    light_color = lighten_color(color)
    dark_color = darken_color(color)
    brightness = get_brightness(color)
    
    if brightness < 128:
        import_line = "@import 'color_dark.css';"
        bg_color = dark_color
        border_color = light_color
    else:
        import_line = "@import 'color_light.css';"
        bg_color = light_color
        border_color = dark_color
    
    updates = {
        r"@import.*": import_line,
        r"@define-color background_color.*": f"@define-color background_color #{bg_color};",
        r"@define-color border_color.*": f"@define-color border_color     #{border_color};",
    }
    update_config_file(config_path, updates, restart_svc="waybar")
    diff_configs(config_path)

def wlogout_set_color(color: str) -> None:
    """Sets the color in wlogout configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "wlogout", "style.css")
    save_config(config_path)
    
    brightness = get_brightness(color)
    if brightness < 128:
        import_line = "@import 'light_icons.css';"
        normal_color = darken_color(color)
        destak_color = lighten_color(color)
    else:
        import_line = "@import 'dark_icons.css';"
        normal_color = lighten_color(color)
        destak_color = darken_color(color)
    
    updates = {
        r"@import.*": import_line,
        r"@define-color background_color.*": f"@define-color background_color #{color};",
        r"@define-color normal_color.*": f"@define-color normal_color #{normal_color};",
        r"@define-color destak_color.*": f"@define-color destak_color #{destak_color};",
    }
    update_config_file(config_path, updates)
    diff_configs(config_path)


def rofi_set_color(color: str) -> None:
    """Sets the color in rofi configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "rofi", "colors.rasi")
    save_config(config_path)
    
    brightness = get_brightness(color)
    dark_color = darken_color(color)
    light_color = lighten_color(color)
    
    primary = light_color if brightness < 128 else dark_color
    text_color_select = "fafafa" if brightness < 128 else "0a0a0a"
    color_rgb = hex_to_rgb(light_color)
    bg_rgba = f"rgba({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]}, 0.7)"
    
    updates = {
        r"(?m)^\s*primary:\s*#[0-9a-fA-F]{6};\s*$": f"    primary: #{primary};",
        r"(?m)^\s*on-surface:\s*#[0-9a-fA-F]{6};\s*$": "    on-surface: #0f0f0f;",
        r"(?m)^\s*on-surface-variant:\s*#[0-9a-fA-F]{6};\s*$": "    on-surface-variant: #fafafa;",
        r"(?m)^\s*on-primary-fixed:\s*#[0-9a-fA-F]{6};\s*$": f"    on-primary-fixed: #{dark_color};",
        r"(?m)^\s*background:\s*rgba\([^)]+\);\s*$": f"    background: {bg_rgba};",
        r"(?m)^\s*text-color-select:\s*#[0-9a-fA-F]{6};\s*$": f"    text-color-select: #{text_color_select};",
    }
    update_config_file(config_path, updates)
    diff_configs(config_path)


def kitty_set_color(color_list: List[str], mode: str = "Default") -> None:
    """Sets the color in kitty configuration."""
    if mode not in kitty_modes:
        raise ValueError(f"Invalid mode. Supported modes are: {', '.join(kitty_modes)}.")
    config_path = os.path.join(get_config_dir(), "kitty", "theme.conf")
    save_config(config_path)
    
    for color in color_list:
        validate_hex_color(color)
    
    with open(config_path, "r") as f:
        config = f.read()
    
    brightness = get_brightness(color_list[0])
    dark_color = darken_color(color_list[0], .6)
    light_color = lighten_color(color_list[0], .6)

    if mode == "Default":
        theme_values = {
            "foreground": "a3a3a3",
            "background": "0a0a0a",
            "selection_foreground": "0a0a0a",
            "selection_background": "a3a3a3",
            "cursor": "a3a3a3",
            "cursor_text_color": "0a0a0a",
            "url_color": "0dcdcd",
        }
    else:
        theme_values = {
            "foreground": dark_color if brightness >= 128 else light_color,
            "background": light_color if brightness >= 128 else dark_color,
            "selection_foreground": light_color if brightness >= 128 else dark_color,
            "selection_background": dark_color if brightness >= 128 else light_color,
            "cursor": dark_color if brightness >= 128 else light_color,
            "cursor_text_color": light_color if brightness >= 128 else dark_color,
            "url_color": light_color if brightness >= 128 else dark_color,
        }

    # Use whitespace-tolerant replacements so themes with different spacing still update correctly.
    for key in ["foreground", "background", "cursor", "cursor_text_color", "url_color"]:
        config = re.sub(
            rf"(?m)^\s*{key}\s+#[0-9a-fA-F]{{6}}\s*$",
            f"{key} #{theme_values[key]}",
            config,
        )

    selection_background_pattern = r"(?m)^\s*selection_background\s+#[0-9a-fA-F]{6}\s*$"
    if re.search(selection_background_pattern, config):
        config = re.sub(
            selection_background_pattern,
            f"selection_background #{theme_values['selection_background']}",
            config,
        )
    else:
        config += f"\nselection_background #{theme_values['selection_background']}\n"

    selection_foreground_pattern = r"(?m)^\s*selection_foreground\s+#[0-9a-fA-F]{6}\s*$"
    if re.search(selection_foreground_pattern, config):
        config = re.sub(
            selection_foreground_pattern,
            f"selection_foreground #{theme_values['selection_foreground']}",
            config,
        )
    else:
        config = re.sub(
            selection_background_pattern,
            lambda m: f"{m.group(0)}\nselection_foreground #{theme_values['selection_foreground']}",
            config,
            count=1,
        )

    # kitty_modes = ["Default", "Precise", "Random", "Monochrome", "Complementary"]

    
    target_colors = ['#000000', '#cc0403', '#19cb00', '#cecb00', '#0d73cc', '#cb1ed1', '#0dcdcd', '#dddddd',
                     '#767676', '#f2201f', '#23fd00', '#fffd00', '#1a8fff', '#fd28ff', '#14ffff', '#ffffff']
    if mode == "Default":
        for i in range(16):
            config = re.sub(f"color{i} #.*", f"color{i} {target_colors[i]}", config)
    elif mode == "Precise":
        for i, target in enumerate(target_colors):
            match = closest_color(target, color_list)
            if match:
                config = re.sub(f"color{i} #.*", f"color{i} #{match}", config)
    elif mode == "Random":
        for i in range(16):
            random_color = random.choice(color_list)
            config = re.sub(f"color{i} #.*", f"color{i} #{random_color}", config)
    elif mode == "Monochrome":
        for i in range(16):
            config = re.sub(f"color{i} #.*", f"color{i} #{color_list[0]}", config)
    elif mode == "Complementary":
        for c, i in zip(color_list, range(16)):
            r, g, b = hex_to_rgb(c)
            comp_r, comp_g, comp_b = (255 - r, 255 - g, 255 - b)
            complementary_color = rgb_to_hex((comp_r, comp_g, comp_b))
            config = re.sub(f"color{i} #.*", f"color{i} #{complementary_color}", config)
    
    with open(config_path, "w") as f:
        f.write(config)

    subprocess.run(["kitty", "@", "set-colors", config_path], check=True)

    diff_configs(config_path)

def main() -> None:
    """Main function to run the wallpaper script."""
    userDirectory = os.path.expanduser("~")

    if len(sys.argv) > 1:
        print(f"Argument provided: {sys.argv[1]}")

    random = False
    kitty_mode = "Default"
    image = None

    for arg in sys.argv[1:]:
        if arg == "Random":
            random = True
        elif arg in kitty_modes:
            kitty_mode = arg
        elif os.path.exists(arg):
            image = arg
        else:
            print(f"Invalid argument: {arg}")

    print("Starting wallpaper script...")
    if not image:
        print("No image provided, selecting a random wallpaper...")
        wallpapers_dir = os.path.join(userDirectory, WALLPAPER_PATH)
        if not os.path.exists(wallpapers_dir):
            raise FileNotFoundError(f"Wallpapers directory does not exist: {wallpapers_dir}")
        print(f"Looking for wallpapers in: {wallpapers_dir}")
        image = get_random_image(wallpapers_dir)
    else:
        image = image.strip('"')  # Remove quotes if the path is provided with them
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file does not exist: {image}")
        print(f"Using provided image: {image}")
        if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            raise ValueError("Selected file is not a valid image format. Supported formats are: PNG, JPEG, BMP.")

    print(f"Selected wallpaper: {image}")
    hyprland_set_wallpaper(image)

    dominant_color = get_cached_dominant_colors(image, n_colors=16)

    if not dominant_color:
        raise ValueError("No dominant color found in the image.")

    hyprland_set_border_color(dominant_color[0])
    hyprlock_set_color(dominant_color[0])
    waybar_color(dominant_color[0])
    wlogout_set_color(dominant_color[0])
    rofi_set_color(dominant_color[0])
    kitty_set_color(dominant_color, mode=kitty_mode)

    print("\nAll configurations updated successfully.")
    print(f"Primary color: {dominant_color[0]} (brightness: {get_brightness(dominant_color[0]):.0f})")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, OSError, ImportError, PermissionError, RuntimeError) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Exiting the script. Goodbye!")
        sys.exit(0)
