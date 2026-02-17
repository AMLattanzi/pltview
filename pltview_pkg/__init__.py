"""pltview package - contains the compiled C binary and resources."""
import os

def get_binary_path():
    """Return the path to the compiled pltview binary."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pltview_bin')

def get_map_layers_path():
    """Return the path to installed map layers, if present."""
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(pkg_dir, 'map_layers')
    if os.path.isdir(path):
        return path
    dev_path = os.path.join(os.path.dirname(pkg_dir), 'map_layers')
    return dev_path if os.path.isdir(dev_path) else None
