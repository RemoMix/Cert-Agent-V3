import json
import re
from pathlib import Path
from Config.utils import norm


CERT_NUMBER_PATTERN = re.compile(r"dokki-\d{5,7}", re.IGNORECASE)


def normalize_ocr_lines(lines):
    """
    Normalize OCR JSON lines.
    Handles TSV dumps embedded inside line["text"].
    """
    clean = []

    for line in lines:
        txt = line.get("text", "")

        # TSV dump case
        if "\t" in txt:
            rows = txt.split("\n")
            for r in rows:
                parts = r.split("\t")
                if parts:
                    word = parts[-1].strip()
                    if word:
                        clean.append({"text": word})
        else:
            if txt.strip():
                clean.append({"text": txt.strip()})

    return clean


def extract(ocr_dir: Path) -> str:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)

        # 👇 التطبيع هنا
        lines = normalize_ocr_lines(data.get("lines", []))

        for i in range(len(lines) - 4):
            w1 = norm(lines[i]["text"])
            w2 = norm(lines[i + 1]["text"])

            # Anchor: Certificate Number / Certificate No
            if w1 == "certificate" and w2 in {"number", "no"}:
                # دور قدّام على Dokki-xxxx
                for j in range(i + 2, min(i + 8, len(lines))):
                    token = lines[j]["text"]

                    match = CERT_NUMBER_PATTERN.search(token)
                    if match:
                        return match.group(0)

    return ""
