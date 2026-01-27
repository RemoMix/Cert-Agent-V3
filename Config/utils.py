def main():
    print("Cert Agent V3 is running")


if __name__ == "__main__":
    main()

def norm(txt: str) -> str:
    return txt.strip().lower()

from pathlib import Path
from datetime import datetime

def warn_overwrite(path: Path, reason: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[WARN {ts}] Overwriting {path.name} | reason: {reason}")
