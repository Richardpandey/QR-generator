#!/usr/bin/env python3  # Allows running this script directly on Unix-like systems
import os  # Standard library module for filesystem and path utilities
from banner import show_banner  # Prints the application banner/logo
from generator import *  # Imports QR generation helpers (URL/text/binary, size calc)

# This script provides a simple CLI to generate QR codes from:
# 1) A URL string
# 2) The contents of a text file
# 3) The raw bytes of a binary file (within encoder size limits)
#
# It prompts the user for inputs, validates basic conditions (e.g., file exists),
# ensures the output directory exists, and delegates QR creation to functions
# defined in `generator.py`.

def get_output_file():
    """Ask for an output image path and create its directory if needed.

    Returns the user-specified path or the default 'qrcode.png' when left blank.
    """
    # Read a desired output file path; default to 'qrcode.png' when empty
    output_file = input("Output file path (default: qrcode.png): ").strip() or "qrcode.png"

    # Extract directory portion (may be empty when only a filename is provided)
    output_dir = os.path.dirname(output_file)

    # Create the directory if it was specified and doesn’t exist yet
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[+] Created directory: {output_dir}")

    # Return the path (relative or absolute) to be used for the generated QR image
    return output_file

def main():
    """Entry point for the CLI menu and QR code generation workflow."""
    # Display the app banner for a friendly CLI experience
    show_banner()

    # Determine the maximum supported payload size from the encoder
    max_size = calculate_max_file_size()
    print(f"[i] Maximum file size: {max_size/1024:.1f} KB\n")

    # Present options for what to encode into a QR code
    print("Options:")
    print("1. Convert URL to QR Code")
    print("2. Convert Text File to QR Code")
    print("3. Convert Binary File to QR Code")
    
    # Read and normalize the user's choice
    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        # Option 1: Encode a URL string as a QR code image
        url = input("Enter URL: ").strip()
        if url:
            # Prompt for output path and generate the PNG
            generate_qr_from_url(url, get_output_file())
        else:
            # Simple validation for empty input
            print("[-] URL cannot be empty!")

    elif choice == "2":
        # Option 2: Read a text file’s content and encode it
        file_path = input("Enter text file path: ").strip()
        if file_path and os.path.exists(file_path):
            generate_qr_from_text_file(file_path, get_output_file())
        else:
            # File path was empty or the file does not exist
            print("[-] File not found!")

    elif choice == "3":
        # Option 3: Read raw bytes from a binary file and encode them
        file_path = input("Enter binary file path: ").strip()
        if file_path and os.path.exists(file_path):
            generate_qr_from_binary_file(file_path, get_output_file())
        else:
            # File path was empty or the file does not exist
            print("[-] File not found!")

    else:
        # Handle any entry outside of 1–3
        print("[-] Invalid choice!")

if __name__ == "__main__":
    # Execute the CLI only when this script is run directly
    main()
