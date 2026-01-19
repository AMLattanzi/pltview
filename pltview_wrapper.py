#!/usr/bin/env python3
"""
Wrapper script for pltview that prefers the C version if available.
Falls back to Python version if C version is not found or fails.
"""
import os
import sys
import subprocess
import shutil


def main():
    # Try to find pltview_c in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    c_version = os.path.join(script_dir, 'pltview_c')
    
    # Also check in PATH
    if not os.path.exists(c_version):
        c_version = shutil.which('pltview_c')
    
    # If C version exists and we have DISPLAY, use it
    if c_version and os.path.exists(c_version) and os.environ.get('DISPLAY'):
        try:
            # Run the C version
            os.execv(c_version, [c_version] + sys.argv[1:])
        except Exception as e:
            print(f"Failed to run C version: {e}", file=sys.stderr)
            print("Falling back to Python version...", file=sys.stderr)
    
    # Fall back to Python version
    import pltview as pltview_module
    pltview_module.main()


if __name__ == '__main__':
    main()
