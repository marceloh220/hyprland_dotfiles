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
#       wallpaper.py
#   or:
#       wallpaper.py /path/to/your/image.png
#
# Kitty theme can be set by providing a second argument with the mode, e.g.:
#       wallpaper.py /path/to/your/image.png Precise
# The available modes for Kitty are: Default, Precise, Random, Monochrome, Complementary.
#   - Default: Uses a defined theme.
#   - Precise: Uses colors extracted from the image that closely match with default colors.
#   - Random: Uses a random color from the image in theme.
#   - Monochrome: Uses a monochrome version of the dominant color.
#   - Complementary: Uses the complementary color of colors extracted from the image.
#
# For more information run the script with the --help flag:
#       wallpaper.py --help
#
# Ensure you have the python packages installed, e.g.:
# pip install Pillow scikit-learn numpy
#
# Note: The script assumes you have Hyprland installed and configured correctly.
# It's works on my dotfiles =p
#
# Copyright 2025-2026 Marcelo H Moraes
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
import argparse
import re
import json
import hashlib
import shutil
import time
from typing import Optional, Tuple, List, Dict, Any, Callable
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
import math

WALLPAPER_PATH = "Imagens/wallpapers"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "wallpaper_script")
CACHE_FILE = os.path.join(CACHE_DIR, "colors.json")
testing_config_path = "../../"
VERBOSE = False
DEBUG = False

kitty_modes = ["Default", "Precise", "Random", "Monochrome", "Complementary"]


def vprint(message: str) -> None:
    """Print informational logs only when verbose mode is enabled."""
    if VERBOSE:
        print(message)


def debug_log(message: str) -> None:
    """Print debug logs only when DEBUG is enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}")


def run_debug_step(step_name: str, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Run a step and report elapsed time when debug mode is enabled."""
    if not DEBUG:
        return func(*args, **kwargs)

    start = time.perf_counter()
    debug_log(f"Starting: {step_name}")
    result = func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000
    debug_log(f"Finished: {step_name} in {elapsed_ms:.2f} ms")
    return result

def get_monitor_resolution() -> Tuple[int, int, int]:
    """Get the current monitor resolution using Hyprctl."""
    try:
        result = subprocess.run(["hyprctl", "monitors", "-j"], capture_output=True, text=True, check=True)
        monitors = json.loads(result.stdout)
        if not monitors:
            raise RuntimeError("No monitors found.")

        monitor = next((m for m in monitors if m.get("focused")), monitors[0])
        width = monitor.get("width")
        height = monitor.get("height")
        scale = monitor.get("scale", 1)

        if not isinstance(width, int) or not isinstance(height, int):
            raise RuntimeError("Monitor width/height not found in hyprctl output.")
        
        vprint(f"Detected monitor resolution: {width}x{height} (scale: {scale})")

        return width, height, scale
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to get monitor resolution: {e}")


def save_config(config_path: str) -> None:
    shutil.copy2(config_path, config_path + ".bak")


def diff_configs(config_path: str) -> None:
    with open(config_path, "r") as f:
        config = f.read()
    with open(config_path+".bak", "r") as f:
        config_bak = f.read()
    
    if config != config_bak:
        vprint(f"Configuration file {config_path.split('/')[-1]} updated:")
        for line, line_bak in zip(config.splitlines(), config_bak.splitlines()):
            if line != line_bak:
                vprint(f"  - {line.strip()} (was: {line_bak.strip()})")
    else:
        vprint(f"No changes detected in the configuration file {config_path.split('/')[-1]}.")


def get_config_dir() -> str:
    home = os.path.expanduser("~")
    return os.path.join(home, ".config")


def validate_hex_color(color: str) -> None:
    if not isinstance(color, str) or len(color) != 6:
        raise ValueError("Color must be a hex string of length 6 (e.g., 'ff0000' for red).")
    if not all(c in '0123456789abcdefABCDEF' for c in color):
        raise ValueError("Color must be a valid hex string (e.g., 'ff0000' for red).")


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
                    debug_log(f"Color cache hit for key: {cache_key}")
                    return cache[cache_key]
        except (json.JSONDecodeError, IOError):
            pass

    debug_log(f"Color cache miss for key: {cache_key}")
    
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


def update_config_file(config_path: str, updates: Dict[str, str]) -> bool:
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

    original_config = config
    
    for pattern, replacement in updates.items():
        config = re.sub(pattern, replacement, config)

    if config == original_config:
        return False

    save_config(config_path)
    with open(config_path, "w") as f:
        f.write(config)
    return True


def extract_dominant_colors(image_path: str, n_colors: int = 1) -> List[str]:
    """
    Extracts the dominant color(s) from an image using K-Means clustering.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if n_colors < 1:
        raise ValueError("Number of colors must be at least 1.")

    with Image.open(image_path) as img:
        if img.format not in ['PNG', 'JPEG', 'BMP']:
            raise ValueError(f"Unsupported image format: {img.format}. Supported formats are: PNG, JPEG, BMP.")
        if img.mode not in ['RGB', 'RGBA']:
            raise ValueError(f"Unsupported image mode: {img.mode}. Supported modes are: RGB, RGBA.")

        if img.mode != 'RGB':
            vprint(f"Converting image {image_path} to RGB mode.")
            img = img.convert("RGB")

        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        pixels = np.asarray(img, dtype=np.uint8).reshape(-1, 3)

    # Keep KMeans fast on very large datasets by sampling a capped number of pixels.
    max_samples = 5000
    if pixels.shape[0] > max_samples:
        idx = np.random.default_rng(42).choice(pixels.shape[0], size=max_samples, replace=False)
        pixels = pixels[idx]

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
    # List all image files in the directory using scandir (faster than listdir for metadata access)
    images = [entry.path for entry in os.scandir(directory) if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    # Ensure there are images in the directory
    if not images:
        raise FileNotFoundError("No images found in the directory.")
    # Select a random image from the list
    return random.choice(images)


def hyprland_set_wallpaper(image_path: str) -> None:
    """Sets the wallpaper for Hyprland desktop environment."""
    config_base = get_config_dir()
    if not os.path.exists(os.path.join(config_base, "hypr")):
        raise FileNotFoundError("Hyprland configuration directory not found.")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    resolution = get_monitor_resolution()
    resolution = (int(resolution[0] * resolution[2]), int(resolution[1] * resolution[2]))  # Apply scale factor
    
    if not isinstance(resolution, tuple) or len(resolution) != 2:
        raise ValueError("Resolution must be a tuple of (width, height).")
    if not all(isinstance(dim, int) for dim in resolution):
        raise ValueError("Resolution dimensions must be integers.")
    if resolution[0] <= 0 or resolution[1] <= 0:
        raise ValueError("Resolution dimensions must be positive integers.")
    
    supported_formats = ['PNG', 'JPEG', 'BMP']
    wallpaper_file = os.path.join(config_base, "hypr", "wallpaper.png")

    with Image.open(image_path) as img:
        if img.format not in supported_formats:
            raise ValueError(f"Unsupported image format: {img.format}. Supported formats are: {', '.join(supported_formats)}.")

        if img.size == resolution:
            vprint("Image is already in the desired resolution. No resizing needed.")
            img_resized = img.copy()
        else:
            vprint(f"Resizing image from {img.size} to {resolution}.")
            img_resized = img.resize(resolution, Image.Resampling.LANCZOS)

        if img_resized.mode != 'RGB':
            vprint("Converting image to RGB mode.")
            img_resized = img_resized.convert('RGB')

    img_resized.save(wallpaper_file, format='PNG')
    subprocess.run(["systemctl", "--user", "restart", "hyprpaper"], check=True)


def hyprland_set_border_color(color: str) -> None:
    """Sets the border color in Hyprland configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "hypr", "modules", "decorator.lua")

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
    if update_config_file(config_path, updates):
        diff_configs(config_path)
    else:
        vprint(f"No changes detected in the configuration file {os.path.basename(config_path)}.")


def hyprlock_set_color(color: str) -> None:
    """Sets the color in Hyprlock configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "hypr", "hyprlock.conf")
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

    if update_config_file(config_path, updates):
        diff_configs(config_path)
    else:
        vprint(f"No changes detected in the configuration file {os.path.basename(config_path)}.")


def waybar_color(color: str) -> None:
    """Sets the color in Waybar configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "waybar", "style.css")

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
    if update_config_file(config_path, updates):
        subprocess.run(["systemctl", "--user", "restart", "waybar"], check=True)
        diff_configs(config_path)
    else:
        vprint(f"\nNo changes detected in the configuration file {os.path.basename(config_path)}.")

def wlogout_set_color(color: str) -> None:
    """Sets the color in wlogout configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "wlogout", "style.css")

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
    if update_config_file(config_path, updates):
        diff_configs(config_path)
    else:
        vprint(f"No changes detected in the configuration file {os.path.basename(config_path)}.")


def rofi_set_color(color: str) -> None:
    """Sets the color in rofi configuration."""
    validate_hex_color(color)
    config_path = os.path.join(get_config_dir(), "rofi", "colors.rasi")

    brightness = get_brightness(color)
    dark_color = darken_color(color)
    light_color = lighten_color(color)
    
    primary = light_color if brightness < 128 else dark_color
    text_color_select = "fafafa" if brightness < 128 else "0a0a0a"
    color_rgb = hex_to_rgb(light_color)
    bg_rgba = f"rgba({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]}, 0.7)"

    updates = {
        "background": bg_rgba,
        "primary": f"#{primary}",
        "on-surface": "#0f0f0f",
        "on-surface-variant": "#fafafa",
        "on-primary-fixed": f"#{dark_color}",
        "text-color-select": f"#{text_color_select}",
    }

    with open(config_path, "r") as f:
        config = f.read()

    original_config = config

    for key, value in updates.items():
        pattern = rf"(?m)^(\s*{re.escape(key)}\s*:\s*).*$"
        replacement = rf"\1{value};"
        config, count = re.subn(pattern, replacement, config, count=1)

        if count == 0:
            # Preserve the theme block even if the target key is missing.
            insertion = f"    {key}: {value};"
            closing_brace = re.search(r"(?m)^}\s*$", config)
            if closing_brace:
                config = f"{config[:closing_brace.start()].rstrip()}\n{insertion}\n{config[closing_brace.start():]}"

    if config != original_config:
        save_config(config_path)
        with open(config_path, "w") as f:
            f.write(config)
        diff_configs(config_path)
    else:
        vprint(f"No changes detected in the configuration file {os.path.basename(config_path)}.")


def kitty_set_color(color_list: List[str], mode: str = "Default") -> None:
    """Sets the color in kitty configuration."""
    if mode not in kitty_modes:
        raise ValueError(f"Invalid mode. Supported modes are: {', '.join(kitty_modes)}.")
    config_path = os.path.join(get_config_dir(), "kitty", "theme.conf")

    for color in color_list:
        validate_hex_color(color)
    
    with open(config_path, "r") as f:
        config = f.read()
    original_config = config
    
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
    
    if config != original_config:
        save_config(config_path)
        with open(config_path, "w") as f:
            f.write(config)

        subprocess.run(["kitty", "@", "set-colors", config_path], check=True)
        diff_configs(config_path)
    else:
        vprint(f"No changes detected in the configuration file {os.path.basename(config_path)}.")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Set Hyprland wallpaper and propagate colors to related configs.",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Image path and/or kitty mode.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logs and step timing output.",
    )
    return parser.parse_args()

def main() -> None:
    """Main function to run the wallpaper script."""
    global VERBOSE, DEBUG

    args = parse_args()
    VERBOSE = args.verbose
    DEBUG = args.verbose

    userDirectory = os.path.expanduser("~")
    debug_log("Verbose/debug mode is enabled.")

    if args.inputs:
        vprint(f"Arguments provided: {' '.join(args.inputs)}")

    kitty_mode = "Default"
    image = None

    for arg in args.inputs:
        if arg in kitty_modes:
            kitty_mode = arg
        elif os.path.exists(arg):
            image = arg
        else:
            print(f"Invalid argument: {arg}")

    vprint("Starting wallpaper script...")
    if not image:
        vprint("No image provided, selecting a random wallpaper...")
        wallpapers_dir = os.path.join(userDirectory, WALLPAPER_PATH)
        if not os.path.exists(wallpapers_dir):
            raise FileNotFoundError(f"Wallpapers directory does not exist: {wallpapers_dir}")
        vprint(f"Looking for wallpapers in: {wallpapers_dir}")
        image = get_random_image(wallpapers_dir)
    else:
        image = image.strip('"')  # Remove quotes if the path is provided with them
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file does not exist: {image}")
        vprint(f"Using provided image: {image}")
        if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            raise ValueError("Selected file is not a valid image format. Supported formats are: PNG, JPEG, BMP.")

    vprint(f"Selected wallpaper: {image}")
    run_debug_step("set wallpaper", hyprland_set_wallpaper, image)

    dominant_color = run_debug_step("extract dominant colors", get_cached_dominant_colors, image, n_colors=16)

    if not dominant_color:
        raise ValueError("No dominant color found in the image.")

    run_debug_step("update hyprland border", hyprland_set_border_color, dominant_color[0])
    run_debug_step("update hyprlock", hyprlock_set_color, dominant_color[0])
    run_debug_step("update waybar", waybar_color, dominant_color[0])
    run_debug_step("update wlogout", wlogout_set_color, dominant_color[0])
    run_debug_step("update rofi", rofi_set_color, dominant_color[0])
    run_debug_step("update kitty", kitty_set_color, dominant_color, mode=kitty_mode)

    vprint("All configurations updated successfully.")
    vprint(f"Primary color: {dominant_color[0]} (brightness: {get_brightness(dominant_color[0]):.0f})")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, OSError, ImportError, PermissionError, RuntimeError) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        vprint("Exiting the script. Goodbye!")
        sys.exit(0)
