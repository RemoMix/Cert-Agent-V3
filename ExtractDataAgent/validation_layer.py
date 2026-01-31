from typing import Dict, Any, List


def validate_product(product: str) -> bool:
    if not product:
        return False
    if len(product) < 3:
        return False
    if not product.isalpha():
        return False
    return True


def validate_lot(lot_structured: Dict[str, Any]) -> bool:
    if not lot_structured:
        return False

    base = lot_structured.get("base_lot")
    if not base:
        return False

    # reject contaminated OCR strings
    forbidden = ["kg", "weight", "variety", "total", "n/a"]
    for f in forbidden:
        if f in base.lower():
            return False

    return True


def validate_weight(weight: str) -> bool:
    if not weight:
        return False
    if "kg" not in weight.lower():
        return False

    try:
        value = int(weight.lower().replace("kg", "").strip())
        return value > 1
    except ValueError:
        return False


def run_validation(row: Dict[str, Any]) -> Dict[str, Any]:
    flags: List[str] = []

    if not row.get("certificate_number"):
        flags.append("MISSING_CERT_NUMBER")

    if not validate_product(row.get("product")):
        flags.append("INVALID_PRODUCT")

    if not validate_lot(row.get("lot_structured")):
        flags.append("INVALID_LOT")

    if not validate_weight(row.get("lot_size")):
        flags.append("INVALID_WEIGHT")

    row["validation_status"] = "PASS" if not flags else "REVIEW"
    row["validation_flags"] = flags

    return row
