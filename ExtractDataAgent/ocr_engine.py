from ExtractDataAgent.ocr_package import OCRLine, OCRPage
from pathlib import Path


def run_ocr(image_paths: list[Path]) -> list[OCRPage]:
    pages = []

    for idx, _ in enumerate(image_paths, start=1):
        pages.append(
            OCRPage(
                page_number=idx,
                lines=[
                    OCRLine(
                        text="Certificate Number : Dokki-281098",
                        line_index=0
                    ),
                    OCRLine(
                        text="Sample : Fennel",
                        line_index=1
                    ),
                    OCRLine(
                        text="Lot number : 139911",
                        line_index=2
                    )
                ]
            )
        )

    return pages