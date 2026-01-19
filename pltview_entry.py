#!/usr/bin/env python3
"""Entry point wrapper for pltview C binary."""
import os
import sys


def main():
    # Find the C binary
    # Method 1: Same directory as this script (editable install from source)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    binary = os.path.join(script_dir, 'pltview')
    
    # Method 2: Parent directory (editable install)
    if not os.path.exists(binary):
        binary = os.path.join(os.path.dirname(script_dir), 'pltview')
    
    # Method 3: Look in bin directory (regular install)
    if not os.path.exists(binary):
        # Get the bin directory (same as where this wrapper is installed)
        # For wrapper at ~/.conda-envs/newenv/bin/pltview, binary should be at ~/.conda-envs/newenv/bin/pltview_bin
        wrapper_path = os.path.abspath(sys.argv[0])
        wrapper_dir = os.path.dirname(wrapper_path)
        binary = os.path.join(wrapper_dir, 'pltview_bin')
    
    # Method 4: Try without _bin suffix
    if not os.path.exists(binary):
        wrapper_path = os.path.abspath(sys.argv[0])
        wrapper_dir = os.path.dirname(wrapper_path)
        # Look for the actual binary in the same bin directory
        for potential_name in ['pltview', '.pltview-wrapped']:
            potential_binary = os.path.join(wrapper_dir, potential_name)
            if os.path.exists(potential_binary) and os.access(potential_binary, os.X_OK):
                # Make sure it's not this wrapper script itself
                if potential_binary != wrapper_path:
                    binary = potential_binary
                    break
    
    if not os.path.exists(binary):
        print("Error: pltview binary not found!", file=sys.stderr)
        print(f"Searched in:", file=sys.stderr)
        print(f"  - {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pltview')}", file=sys.stderr)
        print(f"  - {os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pltview')}", file=sys.stderr)
        if 'wrapper_dir' in locals():
            print(f"  - {os.path.join(wrapper_dir, 'pltview_bin')}", file=sys.stderr)
        print("\nFor editable install: Run 'make' in the source directory", file=sys.stderr)
        print("For regular install: The installation may have failed", file=sys.stderr)
        sys.exit(1)
    
    # Execute the binary
    os.execv(binary, [binary] + sys.argv[1:])


if __name__ == '__main__':
    main()
