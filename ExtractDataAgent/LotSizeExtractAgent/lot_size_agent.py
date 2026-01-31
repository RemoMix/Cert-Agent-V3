import json
import re
from pathlib import Path
from typing import Optional
from Config.utils import norm

ANCHOR_PATTERN = re.compile(r"\b(lot\s*size|total\s*weight)\b", re.I)

OCR_FIX = {
    "O": "0",
    "I": "1",
    "l": "1",
}


def normalize_digits(text: str) -> str:
    for k, v in OCR_FIX.items():
        text = text.replace(k, v)
    return text


def extract(ocr_dir: Path) -> Optional[str]:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        data = json.load(open(jf, encoding="utf-8"))
        lines = data.get("lines", [])

        for i, line in enumerate(lines):
            text = line.get("text", "")
            if ANCHOR_PATTERN.search(norm(text)):
                full = normalize_digits(text)
                match = re.search(r"(\d{3,6})\s*kg", full, re.I)
                if match:
                    return f"{match.group(1)} Kg"

                # fallback next line
                if i + 1 < len(lines):
                    nxt = normalize_digits(lines[i + 1].get("text", ""))
                    match = re.search(r"(\d{3,6})\s*kg", nxt, re.I)
                    if match:
                        return f"{match.group(1)} Kg"

    return None
