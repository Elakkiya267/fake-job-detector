
# Tesseract Configuration for Job Posting OCR
# Uncomment and modify the path below if tesseract is not in your PATH

import pytesseract
import os

# Windows example (uncomment if needed):
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
