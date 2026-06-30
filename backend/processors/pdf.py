import fitz  # PyMuPDF


def extract_text_from_pdf(filepath: str) -> str:
    """Extracts plain text from a given PDF file offline."""
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""
