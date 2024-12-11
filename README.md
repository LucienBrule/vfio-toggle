# VFIO Toggle

Service to toggle VFIO passthrough

# VFIO Toggle Script

A Python-based script for toggling between VFIO passthrough and NVIDIA drivers, integrated with `systemd`.

## Features
- Dynamically toggle between `vfio-pci` and `nvidia` drivers.
- Works with `systemd` for enabling/disabling GPU passthrough.

## Setup
1. Clone the repository:
   ```bash
   git clone https://your-repo-url/vfio-toggle.git
   cd vfio-toggle
