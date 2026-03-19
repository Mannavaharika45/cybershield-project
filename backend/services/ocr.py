import pytesseract
from PIL import Image
import io
import os

# Set tesseract path for Windows if it exists at default location
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Ensure Tesseract can process it, converting if necessary or leaving
        # as is
        text = pytesseract.image_to_string(image)
        return text
    except pytesseract.TesseractNotFoundError:
        # Fallback if tesseract isn't installed
        return "[OCR Failed: Tesseract-OCR is not installed or not in PATH.]"
    except Exception as e:
        print(f"Error in OCR matching: {e}")
        return f"[OCR Error: {str(e)}]"
