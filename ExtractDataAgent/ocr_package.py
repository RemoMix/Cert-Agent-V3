from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import json
from pathlib import Path

@dataclass
class OCRLine:
    text: str
    line_index: int
    bbox: Dict[str, Any] | None = None

@dataclass
class OCRPage:
    page_number: int
    lines: List[OCRLine]

    def to_json(self, path: Path):
        data = {
            "page_number": self.page_number,
            "lines": [
                {
                    "line_index": l.line_index,
                    "text": l.text,
                    "bbox": l.bbox
                }
                for l in self.lines
            ]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
