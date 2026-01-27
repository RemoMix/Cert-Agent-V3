import json
from pathlib import Path
from Config.utils import norm

WINDOW = 25  # مساحة كفاية للأرقام المتكسرة

def extract(ocr_dir: Path) -> str:
    for jf in sorted(ocr_dir.glob("*_ocr.json")):
        data = json.load(open(jf, encoding="utf-8"))
        lines = data["lines"]

        for i in range(len(lines) - 2):
            # Anchor: Lot Size :
            if (
                norm(lines[i]["text"]) == "lot" and
                norm(lines[i+1]["text"]) == "size" and
                norm(lines[i+2]["text"]) == ":"
            ):
                digits = []

                for j in range(i+3, min(i+3+WINDOW, len(lines))):
                    txt = lines[j]["text"].strip()

                    # لو وصلنا للوحدة Kg → نقف
                    if txt.lower() == "kg":
                        if digits:
                            return f"{''.join(digits)} Kg"
                        break

                    # لو token رقم → خزنه
                    if txt.isdigit():
                        digits.append(txt)
                        continue

                    # تجاهل كلمات زي Total
                    if txt.lower() in ("total", "weight"):
                        continue

                    # أي حاجة تانية تكسر التسلسل
                    if digits:
                        break

    return ""
