#!/usr/bin/env python3
"""Shim: the logic lives in campaign_toolkit.validate_run.

Kept at this path, with the same CLI, so the campaign's docs, CI and habits do
not change when the shared tooling is updated.
"""
import pathlib
import sys

from campaign_toolkit.validate_run import main

if __name__ == "__main__":
    sys.exit(main(root=pathlib.Path(__file__).resolve().parent.parent))
