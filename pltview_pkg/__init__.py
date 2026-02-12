"""pltview package - contains the compiled C binary."""
import os

def get_binary_path():
    """Return the path to the compiled pltview binary."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pltview_bin')
