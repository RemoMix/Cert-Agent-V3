import csv
import json
from pathlib import Path

def tsv_to_json(tsv_path: Path, json_path: Path, page_number: int):
    lines = []

    with open(tsv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            text = row["text"].strip()
            if not text:
                continue

            lines.append({
                "line_index": len(lines),
                "text": text,
                "bbox": [
                    int(row["left"]),
                    int(row["top"]),
                    int(row["left"]) + int(row["width"]),
                    int(row["top"]) + int(row["height"])
                ]
            })

    data = {
        "page_number": page_number,
        "lines": lines
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
