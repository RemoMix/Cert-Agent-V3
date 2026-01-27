from Config.paths import GETCERT_INBOX
from ExtractDataAgent.extract_data_agent import ExtractDataAgent

if __name__ == "__main__":
    agent = ExtractDataAgent()

    pdfs = list(GETCERT_INBOX.glob("*.pdf"))

    if not pdfs:
        print("No certificates found.")
    else:
        print(f"Processing {len(pdfs)} certificates...\n")

    for pdf in pdfs:
        print(f"→ Processing: {pdf.name}")
        try:
            agent.run(pdf)
        except Exception as e:
            print(f"❌ Failed: {pdf.name} | {e}")
