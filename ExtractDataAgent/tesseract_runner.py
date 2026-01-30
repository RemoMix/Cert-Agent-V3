import subprocess
from pathlib import Path
from Config.paths import TESSERACT_EXE, TESSDATA_DIR

def run_tesseract(image_path: Path, out_base: Path, mode: str = "text") -> Path:
    """
    Dual OCR runner:
    - mode='text'  → headers & sentences
    - mode='table' → tables & numbers
    """

    if mode == "text":
        config = [
            "-l", "eng+ara",
            "--psm", "6",
            "--oem", "1",
        ]
        suffix = "_text"

    elif mode == "table":
        config = [
            "-l", "eng",
            "--psm", "11",
            "--oem", "1",
        ]
        suffix = "_table"

    else:
        raise ValueError(f"Unknown OCR mode: {mode}")

    out = out_base.with_name(out_base.name + suffix)
    tsv_path = out.with_suffix(".tsv")

    cmd = [
        str(TESSERACT_EXE),
        str(image_path),
        str(out),
        *config,
        "--tessdata-dir", str(TESSDATA_DIR),
        "-c", "tessedit_create_tsv=1",
        "-c", "preserve_interword_spaces=1",
    ]

    subprocess.run(cmd, check=True)

    if not tsv_path.exists():
        raise RuntimeError(f"Tesseract TSV not found: {tsv_path}")

    return tsv_path
