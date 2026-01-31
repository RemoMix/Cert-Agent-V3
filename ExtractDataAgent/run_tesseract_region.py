import cv2
import subprocess
from pathlib import Path
from Config.paths import TESSERACT_EXE, TESSDATA_DIR

def run_tesseract_region(
    image_path: Path,
    crop_ratio: tuple,
    out_base: Path,
    psm: int,
    lang: str,
):
    img = cv2.imread(str(image_path))
    if img is None:
        return None

    h, w = img.shape[:2]
    y1 = int(h * crop_ratio[0])
    y2 = int(h * crop_ratio[1])
    crop = img[y1:y2, :]

    crop_path = out_base.with_suffix(".png")
    cv2.imwrite(str(crop_path), crop)

    cmd = [
        str(TESSERACT_EXE),
        str(crop_path),
        str(out_base),
        "-l", lang,
        "--psm", str(psm),
        "--oem", "1",
        "--tessdata-dir", str(TESSDATA_DIR),
        "-c", "tessedit_create_tsv=1",
        "-c", "preserve_interword_spaces=1",
    ]

    subprocess.run(cmd, check=True)
    return out_base.with_suffix(".tsv")
