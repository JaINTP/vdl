"""
Entry Point: VSIX Downloader Application

This script serves as the entry point for running the VSIX Downloader application.
It initializes and runs the `DownloadApp` from the `vdl.tui` module.

Usage:
    python main.py
"""

import sys
from pathlib import Path
from vdl.tui import DownloadApp

# Add the parent directory to the Python path for module resolution
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

def main() -> None:
    """
    Main entry point for the application.
    Initializes and runs the DownloadApp.
    """
    DownloadApp().run()

if __name__ == '__main__':
    main()