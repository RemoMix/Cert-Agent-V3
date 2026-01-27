from pathlib import Path
from Config.paths import GETCERT_INBOX
from ExtractDataAgent.extract_data_agent import ExtractDataAgent

if __name__ == "__main__":
    pdf = GETCERT_INBOX / "Anise 139385.pdf"
    ExtractDataAgent().run(pdf)
    print("OCR DONE")
