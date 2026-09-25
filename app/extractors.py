"""Document Text Extraction for PDF, DOCX, and Text Files."""

import io
import logging
from typing import Tuple
from pypdf import PdfReader
from docx import Document

logger = logging.getLogger("clausepilot.extractors")

def extract_text_from_file(filename: str, file_bytes: bytes) -> Tuple[str, int]:
    """Extracts text and page count from uploaded document bytes."""
    ext = filename[filename.rfind("."):].lower() if "." in filename else ".txt"

    if ext == ".pdf":
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            pages_text = []
            for p in reader.pages:
                txt = p.extract_text() or ""
                pages_text.append(txt)
            full_text = "\n\n".join(pages_text).strip()
            return full_text, len(reader.pages)
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise ValueError(f"Could not read PDF content. It may be corrupt or encrypted: {e}")

    elif ext == ".docx":
        try:
            doc = Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            full_text = "\n\n".join(paragraphs).strip()
            # Estimate pages ~ 500 words per page
            est_pages = max(1, len(full_text.split()) // 400)
            return full_text, est_pages
        except Exception as e:
            logger.error(f"Failed to extract text from DOCX: {e}")
            raise ValueError(f"Could not read DOCX document: {e}")

    else:
        # Plain text, markdown, rtf
        for encoding in ["utf-8", "latin-1", "cp1252"]:
            try:
                full_text = file_bytes.decode(encoding).strip()
                est_pages = max(1, len(full_text.split()) // 400)
                return full_text, est_pages
            except UnicodeDecodeError:
                continue
        raise ValueError("Could not decode file content. Please upload UTF-8 text or standard PDF.")
