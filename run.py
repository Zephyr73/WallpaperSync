import argparse
import subprocess
import sys
import os
import json
from openrgb import OpenRGBClient

DEFAULT_IP = 'localhost'
DEFAULT_PORT = 6742
CONFIG_FILE = 'config.json'

def save_config(ip: str, port: int, config_file: str):
    """Save IP and port to a JSON configuration file."""
    config = {
        'ip': ip,
        'port': port
    }
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)
    print(f"Settings saved to {config_file}\n")

def load_config(config_file: str) -> (str, int):
    """Load IP and port from a JSON configuration file."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get('ip', DEFAULT_IP), config.get('port', DEFAULT_PORT)
    return DEFAULT_IP, DEFAULT_PORT

def connect_to_openrgb(ip: str, port: int) -> bool:
    """Attempt to connect to OpenRGB and return True if successful, False otherwise."""
    client = OpenRGBClient(ip, port)
    try:
        client.connect()
        client.disconnect()  # Disconnect after a successful connection
        return True
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def main(ip: str, port: int):
    """Main function to run sync.py with custom server IP and port."""
    while True:
        if connect_to_openrgb(ip, port):
            print("Connected to OpenRGB SDK")
            # Save configuration only if the connection is successful
            save_config(ip, port, CONFIG_FILE)
            break
        print("Could not connect to OpenRGB SDK.")
        ip = input("Enter the new server IP address (or press Enter to use default): ") or DEFAULT_IP
        port_str = input("Enter the new server port number (or press Enter to use default): ") or str(DEFAULT_PORT)
        try:
            port = int(port_str)
        except ValueError:
            print("Invalid port number. Please enter a numeric value.")
            continue

    # Path to sync.py
    sync_path = os.path.join(os.path.dirname(__file__), 'sync.py')
    
    # Prepare command to run sync.py with the given IP and port
    command = [
        sys.executable, sync_path,  # sys.executable ensures the same Python interpreter is used
        '--ip', str(ip),
        '--port', str(port)
    ]
    
    # Run sync.py with the provided arguments
    subprocess.run(command, cwd=os.path.dirname(sync_path))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run sync.py with custom server IP and port.")
    parser.add_argument('--ip', type=str, help='The server IP address')
    parser.add_argument('--port', type=int, help='The server port number')
    parser.add_argument('--config', type=str, help='Path to the JSON configuration file to save settings')
    
    args = parser.parse_args()

    # Load configuration if config file exists
    ip, port = load_config(CONFIG_FILE)
    
    # Override with command line arguments if provided
    if args.ip:
        ip = args.ip
    if args.port:
        port = args.port

    # Run the main function with the IP and port
    while True:
        try:
            main(ip, port)
            break  # Exit loop if main function succeeds
        except KeyboardInterrupt:
            print("Goodbye")
            sys.exit()  # Exit the script
        except Exception as e:
            print(f"Could not connect to OpenRGB SDK. Please retry: {e}")
            # Prompt user for new IP and port if connection fails
            ip = input("Enter the new server IP address (or press Enter to use default): ") or DEFAULT_IP
            port_str = input("Enter the new server port number (or press Enter to use default): ") or str(DEFAULT_PORT)
            try:
                port = int(port_str)
            except ValueError:
                print("Invalid port number. Please enter a numeric value.")
                continue
