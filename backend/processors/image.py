import pytesseract
from PIL import Image

def extract_text_from_image(filepath: str) -> str:
    """Extracts text from an image using Tesseract OCR locally."""
    # Note: On Windows, you might need to specify the path to tesseract.exe
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Error processing Image OCR: {e}")
        return ""
