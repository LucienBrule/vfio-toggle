#!/bin/bash

# Ensure script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi

# Install Python requirements
pip3 install -r requirements.txt

# Place Python script
install -Dm755 vfio-toggle.py /usr/local/bin/vfio-toggle.py
install -Dm755 generate_devices.py /usr/local/bind/generate_devices.py

# Generate devices.json
/usr/local/bin/generate_devices.py

# Place systemd service
install -Dm644 vfio-toggle.service /etc/systemd/system/vfio-toggle.service

# Reload systemd
systemctl daemon-reload

echo "Setup complete. Enable the service using:"
echo "  sudo systemctl enable vfio-toggle.service"
echo "  sudo systemctl start vfio-toggle.service"
