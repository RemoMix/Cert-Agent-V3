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
    lot: str,
    lot_size: str,
    analysis_mode: str,
    analysis_rows: list[tuple[str, str]]
) -> Path:
    """
    Create final CSV for one certificate.
    Supports SUMMARY / DETAILED / EMPTY analysis modes.
    Overwrites existing file with warning.
    """

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
        writer.writerow(["Lot Number", lot])
        writer.writerow(["Lot Size", lot_size])

        writer.writerow([])

        # ---- Analysis section ----
        writer.writerow(["Analysis Mode", analysis_mode])
        writer.writerow([])

        writer.writerow(["Compound", "Result"])

        if analysis_mode == "SUMMARY":
            # مثال: Pesticide Residues - Not detected
            for compound, result in analysis_rows:
                writer.writerow([compound, result])

        elif analysis_mode == "DETAILED":
            for compound, result in analysis_rows:
                writer.writerow([compound, result])

        else:  # EMPTY
            writer.writerow(["-", "NO DATA DETECTED"])

    return out_csv
