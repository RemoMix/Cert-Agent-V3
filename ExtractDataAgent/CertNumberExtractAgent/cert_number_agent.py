import re
import json
from pathlib import Path
from typing import Optional
from Config.utils import norm

CERT_PATTERN = re.compile(r"\b(dokki|ism)\s*-\s*\d{4,}\b", re.I)
ANCHOR_PATTERN = re.compile(r"\bcertificate\s*number\b", re.I)


def extract(ocr_dir: Path) -> Optional[str]:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        data = json.load(open(jf, encoding="utf-8"))
        lines = data.get("lines", [])

        for i, line in enumerate(lines):
            text = line.get("text", "")
            text_norm = norm(text)

            if ANCHOR_PATTERN.search(text_norm):
                # same line
                match = CERT_PATTERN.search(text)
                if match:
                    return match.group(0).replace(" ", "")

                # next lines fallback
                for j in range(i + 1, min(i + 4, len(lines))):
                    candidate = lines[j].get("text", "")
                    match = CERT_PATTERN.search(candidate)
                    if match:
                        return match.group(0).replace(" ", "")

    return None
