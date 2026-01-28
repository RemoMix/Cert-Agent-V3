from pathlib import Path
from Config.paths import OCR_OUTPUT_DIR

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
from Config.utils import warn_overwrite


class ExtractDataAgent:

    def run(self, pdf_path: Path):
        """
        Process ONE certificate PDF.
        Safe for batch execution (no shared state).
        """

        # ---- OCR CONTEXT PER CERTIFICATE ----
        cert_ocr_dir = OCR_OUTPUT_DIR / pdf_path.stem
        cert_ocr_dir.mkdir(parents=True, exist_ok=True)

        # -------- STEP 1: OCR PIPELINE --------
        existing_json = list(cert_ocr_dir.glob(f"{pdf_path.stem}_page_*_ocr.json"))

        if existing_json:
            for jf in existing_json:
                warn_overwrite(jf, "re-running ExtractDataAgent on same PDF")
        else:
            images = pdf_to_images(pdf_path, cert_ocr_dir)

            for idx, img in enumerate(images, start=1):
                preprocess(img)

                base = cert_ocr_dir / f"{pdf_path.stem}_page_{idx}"

                if img.exists():
                    warn_overwrite(img, "image regenerated")

                tsv = run_tesseract(img, base)

                if tsv.exists():
                    warn_overwrite(tsv, "TSV regenerated")

                json_path = cert_ocr_dir / f"{pdf_path.stem}_page_{idx}_ocr.json"
                if json_path.exists():
                    warn_overwrite(json_path, "OCR JSON regenerated")

                tsv_to_json(tsv, json_path, idx)

        # -------- STEP 2: EXTRACTION (ISOLATED) --------
        cert = cert_extract(cert_ocr_dir)
        product = product_extract(cert_ocr_dir)
        lot = lot_extract(cert_ocr_dir)
        lot_size = lot_size_extract(cert_ocr_dir)

        analysis_result = analysis_extract(cert_ocr_dir)
        analysis_mode = analysis_result["analysis_mode"]
        analysis_rows = analysis_result["analysis_rows"]

        # -------- STEP 3: AGGREGATION --------
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
