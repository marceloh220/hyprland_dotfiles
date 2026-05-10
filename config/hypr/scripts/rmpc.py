#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

def rmpc_toggle():
    state = subprocess.run(["pgrep", "-x", "rmpc"], capture_output=True, text=True)
    if state.returncode == 0:
        subprocess.run(["pkill", "-x", "rmpc"])
    else:
        subprocess.run(["kitty", "--class", "showcase", "rmpc"])

if __name__ == "__main__":
    rmpc_toggle()