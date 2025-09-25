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
    for i, chunk in enumerate(split_output(result), start=1):
        print(f"\n--- Section {i} ---\n")
        print(chunk)
    if CLIP:
        try:
            pyperclip.copy(result)
            print("\n[Cleaned transcript copied to clipboard]")
        except Exception:
            pass

def split_output(text: str, max_length: int = 10240):
    paragraphs = text.split('\n')
    current_chunk = []
    current_length = 0
    for para in paragraphs:
        para_length = len(para) + 1  # +1 for the newline
        if current_length + para_length > max_length:
            yield '\n'.join(current_chunk).strip()
            current_chunk = [para]
            current_length = para_length
        else:
            current_chunk.append(para)
            current_length += para_length
    if current_chunk:
        yield '\n'.join(current_chunk).strip()

if __name__ == "__main__":
    main()