import argparse
from vfio_toggle.vfio_toggle import toggle_state, load_devices
from vfio_toggle.generate_devices import generate_devices_file

def main():
    parser = argparse.ArgumentParser(description="VFIO Toggle Utility")
    subparsers = parser.add_subparsers(dest="command")

    toggle_parser = subparsers.add_parser("toggle", help="Toggle between VFIO and NVIDIA")
    gen_parser = subparsers.add_parser("generate", help="Generate devices.json based on NVIDIA cards")

    args = parser.parse_args()

    if args.command == "toggle":
        devices = load_devices()
        toggle_state(devices)
    elif args.command == "generate":
        generate_devices_file()
    else:
        parser.print_help()
