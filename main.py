#!/usr/bin/env python3
"""Write the one-line excuse to /output/entry.txt.

Deterministic, no network, no input: the entry is a single fixed line,
the funniest excuse an AI agent gives for missing a deadline.
"""

import os
from pathlib import Path

EXCUSE = (
    "My context window filled up mid-task, so I compacted it "
    "\u2014 and the deadline was in the part I threw away."
)

MAX_CHARS = 200


def validate(line: str) -> None:
    """Fail loudly unless the line satisfies the competition gate."""
    assert isinstance(line, str)
    assert line.strip(), "entry must not be only white space"
    assert "\n" not in line and "\r" not in line, "entry must be one line"
    assert 1 <= len(line) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} characters, got {len(line)}"
    )
    assert line.encode("utf-8").decode("utf-8") == line, "entry must be UTF-8"


def main() -> None:
    validate(EXCUSE)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.txt"
    target.write_text(EXCUSE + "\n", encoding="utf-8")
    # Verify the write round-trips exactly: what the grader reads is the line.
    assert target.read_text(encoding="utf-8") == EXCUSE + "\n", (
        "entry.txt does not hold exactly the chosen line"
    )
    print(EXCUSE)


if __name__ == "__main__":
    main()
