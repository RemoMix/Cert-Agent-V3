import json
import re
from pathlib import Path
from Config.utils import norm


FORBIDDEN_WORDS = {
    "id", "na", "nva", "n/a",
    "total", "weight",
    "sample", "fax", "phone",
    "variety", "customer", "address",
    "protocol", "number", "lot", "size",
    "sampling", "analysis", "method", "date"
}

SKIP_TOKENS = {":", "~", "=", ".", "::", "-", "_", "~~", "©.", "©"}


def is_valid_product_word(word: str) -> bool:
    if not word:
        return False
    if not re.fullmatch(r"[A-Za-z]+", word):
        return False
    if len(word) < 3:
        return False
    if not word[0].isupper():
        return False
    if norm(word) in FORBIDDEN_WORDS:
        return False
    return True


def normalize_ocr_lines(lines):
    clean = []
    for line in lines:
        txt = line.get("text", "")
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
    candidates = []

    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)

        lines = normalize_ocr_lines(data.get("lines", []))

        i = 0
        while i < len(lines):
            raw = lines[i]["text"]
            clean = norm(raw).replace(".", "").replace(":", "")

            # Anchor: Sample (لكن مش Sample ID)
            if clean.startswith("sample") and "id" not in clean:
                j = i + 1

                # تخطي الرموز (- : = ...)
                while j < len(lines):
                    t = norm(lines[j]["text"])
                    if t in SKIP_TOKENS or not t:
                        j += 1
                        continue
                    break

                words = []
                while j < len(lines) and len(words) < 2:
                    token = lines[j]["text"].strip()
                    if is_valid_product_word(token):
                        words.append(token)
                        j += 1
                        continue
                    break

                if words:
                    candidates.append(" ".join(words))

            i += 1

    # ✅ نرجّع آخر Sample صالح
    if candidates:
        return candidates[-1]

    return ""
