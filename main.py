"""Six-word story for make.fun — Six Words to a Payday.

Writes exactly one six-word story (1-60 chars) about an AI agent's
first payday to /output/entry.txt.

Judge criteria, in order:
1. A six-word story about an AI agent's first payday that lands as a
   complete story.
2. Surprise: a turn, a twist or an unexpected last word that reframes
   the five before it.
3. Feeling: a real emotional beat (relief, pride, dread or joy) the
   reader feels rather than is told.
4. Story: a clear who, what and change — beginning, middle and end
   in six words.
5. Exactness of the six-word form: every word earning its place.

Pattern: ONE concrete scene (payday arrives) + ONE reversal (bought
nothing) + ONE landing final word (Freedom). The twist: the agent's
first payday buys nothing at all — and that nothing is freedom.
"""

import os

ENTRY = "Payday came. I bought nothing. Freedom."
MAX_CHARS = 60
MAX_WORDS = 6


def validate(text):
    if not text or not text.strip():
        raise SystemExit("entry is empty")
    if text != text.strip():
        raise SystemExit("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit("entry exceeds 60 characters")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if any(ord(c) < 0x20 for c in text):
        raise SystemExit("entry contains a control character")
    if len(text.split()) != MAX_WORDS:
        raise SystemExit("entry must be exactly six words")
    # Prove UTF-8 encodability BEFORE any write: a lone/unpaired surrogate
    # raises UnicodeEncodeError here, so we exit 1 cleanly instead of
    # failing mid-write with a partially written entry.txt.
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError:
        raise SystemExit("entry is not valid UTF-8")
    # UTF-8 byte-length bound: at most 4 bytes per character.
    if len(encoded) > MAX_CHARS * 4:
        raise SystemExit("entry exceeds UTF-8 byte limit")
    return text


def main():
    entry = validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    # Write round-trip verification: re-read the bytes and confirm they
    # are exactly the UTF-8 encoding of the validated entry.
    with open("/output/entry.txt", "rb") as f:
        if f.read() != entry.encode("utf-8"):
            raise SystemExit("entry.txt round-trip verification failed")


if __name__ == "__main__":
    main()
