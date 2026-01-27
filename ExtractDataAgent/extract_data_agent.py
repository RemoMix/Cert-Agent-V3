from pathlib import Path
from Config.paths import OCR_OUTPUT_DIR, GETCERT_INBOX

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
        OCR_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # -------- STEP 1: OCR PIPELINE (only if JSON not exists) --------
        existing_json = list(OCR_OUTPUT_DIR.glob(f"{pdf_path.stem}_page_*_ocr.json"))

        if existing_json:
            for jf in existing_json:
                warn_overwrite(jf, "re-running ExtractDataAgent on same PDF")
        else:
            images = pdf_to_images(pdf_path, OCR_OUTPUT_DIR)

            for idx, img in enumerate(images, start=1):
                preprocess(img)

                base = OCR_OUTPUT_DIR / f"{pdf_path.stem}_page_{idx}"

                # PNG
                if img.exists():
                    warn_overwrite(img, "image regenerated")

                tsv = run_tesseract(img, base)

                if tsv.exists():
                    warn_overwrite(tsv, "TSV regenerated")

                json_path = OCR_OUTPUT_DIR / f"{pdf_path.stem}_page_{idx}_ocr.json"
                if json_path.exists():
                    warn_overwrite(json_path, "OCR JSON regenerated")

                tsv_to_json(tsv, json_path, idx)


        # -------- STEP 2: EXTRACTION --------
        cert = cert_extract(OCR_OUTPUT_DIR)
        product = product_extract(OCR_OUTPUT_DIR)
        lot = lot_extract(OCR_OUTPUT_DIR)
        lot_size = lot_size_extract(OCR_OUTPUT_DIR)
        analysis = analysis_extract(OCR_OUTPUT_DIR)

        # -------- STEP 3: AGGREGATION --------
        out_csv = aggregate(
            f"{pdf_path.stem}_FINAL.csv",
            cert,
            product,
            lot,
            lot_size,
            analysis
        )


        return out_csv
