"""QR code generation helpers.

This module provides small utility functions for generating QR codes from:
- A raw URL string
- Text file contents
- Binary file contents (base64-encoded before embedding)

It also exposes a helper to estimate the maximum binary payload size that can
fit in a single QR symbol once base64 overhead is accounted for.
"""

import qrcode  # Third-party library for creating QR codes
import os  # Filesystem utilities (path operations and file size)
import base64  # For encoding binary data into text (base64)

# Constants
# Approximate maximum number of bytes that can be stored in a single QR symbol
# at a common configuration (depends on version and error correction). This is
# used here as a practical upper bound for plain text content.
MAX_QR_CAPACITY = 2953

# Multiplicative overhead when converting raw bytes to base64 text. Base64
# typically expands data by ~4/3 (≈1.33x), ignoring minor padding differences.
BASE64_OVERHEAD = 1.33

def calculate_max_file_size():
    """Return max binary file size (in bytes) that fits after base64 encoding.

    We estimate by dividing the raw QR capacity by the base64 expansion factor.
    This is used for binary files since they are encoded to base64 before
    embedding in the QR code.
    """
    return int(MAX_QR_CAPACITY / BASE64_OVERHEAD)

def generate_qr(data, output_file, is_binary=False):
    """Create and save a QR code image from the provided data string.

    Parameters:
    - data: str — the text content to embed in the QR symbol.
    - output_file: str — path where the generated image (PNG) will be saved.
    - is_binary: bool — whether the source was binary (affects user messaging).

    Returns True on success, False on error (and prints a message).
    """
    try:
        # Build a QRCode object; version=None lets the library pick the minimum
        # size that can fit the provided data at the chosen error correction.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Add the payload and let the library compute the optimal layout
        qr.add_data(data)
        qr.make(fit=True)

        # Render to a PIL image and write it to disk
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_file)
        
        if is_binary:
            print(f"[+] QR code successfully generated from binary file and saved as {output_file}")
            print("[!] Note: The QR code contains base64 encoded data. Decode with base64 to recover the original file.")
        else:
            print(f"[+] QR code successfully generated and saved as {output_file}")
            
        return True
    except Exception as e:
        print(f"[-] Error generating QR code: {e}")
        return False

def generate_qr_from_url(url, output_file="qrcode.png"):
    """Generate a QR code directly from a URL string."""
    return generate_qr(url, output_file)

def generate_qr_from_text_file(file_path, output_file="qrcode.png"):
    """Read a text file and encode its contents into a QR code image.

    Only common text file extensions are accepted to help distinguish from
    binary files. Content is embedded as-is (no base64), so the raw QR symbol
    capacity (MAX_QR_CAPACITY) is used for size checking.
    """
    try:
        # A small allowlist of typical text file extensions
        text_extensions = ['.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv', '.md']
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext not in text_extensions:
            print(f"[-] Error: Not a text file. Detected: {file_ext}. Use option 3 for binary files.")
            return False
        
        # Read text content as UTF-8. If this fails, we treat it as binary.
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # For plain text, compare against raw capacity. Note the printed
        # max value references the base64-adjusted helper (used for binaries).
        # This keeps user-facing guidance consistent across modes.
        max_size = calculate_max_file_size()
        if len(content) > MAX_QR_CAPACITY:
            print(f"[-] Error: File too large. Max: {max_size/1024:.1f} KB, Your file: {len(content)/1024:.1f} KB")
            return False
        
        return generate_qr(content, output_file)
        
    except UnicodeDecodeError:
        print("[-] Error: This is a binary file. Use option 3 instead.")
        return False
    except FileNotFoundError:
        print("[-] Error: File not found.")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def generate_qr_from_binary_file(file_path, output_file="qrcode.png"):
    """Read a binary file, base64-encode its bytes, and encode into a QR.

    The file size is validated against the base64-adjusted capacity to reduce
    the chance of producing an oversized QR symbol that cannot be rendered.
    """
    try:
        # Determine raw byte size and the maximum allowed when base64 encoded
        file_size = os.path.getsize(file_path)
        max_size = calculate_max_file_size()
        
        if file_size > max_size:
            print(f"[-] Error: File too large. Max: {max_size/1024:.1f} KB, Your file: {file_size/1024:.1f} KB")
            return False
        
        # Read the entire file as bytes and convert to base64 text
        with open(file_path, 'rb') as file:
            binary_content = file.read()
        
        encoded_content = base64.b64encode(binary_content).decode('utf-8')
        return generate_qr(encoded_content, output_file, is_binary=True)
        
    except FileNotFoundError:
        print("[-] Error: File not found.")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False
