#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import subprocess
from typing import Tuple

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
        
        return width, height, scale
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to get monitor resolution: {e}")


def main():
    res_w, res_h, h_scale = get_monitor_resolution()
    h_scale = int(h_scale * 100)  # Convert to integer percentage
    w_margin = res_h * 37 // h_scale
    subprocess.run(['wlogout', '-b', '4', '-T', str(w_margin), '-B', str(w_margin)])

if __name__ == "__main__":
    main()
