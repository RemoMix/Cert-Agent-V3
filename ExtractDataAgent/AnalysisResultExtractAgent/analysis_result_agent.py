import json
from pathlib import Path
from Config.utils import norm

START = "results"
STOP_WORDS = ["uncertainty", "person", "thank"]

def extract(ocr_dir: Path) -> list[tuple[str, str]]:
    rows = []
    in_section = False
    pending_compound = None

    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        data = json.load(open(jf, encoding="utf-8"))
        lines = data["lines"]

        for line in lines:
            txt = line["text"].strip()
            low = norm(txt)

            if not in_section and low == "results":
                in_section = True
                continue

            if in_section:
                if any(w in low for w in STOP_WORDS):
                    return rows

                # compound
                if pending_compound is None and txt.isalpha():
                    pending_compound = txt
                    continue

                # result
                if pending_compound:
                    rows.append((pending_compound, txt))
                    pending_compound = None

    return rows
