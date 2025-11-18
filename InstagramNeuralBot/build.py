"""
Build Script for Instagram Neural Bot
Builds Windows executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil


def check_requirements():
    """Check if required packages are installed"""
    print("Checking requirements...")

    try:
        import torch
        print("✓ PyTorch installed")
    except ImportError:
        print("❌ PyTorch not found. Install with: pip install torch")
        return False

    try:
        import PyInstaller
        print("✓ PyInstaller installed")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False

    return True


def clean_build():
    """Clean previous build artifacts"""
    print("\nCleaning previous builds...")

    dirs_to_remove = ['build', 'dist', '__pycache__']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")

    # Remove .spec files except build.spec
    for file in os.listdir('.'):
        if file.endswith('.spec') and file != 'build.spec':
            os.remove(file)
            print(f"  Removed {file}")

    print("✓ Cleanup complete")


def build_exe():
    """Build the executable"""
    print("\nBuilding executable...")
    print("This may take several minutes...")

    try:
        # Run PyInstaller
        result = subprocess.run(
            ['pyinstaller', 'build.spec'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ Build successful!")

            exe_path = os.path.join('dist', 'InstagramNeuralBot.exe')
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"\n✅ Executable created: {exe_path}")
                print(f"   Size: {size_mb:.1f} MB")
                return True
            else:
                print("❌ Executable not found after build")
                return False
        else:
            print("❌ Build failed!")
            print("\nError output:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


def main():
    """Main build process"""
    print("=" * 60)
    print("Instagram Neural Bot - Windows Build Script")
    print("=" * 60)

    # Check requirements
    if not check_requirements():
        print("\n❌ Please install missing requirements first:")
        print("   pip install -r requirements.txt")
        print("   pip install pyinstaller")
        sys.exit(1)

    # Clean previous builds
    clean_build()

    # Build executable
    if build_exe():
        print("\n" + "=" * 60)
        print("✅ BUILD SUCCESSFUL!")
        print("=" * 60)
        print("\nYour executable is ready at:")
        print("  dist/InstagramNeuralBot.exe")
        print("\nYou can now distribute this .exe file!")
        print("\nTo run it:")
        print("  1. Ensure an Android emulator is installed")
        print("  2. Double-click InstagramNeuralBot.exe")
        print("  3. Configure settings in the GUI")
        print("  4. Click 'Start Bot'")
    else:
        print("\n" + "=" * 60)
        print("❌ BUILD FAILED")
        print("=" * 60)
        print("\nPlease check the error messages above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
