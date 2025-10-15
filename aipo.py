#!/usr/bin/env python3
"""
AI Project Orchestrator (AIPO) - CLI Tool Entry Point

This is the main entry point for the aipo command-line tool.
The actual implementation is in the aipo package.
"""

import sys
from aipo.cli import main

if __name__ == '__main__':
    sys.exit(main())
