import re
from typing import Optional


SERIAL_REGEXES = [
    r"\bSN[:\s\-]*([A-Z0-9\-]{5,})\b",
    r"\bсерийн(?:ый|ого)?\s*номер[:\s\-]*([A-Z0-9\-]{5,})\b",
    r"\b([A-Z]{2,5}\d{4,})\b"
]


def extract_serial_number(text: str) -> Optional[str]:
    if not text:
        return None

    for pattern in SERIAL_REGEXES:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)

    return None