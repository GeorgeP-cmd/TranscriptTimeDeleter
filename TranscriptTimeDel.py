#!/usr/bin/env python3
import re
import sys

# Optional clipboard support
try:
    import pyperclip
    CLIP = True
except Exception:
    CLIP = False

# Regex matches MM:SS, M:SS, H:MM:SS, optional surrounding [] or (), optional trailing separators
TIMESTAMP_RE = re.compile(
    r'[\[\(]?\s*(?:\d{1,2}:){1,2}\d{1,2}\s*[\]\)]?'
    r'(?:[ \t]*[-–—:]+[ \t]*)?'
)

def remove_timestamps(text: str) -> str:
    cleaned = TIMESTAMP_RE.sub(' ', text)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    cleaned = re.sub(r'^[ \t]+', '', cleaned, flags=re.MULTILINE)
    return cleaned.strip()

def read_pasted_input() -> str:
    prompt = "Paste transcript text, then press Ctrl-D (Linux/Mac) or Ctrl-Z then Enter (Windows) to finish:\n"
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.read()

def main():
    raw = read_pasted_input()
    if not raw.strip():
        print("No input received.")
        return
    result = remove_timestamps(raw)
    print("\n--- Cleaned transcript ---\n")
    print(result)
    if CLIP:
        try:
            pyperclip.copy(result)
            print("\n[Cleaned transcript copied to clipboard]")
        except Exception:
            pass

if __name__ == "__main__":
    main()