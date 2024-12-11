#!/usr/bin/env python3

import os
import sys
import json

# Paths
STATE_FILE = "/var/lib/vfio-toggle/state"
DEVICES_FILE = "/etc/vfio-toggle/devices.json"

def load_devices():
    """Load the list of devices from devices.json."""
    if not os.path.exists(DEVICES_FILE):
        print(f"Error: Devices file not found at {DEVICES_FILE}")
        sys.exit(1)
    with open(DEVICES_FILE, "r") as f:
        try:
            devices = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {DEVICES_FILE}")
            sys.exit(1)
    return devices.get("devices", [])

def bind_driver(dev, driver):
    """Bind a PCI device to a driver."""
    try:
        with open(f"/sys/bus/pci/devices/{dev}/driver/unbind", "w") as unbind_file:
            unbind_file.write(dev)
        with open(f"/sys/bus/pci/devices/{dev}/driver_override", "w") as override_file:
            override_file.write(driver)
        with open(f"/sys/bus/pci/drivers/{driver}/bind", "w") as bind_file:
            bind_file.write(dev)
    except FileNotFoundError:
        print(f"Error: Device {dev} or driver {driver} not found.")
        return False
    except PermissionError:
        print(f"Permission denied while accessing {dev} or {driver}.")
        return False
    return True

def toggle_state(devices):
    """Toggle between VFIO and NVIDIA driver states."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as state_file:
            last_state = state_file.read().strip()
    else:
        last_state = "nvidia"

    new_state = "vfio" if last_state == "nvidia" else "nvidia"

    print(f"Toggling to {new_state} driver...")
    for dev in devices:
        success = bind_driver(dev, "vfio-pci" if new_state == "vfio" else "nvidia")
        if not success:
            print(f"Failed to bind {dev} to {new_state} driver.")
            return

    with open(STATE_FILE, "w") as state_file:
        state_file.write(new_state)

    print(f"Switched to {new_state} driver.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

    devices = load_devices()
    if not devices:
        print("Error: No devices found in devices.json")
        sys.exit(1)

    toggle_state(devices)
