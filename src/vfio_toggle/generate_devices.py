#!/usr/bin/env python3

import os
import json
import subprocess

DEVICES_FILE = "/etc/vfio-toggle/devices.json"

def find_nvidia_devices():
    """Find NVIDIA devices on the system."""
    try:
        result = subprocess.run(["lspci", "-nn"], stdout=subprocess.PIPE, text=True)
        devices = []
        for line in result.stdout.splitlines():
            if "NVIDIA" in line:
                device_id = line.split()[0]  # Extract the PCI address
                devices.append(f"0000:{device_id}")
        return devices
    except FileNotFoundError:
        print("Error: lspci command not found.")
        return []

def generate_devices_file():
    """Generate the devices.json file."""
    devices = find_nvidia_devices()
    if not devices:
        print("No NVIDIA devices found.")
        return

    os.makedirs(os.path.dirname(DEVICES_FILE), exist_ok=True)
    with open(DEVICES_FILE, "w") as f:
        json.dump({"devices": devices}, f, indent=4)

    print(f"Devices file generated at {DEVICES_FILE}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root.")
        exit(1)

    generate_devices_file()
