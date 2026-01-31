import json
from pathlib import Path
from Config.paths import OCR_OUTPUT_DIR

def generate_coverage_report():
    report = {
        "total_certificates": 0,
        "pass": 0,
        "fail": 0,
        "failed_certificates": [],
        "missing_field_stats": {}
    }

    for cert_dir in OCR_OUTPUT_DIR.iterdir():
        if not cert_dir.is_dir():
            continue

        coverage_file = cert_dir / "ocr_coverage.json"
        if not coverage_file.exists():
            continue

        with open(coverage_file, encoding="utf-8") as f:
            data = json.load(f)

        report["total_certificates"] += 1

        if data["status"] == "PASS":
            report["pass"] += 1
        else:
            report["fail"] += 1
            report["failed_certificates"].append({
                "certificate": data["certificate"],
                "missing_fields": data["missing_fields"]
            })

            for field in data["missing_fields"]:
                report["missing_field_stats"][field] = (
                    report["missing_field_stats"].get(field, 0) + 1
                )

    out_dir = OCR_OUTPUT_DIR / "OCR_Text"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "ocr_coverage_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[OK] Coverage report generated: {out_path}")
