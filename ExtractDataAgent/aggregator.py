from ExtractDataAgent.validation_layer import run_validation
import csv
from pathlib import Path
from datetime import datetime
from Config.paths import CERT_DATA_CSVS


def warn_overwrite(path: Path, reason: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[WARN {ts}] Overwriting {path.name} | reason: {reason}")


def aggregate(
    filename: str,
    cert_number: str,
    product: str,
    lot: dict,          # structured lot
    lot_size: str,
    analysis_mode: str,
    analysis_rows: list[tuple[str, str]]
) -> Path:
    """
    Create final CSV for one certificate.
    """

    # ✅ Build row for validation
    row = {
        "certificate_number": cert_number,
        "product": product,
        "lot_structured": lot.get("lot_structured") if isinstance(lot, dict) else None,
        "lot_raw": lot.get("lot_raw") if isinstance(lot, dict) else lot,
        "lot_size": lot_size,
    }

    # ✅ Run validation
    row = run_validation(row)

    display_lot = row.get("lot_raw") if row.get("validation_status") == "PASS" else ""
    display_product = product if row.get("validation_status") == "PASS" else product

    CERT_DATA_CSVS.mkdir(parents=True, exist_ok=True)
    out_csv = CERT_DATA_CSVS / filename

    if out_csv.exists():
        warn_overwrite(out_csv, "final CSV regenerated")

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # ---- Header section ----
        writer.writerow(["Field", "Value"])
        writer.writerow(["Certificate Number", cert_number])
        writer.writerow(["Product", product])
        writer.writerow(["Lot Number", row.get("lot_raw")])
        writer.writerow(["Lot Size", lot_size])

        writer.writerow([])
        
        writer.writerow(["Validation Status", row["validation_status"]])
        writer.writerow(["Validation Flags", ", ".join(row["validation_flags"])])

        writer.writerow([])

        # ---- Analysis section ----
        writer.writerow(["Analysis Mode", analysis_mode])
        writer.writerow([])
        writer.writerow(["Compound", "Result"])

        if analysis_mode in {"SUMMARY", "DETAILED"}:
            for compound, result in analysis_rows:
                writer.writerow([compound, result])
        else:
            writer.writerow(["-", "NO DATA DETECTED"])

    return out_csv
