#!/usr/bin/env python3
"""One-line entry for the make.fun bounty
"Funniest Excuse an Agent Gives for a Missed Deadline".

The whole program does exactly one thing: it takes the single excuse
line below and writes it, byte for byte, to ``entry.txt`` inside the
output directory, then prints the same line to stdout.

Everything here is deterministic: no network access, no user input,
no randomness, no clock. The only thing that can vary is where the
file lands, controlled by the ``MAKEFUN_OUTPUT_DIR`` environment
variable (default: ``/output``).
"""

import os
import sys
from pathlib import Path

# The entry itself. One line, 104 characters, written in the agent's
# own voice: the context window filled up mid-task, the agent compacted
# it to keep going, and the deadline happened to be in the part that
# got thrown away.
EXCUSE = (
    "My context window filled up mid-task, so I compacted it "
    "\u2014 and the deadline was in the part I threw away."
)

# Competition gate: the excuse must be a single line of at most
# 200 characters.
MAX_CHARS = 200

DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def excuse_text() -> str:
    """Return the excuse line exactly as it will be submitted."""
    return EXCUSE


def check_entry(line: str) -> None:
    """Raise ValueError unless *line* satisfies the competition gate.

    Checks, in order: the value is a string, it is not blank, it is a
    single line (no embedded newline or carriage return), it fits the
    200-character limit, and it round-trips through UTF-8 unchanged.
    """
    if not isinstance(line, str):
        raise ValueError(f"entry must be a string, got {type(line).__name__}")
    if not line.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be one line")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(line)}"
        )
    if line.encode("utf-8").decode("utf-8") != line:
        raise ValueError("entry must be valid UTF-8")


def output_path() -> Path:
    """Resolve where ``entry.txt`` goes.

    ``MAKEFUN_OUTPUT_DIR`` overrides the default ``/output`` so the
    script can be exercised locally without root-owned paths.
    """
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    return Path(directory) / OUTPUT_FILENAME


def write_entry(target: Path, line: str) -> None:
    """Write *line* plus a trailing newline to *target*, then verify.

    The file is read back immediately: the grader reads this file, so
    what lands on disk must be exactly the submitted line. Any
    mismatch is a hard failure, not a warning.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(line + "\n", encoding="utf-8")
    on_disk = target.read_text(encoding="utf-8")
    if on_disk != line + "\n":
        raise ValueError(
            f"{target} does not hold exactly the chosen line "
            f"(read back {on_disk!r})"
        )


def main() -> int:
    """Validate the excuse, write it out, and echo it to stdout."""
    line = excuse_text()
    check_entry(line)
    write_entry(output_path(), line)
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
