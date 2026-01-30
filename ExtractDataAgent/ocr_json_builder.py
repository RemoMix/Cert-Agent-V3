import csv
import json
from pathlib import Path


def tsv_to_json(tsv_path: Path, json_path: Path, page_number: int):
    """
    SAFE TSV → OCR JSON converter

    Rules:
    - Preserve RAW OCR text (no normalization, no correction)
    - Parse TSV by level (word-level aggregation)
    - Prevent embedded TSV dumps inside text field
    - Preserve original JSON contract used by Extract Agents
    """

    lines = []

    with open(tsv_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")

        current_line_id = None
        current_words = []
        current_bbox = [float("inf"), float("inf"), 0, 0]

        for row in reader:
            # TSV rows must have at least 12 columns
            if len(row) < 12:
                continue

            try:
                level = int(row[0])
                line_num = int(row[4])
                left = int(row[6])
                top = int(row[7])
                width = int(row[8])
                height = int(row[9])
                text = row[11].strip()
            except (ValueError, IndexError):
                continue

            # ---- WORD LEVEL (level 5) ----
            if level == 5 and text:
                # 🟢 prevent TSV dump embedded inside text
                if "\t" in text:
                    text = text.split("\t")[-1].strip()
                    if not text:
                        continue

                # new line detected → flush previous
                if current_line_id is not None and line_num != current_line_id:
                    if current_words:
                        lines.append({
                            "line_index": len(lines),
                            "text": " ".join(current_words),
                            "bbox": current_bbox.copy()
                        })

                    current_words = []
                    current_bbox = [float("inf"), float("inf"), 0, 0]

                current_line_id = line_num

                # update bbox
                x1 = left
                y1 = top
                x2 = left + width
                y2 = top + height

                current_bbox[0] = min(current_bbox[0], x1)
                current_bbox[1] = min(current_bbox[1], y1)
                current_bbox[2] = max(current_bbox[2], x2)
                current_bbox[3] = max(current_bbox[3], y2)

                current_words.append(text)

        # flush last line
        if current_words:
            lines.append({
                "line_index": len(lines),
                "text": " ".join(current_words),
                "bbox": current_bbox.copy()
            })

    data = {
        "page_number": page_number,
        "lines": lines
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
