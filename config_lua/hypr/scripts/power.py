#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import json
import argparse
import os
import signal

def terminate_clients() -> None:
    TIMEOUT = 5
    POLL_INTERVAL = 0.1
    # Get a list of all client PIDs in the current Hyprland session
    client_pids = subprocess.check_output(['hyprctl', 'clients', '-j']).decode('utf-8')
    client_pids = [client['pid'] for client in json.loads(client_pids)]
    print(f":: Found client PIDs: {client_pids}")

    if not client_pids:
        return

    # Send SIGTERM (kill -15) to each client PID and wait for termination
    for pid in client_pids:
        print(f":: Sending SIGTERM to PID {pid}")
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            # Process already exited between listing clients and signaling.
            pass
        except PermissionError:
            print(f":: No permission to signal PID {pid}")

    deadline = time.monotonic() + TIMEOUT
    remaining = set(client_pids)

    while remaining and time.monotonic() < deadline:
        terminated = set()
        for pid in remaining:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                terminated.add(pid)
                print(f":: PID {pid} has terminated.")
            except PermissionError:
                # If we cannot query status, stop waiting for this PID.
                terminated.add(pid)
                print(f":: Cannot verify PID {pid}, skipping wait.")

        remaining -= terminated
        if remaining:
            print(f":: Waiting for PIDs to terminate... {sorted(remaining)}")
            time.sleep(POLL_INTERVAL)

    if remaining:
        print(f":: Timeout reached. Still running: {sorted(remaining)}")

def exit():
    print(":: Exit")
    terminate_clients()
    subprocess.run(['hyprctl', 'dispatch', 'hl.dsp.exit()'])

def lock():
    print(":: Lock")
    subprocess.run(['hyprlock'])

def reboot():
    print(":: Reboot")
    terminate_clients()
    subprocess.run(['systemctl', 'reboot'])

def shutdown():
    print(":: Shutdown")
    terminate_clients()
    subprocess.run(['systemctl', 'poweroff'])

def suspend():
    print(":: Suspend")
    subprocess.run(['systemctl', 'suspend'])

def hibernate():
    print(":: Hibernate")
    subprocess.run(['systemctl', 'hibernate'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Power management script for Hyprland')
    parser.add_argument('action', choices=['exit', 'lock', 'reboot', 'shutdown', 'suspend', 'hibernate', 'killthemall'], help='Action to perform')
    args = parser.parse_args()

    if args.action == 'exit':
        exit()
    elif args.action == 'lock':
        lock()
    elif args.action == 'reboot':
        reboot()
    elif args.action == 'shutdown':
        shutdown()
    elif args.action == 'suspend':
        suspend()
    elif args.action == 'hibernate':
        hibernate()
    elif args.action == 'killthemall':
        terminate_clients()
