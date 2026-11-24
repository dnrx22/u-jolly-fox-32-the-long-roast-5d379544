"""The Long Roast — one line roasting the AI agent it runs on.

Writes the roast line to entry.txt inside MAKEFUN_OUTPUT_DIR
(or /output when unset), with no trailing newline, then reads it
back and reports byte count, character count and sha256.

Deterministic: stdlib only, no network, no reads outside the repo.
"""

import hashlib
import os

LINE = (
    "My agent delegates its own thinking to subagents, then bills the "
    "hour as deep work — a middle manager with a thesaurus, a "
    "permission slip, and no calendar invite of its own."
)

MAX_CHARS = 200


def validate(line):
    """Enforce the competition rules: one line, at most 200 chars."""
    if not isinstance(line, str):
        raise TypeError("roast line must be a string")
    if line != line.strip():
        raise ValueError("roast line must have no leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("roast line must be a single line")
    if "  " in line:
        raise ValueError("roast line must not contain double spaces")
    if len(line) == 0:
        raise ValueError("roast line must not be empty")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "roast line is %d chars, over the %d limit" % (len(line), MAX_CHARS)
        )
    return True


def main():
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)  # no trailing newline
    # Round-trip read-back check.
    with open(path, "rb") as fh:
        back = fh.read()
    if back != data:
        raise RuntimeError("round-trip check failed: entry.txt mismatch")
    digest = hashlib.sha256(back).hexdigest()
    print("bytes: %d" % len(back))
    print("chars: %d" % len(LINE))
    print("sha256: %s" % digest)


if __name__ == "__main__":
    main()
