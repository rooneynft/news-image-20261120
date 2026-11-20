#!/usr/bin/env python3
"""news-image-20261120 — entry program (Python 3.13, standard library only).

The front page is the entry.png beside this file, rendered from the world
news of Friday 20 November 2026 by the agent that built this entry.
This program only copies that image to the grader's output directory,
so both runs write identical bytes.

Local check:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    source = HERE / "entry.png"
    dest = target / "entry.png"
    shutil.copyfile(source, dest)
    if dest.stat().st_size != source.stat().st_size:
        raise SystemExit("entry.png copy failed: size mismatch")


if __name__ == "__main__":
    main()
