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
    analysis: list[tuple[str, str]]
) -> Path:
    """
    Create final CSV for one certificate.
    Overwrites existing file with warning.
    """

    # ensure output directory exists
    CERT_DATA_CSVS.mkdir(parents=True, exist_ok=True)
    out_csv = CERT_DATA_CSVS / filename

    # overwrite warning
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

        # blank line
        writer.writerow([])

        # ---- Results table ----
        writer.writerow(["Compound", "Result"])
        for compound, result in analysis:
            writer.writerow([compound, result])

    return out_csv
