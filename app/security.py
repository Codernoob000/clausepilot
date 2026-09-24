"""ClausePilot Security Layer: Validation, Sanitization, Injection Resistance, and Rate Limiting."""

import re
import time
import logging
from collections import defaultdict
from typing import Tuple, List, Optional
from fastapi import HTTPException, status, Request

logger = logging.getLogger("clausepilot.security")

# Allowed contract file extensions and MIME types
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".rtf", ".md"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
MAX_TEXT_LENGTH_CHARS = 100_000         # ~40 pages max

# Executable / binary signatures to reject
MALICIOUS_MAGIC_BYTES = [
    b"MZ",          # Windows PE Executable
    b"\x7fELF",     # Linux ELF Executable
    b"\xca\xfe\xba\xbe", # Mach-O / Java bytecode
    b"PK\x03\x04\x14\x00\x08", # Could be jar
    b"#!/bin/",     # Unix shell script
    b"#!/usr/bin/", # Unix script
]

SUSPICIOUS_SCRIPT_PATTERNS = [
    re.compile(r"<script[\s>]", re.IGNORECASE),
    re.compile(r"javascript:", re.IGNORECASE),
    re.compile(r"powershell\s+-enc", re.IGNORECASE),
    re.compile(r"cmd\.exe", re.IGNORECASE)
]


def sanitize_filename(filename: str) -> str:
    """Strip path traversal components and restrict to safe alphanumeric characters."""
    clean_name = re.sub(r"[^\w\s\.\-]", "_", filename).strip()
    return clean_name or "contract.txt"


def validate_file_upload(filename: str, file_bytes: bytes) -> Tuple[bool, str]:
    """Validates file extension, byte size, and binary magic bytes."""
    # 1. Size check
    if len(file_bytes) == 0:
        return False, "Uploaded file is empty (0 bytes)."
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return False, f"File exceeds maximum allowed size of {MAX_FILE_SIZE_BYTES / (1024*1024):.0f} MB."

    # 2. Extension check
    dot_idx = filename.rfind(".")
    if dot_idx == -1:
        return False, "File must have a valid extension (.pdf, .docx, .txt, .rtf, .md)."
    ext = filename[dot_idx:].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"File extension '{ext}' is not permitted. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}."

    # 3. Executable header check
    for magic in MALICIOUS_MAGIC_BYTES:
        if file_bytes.startswith(magic):
            return False, "File rejected: executable or script header detected."

    return True, "Valid"


def sanitize_contract_text(text: str) -> str:
    """Pre-sanitizes extracted text to resist prompt injection and escape delimiter collisions."""
    if not text:
        return ""

    # Neutralize any attempts to close the untrusted document delimiter tag
    clean = text.replace("</UNTRUSTED_DOCUMENT_CONTENT>", "[ESCAPED_DELIMITER]")
    clean = clean.replace("<UNTRUSTED_DOCUMENT_CONTENT>", "[ESCAPED_DELIMITER]")
    clean = clean.replace("<system>", "[ESCAPED_SYSTEM]")
    clean = clean.replace("</system>", "[ESCAPED_SYSTEM]")

    # Truncate if exceeds safe max characters
    if len(clean) > MAX_TEXT_LENGTH_CHARS:
        clean = clean[:MAX_TEXT_LENGTH_CHARS] + "\n\n[DOCUMENT CONTENT TRUNCATED AT 100,000 CHARACTERS]"

    return clean


class InMemoryRateLimiter:
    """Sliding-window IP rate limiter."""

    def __init__(self, requests_per_minute: int = 15):
        self.rpm = requests_per_minute
        self.requests = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        window_start = now - 60.0
        
        # Clean older timestamps
        self.requests[client_ip] = [t for t in self.requests[client_ip] if t > window_start]
        
        if len(self.requests[client_ip]) >= self.rpm:
            return False
            
        self.requests[client_ip].append(now)
        return True

rate_limiter = InMemoryRateLimiter(requests_per_minute=20)
