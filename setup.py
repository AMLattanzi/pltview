from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py
import subprocess
import os
import sys
import shutil


class BuildCExtension:
    """Mixin class to build C extension during install/develop"""
    
    def run(self):
        # Build the C version first
        self.build_c_version()
        # Run the original install/develop/build
        super().run()
    
    def build_c_version(self):
        """Compile the C version of pltview"""
        print("=" * 60)
        print("Building C version of pltview...")
        print("=" * 60)
        
        # Check if we're on a system with X11
        x11_paths = ['/usr/include/X11', '/opt/X11/include', '/usr/X11R6/include']
        has_x11 = any(os.path.exists(p) for p in x11_paths)
        
        if not has_x11:
            print("Warning: X11 not found. Skipping C version build.")
            print("Only Python version will be available.")
            print("=" * 60)
            return
        
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
        
        # Compile command
        compile_cmd = [
            'gcc', '-O3', '-Wall', '-march=native',
            f'-I{x11_include}',
            '-o', 'pltview_c', 'pltview.c',
            '-lX11', '-lXt', '-lXaw', '-lXmu', '-lm',
            f'-L{x11_lib}'
        ]
        
        try:
            print(f"Running: {' '.join(compile_cmd)}")
            subprocess.run(compile_cmd, check=True, cwd=os.path.dirname(__file__) or '.')
            print("✓ C version built successfully!")
            print("=" * 60)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to build C version: {e}")
            print("Only Python version will be available.")
            print("=" * 60)
        except FileNotFoundError:
            print("Warning: gcc not found. Skipping C version build.")
            print("Only Python version will be available.")
            print("=" * 60)


class CustomInstall(BuildCExtension, install):
    """Custom install command that builds C extension"""
    
    def run(self):
        super().run()
        # Copy pltview_c to scripts directory if it exists
        if os.path.exists('pltview_c'):
            scripts_dir = os.path.join(self.install_scripts)
            os.makedirs(scripts_dir, exist_ok=True)
            dest = os.path.join(scripts_dir, 'pltview_c')
            print(f"Installing pltview_c to {dest}")
            shutil.copy2('pltview_c', dest)
            os.chmod(dest, 0o755)


class CustomDevelop(BuildCExtension, develop):
    """Custom develop command that builds C extension"""
    pass


class CustomBuildPy(BuildCExtension, build_py):
    """Custom build_py command that builds C extension"""
    pass


setup(
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
        'build_py': CustomBuildPy,
    },
)
