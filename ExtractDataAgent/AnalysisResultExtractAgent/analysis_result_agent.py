import json
from pathlib import Path
from Config.utils import norm


SUMMARY_KEYWORDS = [
    "pesticide residues",
    "pesticide residue",
]

SUMMARY_VALUES = [
    "not detected",
    "nd",
]

STOP_WORDS = [
    "uncertainty",
    "person",
    "charge",
    "signature",
    "thank",
]

def extract(ocr_dir: Path):
    """
    Returns:
      analysis_mode: 'SUMMARY' | 'DETAILED' | 'EMPTY'
      analysis_rows: list of (compound, result)
    """

    rows = []
    in_results_section = False

    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        data = json.load(open(jf, encoding="utf-8"))
        lines = data["lines"]

        # -------- PASS 1: detect SUMMARY --------
        for i in range(len(lines) - 1):
            left = norm(lines[i]["text"])
            right = norm(lines[i + 1]["text"])

            if any(k in left for k in SUMMARY_KEYWORDS) and any(v in right for v in SUMMARY_VALUES):
                return {
                    "analysis_mode": "SUMMARY",
                    "analysis_rows": [("Pesticide Residues", "Not detected")]
                }

        # -------- PASS 2: detect DETAILED TABLE --------
        pending_compound = None

        for i in range(len(lines)):
            txt = lines[i]["text"].strip()
            low = norm(txt)

            if any(sw in low for sw in STOP_WORDS):
                break

            # compound line
            if pending_compound is None:
                # اسم مبيد غالبًا كلمة واحدة أو اتنين
                if txt.isalpha() and len(txt) > 3:
                    pending_compound = txt
                continue

            # result line
            if pending_compound:
                if txt.startswith("<") or txt.lower() in ("nd", "not detected"):
                    rows.append((pending_compound, txt))
                    pending_compound = None
                elif txt.replace(".", "").isdigit():
                    rows.append((pending_compound, txt))
                    pending_compound = None
                else:
                    pending_compound = None

    if rows:
        return {
            "analysis_mode": "DETAILED",
            "analysis_rows": rows
        }

    return {
        "analysis_mode": "EMPTY",
        "analysis_rows": []
    }
