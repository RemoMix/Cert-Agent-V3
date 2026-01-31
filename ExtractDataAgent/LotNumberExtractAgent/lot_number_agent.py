import json
import re
from pathlib import Path
from typing import Dict, Any, Optional
from Config.utils import norm

STOP_WORDS = {
    "kg", "weight", "variety", "phone", "fax",
    "total", "sample", "analysis"
}

LOT_VALUE = re.compile(r"[A-Z0-9][A-Z0-9\-\/]{2,}", re.I)


def parse_lot(raw: str) -> Dict[str, Any]:
    if "-" in raw and all(p.isdigit() for p in raw.split("-")):
        return {
            "type": "explicit_multi",
            "base_lot": None,
            "count": len(raw.split("-")),
            "expanded_lots": raw.split("-"),
            "annotation_hint": None,
        }

    if "/" in raw and raw.split("/")[0].isdigit() and raw.split("/")[1].isdigit():
        base, cnt = raw.split("/")
        cnt = int(cnt)
        return {
            "type": "implicit_multi",
            "base_lot": base,
            "count": cnt,
            "expanded_lots": [base],
            "annotation_hint": f"+{cnt-1}",
        }

    return {
        "type": "single",
        "base_lot": raw,
        "count": 1,
        "expanded_lots": [raw],
        "annotation_hint": None,
    }


def extract(ocr_dir: Path) -> Optional[Dict[str, Any]]:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)

        text = " ".join(line.get("text", "") for line in data.get("lines", []))
        text = re.sub(r"\s+", " ", text)

        m = re.search(r"\blot\s*number\s*:\s*(.+?)\b(number|total|weight|variety|package|sample)\b", text, re.I)
        if not m:
            continue

        segment = m.group(1)

        for tok in re.split(r"[^\w\/\-]+", segment):
            tok = tok.strip()
            if not tok:
                continue
            if tok.lower() in STOP_WORDS:
                break
            if LOT_VALUE.fullmatch(tok):
                return {
                    "lot_raw": tok,
                    "lot_structured": parse_lot(tok)
                }

    return None
