#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import argparse

def check_hypridle_state() -> bool:
    state = subprocess.run(['systemctl', '--user', 'is-active', 'hypridle'], capture_output=True, text=True)
    if state.stdout.strip() == "active":
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toggle HyprIdle on or off.")
    parser.add_argument('--toggle', action='store_true', help='Toggle HyprIdle on or off')
    parser.add_argument('--status', action='store_true', help='Check the current status of HyprIdle')
    args = parser.parse_args()
    
    if args.toggle:
        if check_hypridle_state():
            subprocess.run(['systemctl', '--user', 'stop', 'hypridle'])
        else:
            subprocess.run(['systemctl', '--user', 'start', 'hypridle'])
    elif args.status:
        if check_hypridle_state():
            # This format is nessecary for waybar to display the status correctly
            print('{"text": "RUNNING", "class": "active", "tooltip": "Hypridle active\\nLeft: Deactivate"}', end = "\t\n")
        else:
            print('{"text": "NOT RUNNING", "class": "notactive", "tooltip": "Hypridle deactivated\\nLeft: Activate"}', end = "\t\n")
