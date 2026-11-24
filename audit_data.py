"""Compatibility entry point for the curated conversation corpus audit.

The shared preparation pipeline also writes separate scenario-review candidates.
"""
from prepare_data import main

if __name__ == "__main__":
    main()
