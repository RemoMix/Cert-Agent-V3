from pathlib import Path
import json

from Config.paths import OCR_OUTPUT_DIR
from Config.utils import safe_slug

from ExtractDataAgent.pdf_to_images import pdf_to_images
from ExtractDataAgent.image_preprocess import preprocess
from ExtractDataAgent.tesseract_runner import run_tesseract
from ExtractDataAgent.ocr_json_builder import tsv_to_json
from ExtractDataAgent.run_tesseract_region import run_tesseract_region

from ExtractDataAgent.CertNumberExtractAgent.cert_number_agent import extract as cert_extract
from ExtractDataAgent.ProductNameExtractAgent.product_name_agent import extract as product_extract
from ExtractDataAgent.LotNumberExtractAgent.lot_number_agent import extract as lot_extract
from ExtractDataAgent.LotSizeExtractAgent.lot_size_agent import extract as lot_size_extract
from ExtractDataAgent.AnalysisResultExtractAgent.analysis_result_agent import extract as analysis_extract

from ExtractDataAgent.aggregator import aggregate


# ================= OCR DEBUG (TXT جنب الشهادة) =================
def dump_ocr_full_text(cert_ocr_dir: Path, cert_name: str):
    out_path = cert_ocr_dir / f"{cert_name}_ocr.txt"

    seen = set()
    lines_out = []

    for jf in sorted(cert_ocr_dir.glob("*_ocr.json")):
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)

        page = data.get("page_number", "?")
        lines_out.append(f"\n=== PAGE {page} ===\n")

        for line in data.get("lines", []):
            txt = line.get("text", "")
            if not txt:
                continue
            key = txt.strip().lower()
            if key in seen:
                continue
            seen.add(key)
            lines_out.append(txt)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out))


# ================= COVERAGE GATE =================
def ocr_coverage_gate(cert_ocr_dir: Path, cert_name: str):
    full_text = []

    for jf in cert_ocr_dir.glob("*_ocr.json"):
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)
        for line in data.get("lines", []):
            txt = line.get("text", "")
            if txt:
                full_text.append(txt.lower())

    text = " ".join(full_text)

    CORE = {
        "certificate_number": ["certificate number", "cert number", "certificate no", "cert no"],
        "sample_product": ["sample", "product"],
        "lot_number": ["lot number", "lot no"],
        "analysis": ["results of analysis", "analysis results", "results"]
    }

    missing = []
    for field, keys in CORE.items():
        if not any(k in text for k in keys):
            missing.append(field)

    status = "PASS" if not missing else "FAIL"

    coverage = {
        "certificate": cert_name,
        "status": status,
        "missing_fields": missing
    }

    with open(cert_ocr_dir / "ocr_coverage.json", "w", encoding="utf-8") as f:
        json.dump(coverage, f, ensure_ascii=False, indent=2)

    return status, missing


# ================= SMART RETRY =================
def smart_ocr_retry(images, cert_ocr_dir, pdf_stem, missing_fields):
    for idx, img_path in enumerate(images, start=1):

        if "certificate_number" in missing_fields:
            tsv = run_tesseract_region(
                img_path,
                crop_ratio=(0.0, 0.25),
                out_base=cert_ocr_dir / f"{pdf_stem}_page_{idx}_retry_cert",
                psm=6,
                lang="eng+ara",
            )
            if tsv:
                tsv_to_json(tsv, cert_ocr_dir / f"{pdf_stem}_page_{idx}_retry_cert.json", idx)

        if "lot_number" in missing_fields:
            tsv = run_tesseract_region(
                img_path,
                crop_ratio=(0.3, 0.7),
                out_base=cert_ocr_dir / f"{pdf_stem}_page_{idx}_retry_lot",
                psm=11,
                lang="eng",
            )
            if tsv:
                tsv_to_json(tsv, cert_ocr_dir / f"{pdf_stem}_page_{idx}_retry_lot.json", idx)

        if "analysis" in missing_fields:
            tsv = run_tesseract_region(
                img_path,
                crop_ratio=(0.5, 1.0),
                out_base=cert_ocr_dir / f"{pdf_stem}_page_{idx}_retry_analysis",
                psm=11,
                lang="eng",
            )
            if tsv:
                tsv_to_json(tsv, cert_ocr_dir / f"{pdf_stem}_page_{idx}_retry_analysis.json", idx)


# ================= MERGE =================
def merge_all_ocr_json(cert_ocr_dir, pdf_stem, page_num):
    lines = []

    for jf in cert_ocr_dir.glob(f"{pdf_stem}_page_{page_num}*.json"):
        if jf.name.endswith("_ocr.json"):
            continue
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)
        lines.extend(data.get("lines", []))

    out = cert_ocr_dir / f"{pdf_stem}_page_{page_num}_ocr.json"
    json.dump(
        {"page_number": page_num, "lines": lines},
        open(out, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2
    )


# ================= MAIN AGENT =================
class ExtractDataAgent:

    def _extract_only(self, pdf_path, cert_ocr_dir):
        cert = cert_extract(cert_ocr_dir)
        product = product_extract(cert_ocr_dir)
        lot = lot_extract(cert_ocr_dir)
        lot_size = lot_size_extract(cert_ocr_dir)

        analysis_result = analysis_extract(cert_ocr_dir)
        analysis_mode = analysis_result["analysis_mode"]
        analysis_rows = analysis_result["analysis_rows"]

        return aggregate(
            f"{pdf_path.stem}_FINAL.csv",
            cert,
            product,
            lot,
            lot_size,
            analysis_mode,
            analysis_rows
        )

    def run(self, pdf_path: Path):

        safe_name = safe_slug(pdf_path.stem)
        cert_ocr_dir = OCR_OUTPUT_DIR / safe_name
        cert_ocr_dir.mkdir(parents=True, exist_ok=True)

        # ---------- SKIP GATE ----------
        coverage_file = cert_ocr_dir / "ocr_coverage.json"
        if coverage_file.exists():
            with open(coverage_file, encoding="utf-8") as f:
                coverage = json.load(f)

            if coverage.get("status") == "PASS":
                print(f"[SKIP OCR] {safe_name} already PASS")
                return self._extract_only(pdf_path, cert_ocr_dir)

        # ---------- OCR ----------
        images = pdf_to_images(pdf_path, cert_ocr_dir)

        for idx, img in enumerate(images, start=1):
            preprocess(img)
            base = cert_ocr_dir / f"{pdf_path.stem}_page_{idx}"

            tsv_text = run_tesseract(img, base, mode="text")
            tsv_table = run_tesseract(img, base, mode="table")

            tsv_to_json(tsv_text, cert_ocr_dir / f"{pdf_path.stem}_page_{idx}_text_ocr.json", idx)
            tsv_to_json(tsv_table, cert_ocr_dir / f"{pdf_path.stem}_page_{idx}_table_ocr.json", idx)

            merge_all_ocr_json(cert_ocr_dir, pdf_path.stem, idx)

        dump_ocr_full_text(cert_ocr_dir, safe_name)

        status, missing = ocr_coverage_gate(cert_ocr_dir, safe_name)

        if status == "FAIL":
            smart_ocr_retry(images, cert_ocr_dir, pdf_path.stem, missing)

            for i in range(1, len(images) + 1):
                merge_all_ocr_json(cert_ocr_dir, pdf_path.stem, i)

            dump_ocr_full_text(cert_ocr_dir, safe_name)
            status, missing = ocr_coverage_gate(cert_ocr_dir, safe_name)

            if status == "FAIL":
                return {
                    "status": "OCR_FINAL_FAIL",
                    "missing_fields": missing
                }

        return self._extract_only(pdf_path, cert_ocr_dir)
