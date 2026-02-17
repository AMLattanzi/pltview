#!/usr/bin/env python3
"""Entry point wrapper for pltview C binary."""
import os
import sys


def main():
    # Find the C binary

    # Method 1: Inside installed package (works for both pip install and editable)
    binary = None
    try:
        from pltview_pkg import get_binary_path, get_map_layers_path
        candidate = get_binary_path()
        if os.path.exists(candidate):
            binary = candidate
        map_layers_path = get_map_layers_path()
        if map_layers_path:
            os.environ.setdefault("PLTVIEW_MAP_LAYERS", map_layers_path)
    except ImportError:
        pass

    # Method 2: Same directory as this script (editable install / dev)
    if binary is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidate = os.path.join(script_dir, 'pltview')
        if os.path.exists(candidate):
            binary = candidate

    # Method 3: pltview_bin next to the wrapper script (legacy regular install)
    if binary is None:
        wrapper_path = os.path.abspath(sys.argv[0])
        wrapper_dir = os.path.dirname(wrapper_path)
        candidate = os.path.join(wrapper_dir, 'pltview_bin')
        if os.path.exists(candidate):
            binary = candidate

    if binary is None:
        print("Error: pltview binary not found!", file=sys.stderr)
        print("Searched in:", file=sys.stderr)
        try:
            from pltview_pkg import get_binary_path
            print(f"  - {get_binary_path()}", file=sys.stderr)
        except ImportError:
            print("  - pltview_pkg not installed", file=sys.stderr)
        print(f"  - {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pltview')}", file=sys.stderr)
        print("\nTry reinstalling: pip install --force-reinstall pltview", file=sys.stderr)
        sys.exit(1)

    # Execute the binary
    os.execv(binary, [binary] + sys.argv[1:])


if __name__ == '__main__':
    main()
