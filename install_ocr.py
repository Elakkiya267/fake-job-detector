#!/usr/bin/env python3
"""
OCR Setup Script for Fake Job Postings Detection App
This script helps install and configure Tesseract OCR for image text extraction.
"""

import os
import sys
import platform
import subprocess

def check_tesseract():
    """Check if Tesseract is installed and accessible."""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, check=True)
        print("✅ Tesseract is already installed!")
        print(f"Version: {result.stdout.split()[1]}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_tesseract_windows():
    """Instructions for installing Tesseract on Windows."""
    print("\n📋 Windows Installation Instructions:")
    print("1. Download Tesseract installer from:")
    print("   https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. Run the installer and follow the setup wizard")
    print("3. Add Tesseract to your PATH environment variable")
    print("   Default path: C:\\Program Files\\Tesseract-OCR")
    print("4. Restart your command prompt/IDE")
    print("\n💡 Alternative: Use Windows Package Manager")
    print("   winget install UB-Mannheim.TesseractOCR")

def install_tesseract_mac():
    """Instructions for installing Tesseract on macOS."""
    print("\n📋 macOS Installation Instructions:")
    print("Using Homebrew (recommended):")
    print("   brew install tesseract")
    print("\nUsing MacPorts:")
    print("   sudo port install tesseract")

def install_tesseract_linux():
    """Instructions for installing Tesseract on Linux."""
    print("\n📋 Linux Installation Instructions:")
    print("Ubuntu/Debian:")
    print("   sudo apt-get update")
    print("   sudo apt-get install tesseract-ocr")
    print("\nCentOS/RHEL/Fedora:")
    print("   sudo yum install tesseract")
    print("   # or")
    print("   sudo dnf install tesseract")

def setup_pytesseract_config():
    """Create a configuration file for pytesseract if needed."""
    config_content = '''
# Tesseract Configuration for Job Posting OCR
# Uncomment and modify the path below if tesseract is not in your PATH

import pytesseract
import os

# Windows example (uncomment if needed):
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# macOS example (uncomment if needed):
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Linux example (usually not needed):
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def configure_tesseract():
    """Configure pytesseract path if needed."""
    # This function can be imported in your main app
    system = os.name
    if system == 'nt':  # Windows
        possible_paths = [
            r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
            r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe',
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
'''
    
    config_file = os.path.join(os.path.dirname(__file__), 'tesseract_config.py')
    with open(config_file, 'w') as f:
        f.write(config_content)
    print(f"✅ Created configuration file: {config_file}")

def main():
    print("🔧 Fake Job Postings Detection - OCR Setup")
    print("=" * 50)
    
    # Check current system
    system = platform.system().lower()
    print(f"Detected OS: {platform.system()}")
    
    # Check if Tesseract is already installed
    if check_tesseract():
        print("✅ OCR is ready to use!")
        setup_pytesseract_config()
        return
    
    print("\n❌ Tesseract OCR not found. Installation required.")
    
    # Provide installation instructions based on OS
    if system == 'windows':
        install_tesseract_windows()
    elif system == 'darwin':  # macOS
        install_tesseract_mac()
    elif system == 'linux':
        install_tesseract_linux()
    else:
        print(f"\n⚠️  Unsupported OS: {system}")
        print("Please install Tesseract manually from: https://github.com/tesseract-ocr/tesseract")
    
    print("\n📦 Python Dependencies:")
    print("Make sure you have installed the required packages:")
    print("   pip install -r requirements.txt")
    
    print("\n🔄 After installing Tesseract:")
    print("1. Restart your terminal/command prompt")
    print("2. Run this script again to verify installation")
    print("3. Start your Flask backend: python backend/app.py")
    
    setup_pytesseract_config()

if __name__ == "__main__":
    main()