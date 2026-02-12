from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build import build
from setuptools.command.editable_wheel import editable_wheel
import subprocess
import os


def build_c_binary():
    """Compile the C version of pltview into pltview_pkg/"""
    print("=" * 60)
    print("Building pltview (C version)...")
    print("=" * 60)

    # Check if we're on a system with X11
    x11_paths = ['/usr/include/X11', '/opt/X11/include', '/usr/X11R6/include']
    has_x11 = any(os.path.exists(p) for p in x11_paths)

    if not has_x11:
        raise RuntimeError(
            "X11 development libraries not found!\n"
            "Please install:\n"
            "  - macOS: Install XQuartz from https://www.xquartz.org/\n"
            "  - Debian/Ubuntu: sudo apt-get install libx11-dev libxt-dev libxaw7-dev libxmu-dev\n"
            "  - RHEL/CentOS: sudo yum install libX11-devel libXt-devel libXaw-devel libXmu-devel"
        )

    # Determine X11 include and lib paths
    if os.path.exists('/opt/X11/include'):
        x11_include = '/opt/X11/include'
        x11_lib = '/opt/X11/lib'
    elif os.path.exists('/usr/include/X11'):
        x11_include = '/usr/include'
        x11_lib = '/usr/lib'
    else:
        x11_include = '/usr/X11R6/include'
        x11_lib = '/usr/X11R6/lib'

    print(f"Using X11 from: {x11_include}")

    src_dir = os.path.dirname(__file__) or '.'
    output = os.path.join(src_dir, 'pltview_pkg', 'pltview_bin')

    # Compile command
    compile_cmd = [
        'gcc', '-O3', '-Wall', '-march=native',
        f'-I{x11_include}',
        '-o', output, 'pltview.c',
        '-lX11', '-lXt', '-lXaw', '-lXmu', '-lm',
        f'-L{x11_lib}'
    ]

    try:
        print(f"Running: {' '.join(compile_cmd)}")
        subprocess.run(compile_cmd, check=True, cwd=src_dir)
        print("✓ pltview built successfully!")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to build C version: {e}")
    except FileNotFoundError:
        raise RuntimeError("gcc not found. Please install gcc compiler.")


class BuildC(build):
    """Custom build command that compiles C version"""

    def run(self):
        build_c_binary()
        super().run()


class EditableWheel(editable_wheel):
    """Custom editable_wheel command to build C binary"""

    def run(self):
        print("Running editable_wheel - building C binary...")
        build_c_binary()
        super().run()


class InstallC(install):
    """Custom install command that installs C binary"""

    def run(self):
        build_c_binary()
        super().run()


class DevelopC(develop):
    """Custom develop command for editable install"""

    def run(self):
        print("Running develop - building C binary...")
        build_c_binary()
        super().run()


setup(
    cmdclass={
        'build': BuildC,
        'install': InstallC,
        'develop': DevelopC,
        'editable_wheel': EditableWheel,
    },
)
