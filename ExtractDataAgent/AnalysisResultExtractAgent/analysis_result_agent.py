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

        for i in range(len(lines)):
            txt = lines[i]["text"].strip()
            low = norm(txt)

            if not in_section and low == "results":
                in_section = True
                continue

            if in_section:
                if any(w in low for w in STOP_WORDS):
                    return rows

                # اسم مبيد = سطر قبل <LOQ أو رقم
                if i + 1 < len(lines):
                    nxt = lines[i+1]["text"].strip()
                    if nxt.startswith("<") or nxt.replace(".", "").isdigit():
                        rows.append((txt, nxt))

    return rows
