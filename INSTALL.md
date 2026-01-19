# Installation Guide

## Quick Start

On your Linux server (or any system with X11), simply run:

```bash
pip install git+https://github.com/wang1202/pltview.git
```

The installation will:
1. Automatically detect if X11 development libraries are available
2. Build the ultra-fast C version if possible
3. Install both C and Python versions
4. Set up the `pltview` command to automatically use the C version

## What Gets Installed

After `pip install`:

- **pltview** - Smart wrapper that uses C version if available, Python otherwise
- **pltview-py** - Direct access to Python version
- **pltview_c** - Direct access to C version (in your PATH)

## Usage

```bash
# Just use this - it automatically picks the best version
pltview plt00100

# Force Python version if needed
pltview-py plt00100

# Direct C version
pltview_c plt00100
```

## Prerequisites

For the C version to build, you need X11 development libraries:

### Linux
**Debian/Ubuntu:**
```bash
sudo apt-get install libx11-dev libxt-dev libxaw7-dev libxmu-dev
```

**RHEL/CentOS/Fedora:**
```bash
sudo yum install libX11-devel libXt-devel libXaw-devel libXmu-devel
```

### macOS
Install XQuartz from https://www.xquartz.org/

## What Happens During Installation

1. **pip install** downloads the package
2. **setup.py** runs and checks for X11 libraries
3. If X11 is found, it compiles `pltview.c` → `pltview_c`
4. Installs Python files and the C binary to your PATH
5. Creates entry points for `pltview`, `pltview-py`

### Example Installation Output

```
Building C version of pltview...
============================================================
Using X11 from: /usr/include
Running: gcc -O3 -Wall -march=native -I/usr/include -o pltview_c pltview.c ...
✓ C version built successfully!
============================================================
```

If X11 is not available, you'll see:
```
Warning: X11 not found. Skipping C version build.
Only Python version will be available.
```

## Verification

After installation, verify everything works:

```bash
# Check which version will be used
pltview --help   # Should show usage info

# Check C version is in PATH
which pltview_c
```

## Performance

On a typical Linux server with a 320×512×100 dataset:
- **C version**: ~0.1 seconds to load and render
- **Python version**: ~2 seconds to load and render

The `pltview` command automatically uses the C version for maximum performance!
