import pdfplumber


def extract_text(pdf_file) -> str:
    """Return all text from a PDF. Accepts a file path or a file-like object."""
    pages = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)

    full_text = "\n".join(pages).strip()
    if not full_text:
        raise ValueError("No text found. The PDF may be a scanned image.")
    return full_text.replace("(cid:127)", "•")


if __name__ == "__main__":
    import sys
    print(extract_text(sys.argv[1]))
