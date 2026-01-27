import subprocess
from pathlib import Path
from Config.paths import TESSERACT_EXE, TESSDATA_DIR

def run_tesseract(image_path: Path, out_base: Path) -> Path:
    """
    Runs Tesseract and forces TSV output using config flag
    (robust on Windows, avoids legacy 'tsv' parsing issues)
    """
    tsv_path = out_base.with_suffix(".tsv")

    cmd = [
        str(TESSERACT_EXE),
        str(image_path),
        str(out_base),
        "-l", "eng+ara",
        "--psm", "6",
        "--oem", "1",
        "--tessdata-dir", str(TESSDATA_DIR),
        "-c", "tessedit_create_tsv=1",
        "-c", "preserve_interword_spaces=1",
    ]

    subprocess.run(cmd, check=True)

    if not tsv_path.exists():
        raise RuntimeError(
            f"Tesseract finished but TSV not found: {tsv_path}"
        )

    return tsv_path
