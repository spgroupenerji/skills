#!/usr/bin/env python3
"""sp-gorsel-tedarik giriş noktası."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tedarik.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
