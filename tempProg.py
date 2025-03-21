import sys
import os

def verify_filename():
    if os.path.basename(__file__) != "tempProg1.py":
        print("Error: This script must be named 'tempProg.py'. Exiting...")
        sys.exit(1)

verify_filename()

print('good')