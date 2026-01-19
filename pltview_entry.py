#!/usr/bin/env python3
"""Entry point wrapper for pltview C binary."""
import os
import sys


def main():
    # Find the C binary in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    binary = os.path.join(script_dir, 'pltview')
    
    # If not found, try looking in parent directory (for editable install)
    if not os.path.exists(binary):
        binary = os.path.join(os.path.dirname(script_dir), 'pltview')
    
    if not os.path.exists(binary):
        print("Error: pltview binary not found!", file=sys.stderr)
        print(f"Expected at: {binary}", file=sys.stderr)
        print("Try running: make", file=sys.stderr)
        sys.exit(1)
    
    # Execute the binary
    os.execv(binary, [binary] + sys.argv[1:])


if __name__ == '__main__':
    main()
