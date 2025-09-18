#!/usr/bin/env python3
"""
Slack Canvas to Markdown Exporter

Direct execution script for exporting Slack canvases to markdown files.
"""

import sys
import os
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from slack_canvas_export.cli import main

if __name__ == "__main__":
    main()
