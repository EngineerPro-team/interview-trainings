#!/usr/bin/env python3
"""DEPRECATED — no-op.

The System Design v2 chapters are original, hand-authored HTML (EN + VI) under
src/assets/content/system-design/{en,vi}/<slug>.html with original Mermaid
diagrams, and the manifest src/assets/system-design-data.js is hand-maintained.

There is no external markdown source and no generator. This file is intentionally
a no-op so it can never regenerate or overwrite the hand-maintained manifest.
Edit the content files and the manifest directly.
"""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "[build_system_design] DEPRECATED no-op. v2 chapters are hand-authored HTML;\n"
        "  edit src/assets/content/system-design/{en,vi}/<slug>.html and the manifest\n"
        "  src/assets/system-design-data.js directly. Nothing to generate.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
