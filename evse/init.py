#!/usr/bin/env python

"""
Run this script just once to create the records of simulations for charging station.
"""

import signal
import sys
from pathlib import Path

from utils.generate_charges import simulate

NDEVICES = 10

PATH = Path("./static/")

def signal_handler(sig, frame):
    print("Blocking the simulations...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    FILE_PATH = PATH / "charges.json"
    if not FILE_PATH.exists():
        print("Starting simulations.\nThis can take a while...")
        print("PRESS CTRL + C FOR STOP THE SIMULATION!")
        simulate(NDEVICES, FILE_PATH)
        print("Generate simulations!")
    else:
        print("Already generate simulations!")
