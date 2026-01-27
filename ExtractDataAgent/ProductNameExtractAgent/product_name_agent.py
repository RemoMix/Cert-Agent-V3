import json
from pathlib import Path
from Config.utils import norm

def extract(ocr_dir: Path) -> str:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        data = json.load(open(jf, encoding="utf-8"))
        lines = data["lines"]

        for i in range(len(lines) - 2):
            if (
                norm(lines[i]["text"]) == "sample" and
                norm(lines[i+1]["text"]) == ":"
            ):
                value = lines[i+2]["text"].strip()

                # تجاهل Sample ID
                if "dokki" in value.lower():
                    continue

                return value

    return ""
