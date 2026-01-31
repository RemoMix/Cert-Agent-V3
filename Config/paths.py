from pathlib import Path

# Root of the project (Cert-Agent-V3)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ---- Tesseract ----
TESSERACT_DIR = PROJECT_ROOT / "Tesseract"
TESSERACT_EXE = TESSERACT_DIR / "tesseract.exe"
TESSDATA_DIR = TESSERACT_DIR / "tessdata"

# ---- Poppler ----
POPPLER_DIR = PROJECT_ROOT / "Poppler" / "Library" / "bin"

#GetCertAgent folders
# Folder for saved emails
MY_EMAILS_FOLDER = PROJECT_ROOT / "GetCertAgent" / "MyEmails"
# ---- Input PDFs ----
GETCERT_INBOX = PROJECT_ROOT / "GetCertAgent" / "Cert_Inbox"

#ExtractDataAgent folders
# ---- OCR Outputs ----
OCR_OUTPUT_DIR = PROJECT_ROOT / "ExtractDataAgent" / "Cert_To_PNG_OCR"
# ---- Data CSVs Outputs ----
CERT_DATA_CSVS = PROJECT_ROOT / "ExtractDataAgent" / "Cert_Data_CSVs"
