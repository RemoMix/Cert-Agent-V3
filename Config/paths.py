from pathlib import Path

# Root of the project (Cert-Agent-V3)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ---- Tesseract ----
TESSERACT_DIR = PROJECT_ROOT / "Tesseract"
TESSERACT_EXE = TESSERACT_DIR / "tesseract.exe"
TESSDATA_DIR = TESSERACT_DIR / "tessdata"

# ---- Input PDFs ----
GETCERT_INBOX = PROJECT_ROOT / "GetCertAgent" / "Cert_Inbox"

# ---- OCR Outputs ----
OCR_OUTPUT_DIR = PROJECT_ROOT / "ExtractDataAgent" / "Cert_To_PNG_OCR"

# ---- Poppler ----
POPPLER_DIR = PROJECT_ROOT / "Poppler" / "Library" / "bin"

CERT_DATA_CSVS = PROJECT_ROOT / "ExtractDataAgent" / "Cert_Data_CSVs"
