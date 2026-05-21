#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
import signal
import argparse

def toogle_state(program_name):
    try:
        # Check if the process is running
        result = subprocess.run(['pgrep', '-x', program_name], stdout=subprocess.PIPE)
        if result.stdout:
            # If the process is running, kill it
            pid = int(result.stdout.decode().strip())
            os.kill(pid, signal.SIGTERM)
            print(f"{program_name} has been closed.")
        else:
            # If the process is not running, start it
            subprocess.Popen([program_name])
            print(f"{program_name} has been opened.")
    except Exception as e:
        print(f"Error toggling process: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Toggle the state of a program.')
    parser.add_argument('program_name', type=str, help='The name of the program to toggle')
    args = parser.parse_args()

    toogle_state(args.program_name)
