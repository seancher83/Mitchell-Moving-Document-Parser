#!/usr/bin/env python3
"""
GBL Parser - Wrapper script to run the parser with proper imports.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Now import and run main
from main import main

if __name__ == "__main__":
    sys.exit(main())
