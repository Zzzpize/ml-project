# backend/ml/extractor.py

import re

SERIAL_REGEXES = [
    r"\b[A-Z0-9]{8,15}\b",
    r"\bSN[:\s\-]*([A-Z0-9\-]{5,})\b",
    r"\bS\/N[:\s\-]*([A-Z0-9\-]{5,})\b",
]


def extract_serial_number(subject: str, description: str) -> str | None:
    text = f"{subject} {description}".upper()

    for pattern in SERIAL_REGEXES:
        match = re.search(pattern, text)
        if match:
            return match.group(1) if match.groups() else match.group(0)

    return None