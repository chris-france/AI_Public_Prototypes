"""
File extraction module for the Local RAG System.
Supports PDF, DOCX, and TXT file parsing with page mapping for PDFs.
"""

import io
from PyPDF2 import PdfReader
from docx import Document


def extract_text(filename: str, content: bytes) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        reader = PdfReader(io.BytesIO(content))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == "docx":
        doc = Document(io.BytesIO(content))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif ext == "txt":
        return content.decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def get_page_map(filename: str, content: bytes) -> dict[int, int] | None:
    """For PDFs, return a mapping of character offset -> page number."""
    if not filename.lower().endswith(".pdf"):
        return None
    reader = PdfReader(io.BytesIO(content))
    page_map = {}
    offset = 0
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        page_map[offset] = i + 1
        offset += len(text) + 2  # +2 for \n\n separator
    return page_map


def char_offset_to_page(offset: int, page_map: dict[int, int] | None) -> int | None:
    if page_map is None:
        return None
    page = None
    for start, pg in sorted(page_map.items()):
        if start <= offset:
            page = pg
        else:
            break
    return page
