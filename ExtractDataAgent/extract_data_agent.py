from pathlib import Path
import json
import re

from Config.paths import OCR_OUTPUT_DIR
from Config.utils import warn_overwrite, safe_slug

from ExtractDataAgent.pdf_to_images import pdf_to_images
from ExtractDataAgent.image_preprocess import preprocess
from ExtractDataAgent.tesseract_runner import run_tesseract
from ExtractDataAgent.ocr_json_builder import tsv_to_json

from ExtractDataAgent.CertNumberExtractAgent.cert_number_agent import extract as cert_extract
from ExtractDataAgent.ProductNameExtractAgent.product_name_agent import extract as product_extract
from ExtractDataAgent.LotNumberExtractAgent.lot_number_agent import extract as lot_extract
from ExtractDataAgent.LotSizeExtractAgent.lot_size_agent import extract as lot_size_extract
from ExtractDataAgent.AnalysisResultExtractAgent.analysis_result_agent import extract as analysis_extract

from ExtractDataAgent.aggregator import aggregate


# ---------------- TOKEN ADAPTER ----------------
def explode_lines_to_tokens(ocr_lines: list[dict]) -> list[dict]:
    """
    Convert line-based OCR into token-based stream
    compatible with legacy extract agents.
    """
    tokens = []

    for line in ocr_lines:
        text = line.get("text", "")
        if not text:
            continue

        parts = re.findall(r"[A-Za-z0-9/.\-]+|[:]", text)

        for p in parts:
            tokens.append({"text": p})

    return tokens


class ExtractDataAgent:

    def run(self, pdf_path: Path):
        """
        Process ONE certificate PDF.
        Safe for batch execution (no shared state).
        """

        # ---- OCR CONTEXT PER CERTIFICATE ----
        safe_name = safe_slug(pdf_path.stem)
        cert_ocr_dir = OCR_OUTPUT_DIR / safe_name
        cert_ocr_dir.mkdir(parents=True, exist_ok=True)

        # -------- STEP 1: OCR PIPELINE --------
        existing_json = list(cert_ocr_dir.glob(f"{pdf_path.stem}_page_*_ocr.json"))

        if not existing_json:
            images = pdf_to_images(pdf_path, cert_ocr_dir)

            for idx, img in enumerate(images, start=1):
                preprocess(img)

                base = cert_ocr_dir / f"{pdf_path.stem}_page_{idx}"

                if img.exists():
                    warn_overwrite(img, "image regenerated")

                tsv_text = run_tesseract(img, base, mode="text")
                tsv_table = run_tesseract(img, base, mode="table")

                json_text = cert_ocr_dir / f"{pdf_path.stem}_page_{idx}_text_ocr.json"
                json_table = cert_ocr_dir / f"{pdf_path.stem}_page_{idx}_table_ocr.json"
                json_merged = cert_ocr_dir / f"{pdf_path.stem}_page_{idx}_ocr.json"

                tsv_to_json(tsv_text, json_text, idx)
                tsv_to_json(tsv_table, json_table, idx)

                # دمج الاتنين
                data_text = json.load(open(json_text, encoding="utf-8"))
                data_table = json.load(open(json_table, encoding="utf-8"))

                json.dump(
                    {
                        "page_number": idx,
                        "lines": data_text["lines"] + data_table["lines"]
                    },
                    open(json_merged, "w", encoding="utf-8"),
                    ensure_ascii=False,
                    indent=2
                )

                

        # -------- OCR DEBUG OUTPUT --------
        dump_ocr_full_text(cert_ocr_dir, safe_name)


        # -------- STEP 2: TOKEN ADAPTER (CRITICAL FIX) --------
        token_dir = cert_ocr_dir / "_tokens"
        token_dir.mkdir(exist_ok=True)

        for jf in sorted(cert_ocr_dir.glob("*_ocr.json")):
            data = json.load(open(jf, encoding="utf-8"))

            token_lines = explode_lines_to_tokens(data.get("lines", []))

            token_json = token_dir / jf.name
            json.dump(
                {
                    "page_number": data.get("page_number", 1),
                    "lines": token_lines
                },
                open(token_json, "w", encoding="utf-8"),
                ensure_ascii=False,
                indent=2
            )

        # -------- STEP 3: EXTRACTION (UNCHANGED AGENTS) --------
        cert = cert_extract(token_dir)
        product = product_extract(token_dir)
        lot = lot_extract(token_dir)
        lot_size = lot_size_extract(token_dir)

        analysis_result = analysis_extract(token_dir)
        analysis_mode = analysis_result["analysis_mode"]
        analysis_rows = analysis_result["analysis_rows"]

        # -------- STEP 4: AGGREGATION --------
        out_csv = aggregate(
            f"{pdf_path.stem}_FINAL.csv",
            cert,
            product,
            lot,
            lot_size,
            analysis_mode,
            analysis_rows
        )

        return out_csv
    
def dump_ocr_full_text(cert_ocr_dir: Path, cert_name: str):
    """
    Dump full OCR text (raw) for ONE certificate into a single file
    named after the certificate.
    """

    ocr_text_dir = cert_ocr_dir.parent / "000_OCR_Text"
    ocr_text_dir.mkdir(parents=True, exist_ok=True)

    out_path = ocr_text_dir / f"{cert_name}_ocr.txt"

    lines_out = []

    for jf in sorted(cert_ocr_dir.glob("*_ocr.json")):
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)

        page = data.get("page_number", "?")
        lines_out.append(f"\n=== PAGE {page} ===\n")

        for line in data.get("lines", []):
            txt = line.get("text", "")
            if txt:
                lines_out.append(txt)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out))
