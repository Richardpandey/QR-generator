import pyfiglet
from termcolor import colored

def show_banner():
    banner = pyfiglet.figlet_format("QRGen Tool", font="jazmine")
    print(colored(banner, "green"))
    print(" QR Code Generator Tool - Convert Files/URLs to QR Codes")
    print()
    print(colored("👤 Author: Richard | GitHub: Richardpandey", "green"))
    print()
    print(colored("------------------------------------------------------------\n", "white"))
