from pathlib import Path
from pdf2image import convert_from_path
from Config.paths import POPPLER_DIR

def pdf_to_images(pdf_path: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(
        pdf_path,
        dpi=300,
        fmt="png",
        poppler_path=str(POPPLER_DIR)
    )

    paths = []
    for i, img in enumerate(images, start=1):
        out = output_dir / f"{pdf_path.stem}_page_{i}.png"
        img.save(out, "PNG")
        paths.append(out)

    return paths
