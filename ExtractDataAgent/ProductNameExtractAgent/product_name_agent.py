import json
import re
from pathlib import Path
from typing import Optional
from Config.utils import norm

STOP_LABELS = {
    "number", "total", "weight", "variety", "phone",
    "fax", "protocol", "lot", "analysis", "package"
}


def extract(ocr_dir: Path) -> Optional[str]:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)

        # نشتغل على أول صفحة فقط (الهيدر)
        if data.get("page_number") != 1:
            continue

        text = " ".join(line.get("text", "") for line in data.get("lines", []))
        text = re.sub(r"\s+", " ", text)

        m = re.search(r"\bsample\s*:\s*(.+?)\b(number|total|lot|weight|variety)\b", text, re.I)
        if not m:
            continue

        segment = m.group(1)

        for tok in re.split(r"[^\w]+", segment):
            if tok.isalpha() and len(tok) >= 3:
                return tok.capitalize()

    return None
