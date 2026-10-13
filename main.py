#!/usr/bin/env python3
"""Main Entry Point for the Classical Cryptography Toolkit.

Final Year (ECM) Mini-Project | Academic Year 2026–27 | Subject: Network Security
"""

import argparse
import sys
import unittest
from pathlib import Path

# Add src to sys.path to ensure seamless local import
src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


def main():
    parser = argparse.ArgumentParser(
        description="Classical Cryptography Toolkit — Network Security Academic Mini-Project"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Launch the interactive Command-Line Interface menu (13 options) instead of Tkinter GUI",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the automated test suite discovering all unit and integration tests",
    )
    parser.add_argument(
        "--compare",
        type=str,
        nargs="?",
        const="NETWORK SECURITY",
        help="Run a quick algorithm performance comparison benchmark for the provided sample string",
    )

    args = parser.parse_args()

    if args.test:
        print("\n=== Running Automated Test Suite ===")
        loader = unittest.TestLoader()
        suite = loader.discover("tests")
        runner = unittest.TextTestRunner(verbosity=2)
        res = runner.run(suite)
        sys.exit(0 if res.wasSuccessful() else 1)

    if args.compare is not None:
        from cryptotoolkit.services.comparison_service import ComparisonService
        print(f"\n=== Algorithm Benchmark for Message: '{args.compare}' ===")
        rows = ComparisonService.run_comparison(args.compare)
        header = f"{'Algorithm':<28} | {'Category':<14} | {'Enc (µs)':<9} | {'Dec (µs)':<9} | {'Roundtrip'}"
        print(header)
        print("-" * len(header))
        for r in rows:
            rt = "PASS" if r.round_trip_success else "NORM"
            print(f"{r.cipher_name:<28} | {r.category:<14} | {r.enc_time_us:<9.2f} | {r.dec_time_us:<9.2f} | {rt}")
        return

    if args.cli:
        from cryptotoolkit.cli import run_cli
        run_cli()
        return

    # Default: launch modern desktop GUI
    try:
        from cryptotoolkit.gui.app import run_app
        run_app()
    except Exception as exc:
        print(f"[Notice] Failed to launch GUI window: {exc}")
        print("Falling back to interactive Command-Line Interface...\n")
        from cryptotoolkit.cli import run_cli
        run_cli()


if __name__ == "__main__":
    main()
