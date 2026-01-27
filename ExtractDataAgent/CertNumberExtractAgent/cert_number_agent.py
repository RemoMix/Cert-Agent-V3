import json
from pathlib import Path
from Config.utils import norm

def extract(ocr_dir: Path) -> str:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        data = json.load(open(jf, encoding="utf-8"))
        lines = data["lines"]

        for i in range(len(lines) - 3):
            if (
                norm(lines[i]["text"]) == "certificate" and
                norm(lines[i+1]["text"]) == "number" and
                norm(lines[i+2]["text"]) == ":"
            ):
                return lines[i+3]["text"].strip()

    return ""
