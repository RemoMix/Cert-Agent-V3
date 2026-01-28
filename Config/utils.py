def main():
    print("Cert Agent V3 is running")


if __name__ == "__main__":
    main()

def norm(txt: str) -> str:
    return txt.strip().lower()

from pathlib import Path
from datetime import datetime

def warn_overwrite(path: Path, reason: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[WARN {ts}] Overwriting {path.name} | reason: {reason}")

def normalize_ocr_lines(lines):
    """
    Fix cases where OCR JSON line contains TSV dump.
    Returns a clean list of {'text': str}
    """
    clean = []

    for line in lines:
        txt = line.get("text", "")

        # حالة TSV dump
        if "\t" in txt:
            rows = txt.split("\n")
            for r in rows:
                parts = r.split("\t")
                if parts:
                    word = parts[-1].strip()
                    if word:
                        clean.append({"text": word})
        else:
            clean.append({"text": txt})

    return clean

import re

def safe_slug(text: str) -> str:
    """
    Convert any filename to safe ASCII slug for filesystem usage
    """
    text = re.sub(r"[^\w\-]+", "_", text, flags=re.ASCII)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")
