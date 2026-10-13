"""Interactive Command Line Interface matching the exact 13-item menu structure."""

import os
import sys
import time
from typing import Optional

from .ciphers import get_cipher, CIPHER_REGISTRY
from .ciphers.monoalphabetic import MonoalphabeticCipher
from .ciphers.one_time_pad import OneTimePadCipher
from .services.file_service import FileService
from .services.comparison_service import ComparisonService


BANNER = r"""
======================================================================
                 CLASSICAL CRYPTOGRAPHY TOOLKIT
          Final Year (ECM) Mini-Project | Network Security
======================================================================
"""

MENU_TEXT = """
[ SUBSTITUTION CIPHERS ]
  1. Caesar Cipher
  2. Monoalphabetic Substitution Cipher
  3. Playfair Cipher
  4. Hill Cipher (2×2 Matrix)
  5. Vigenère (Polyalphabetic) Cipher
  6. One-Time Pad (Vernam)

[ TRANSPOSITION CIPHERS ]
  7. Rail Fence Cipher
  8. Columnar Transposition Cipher

[ UTILITY MODULES ]
  9. Compare Algorithms
 10. Encrypt Text File
 11. Decrypt Text File
 12. Help and Documentation
 13. Exit
"""


def prompt_cipher(cipher_id: str, default_key_hint: str) -> None:
    """Generic interactive encrypt/decrypt handler for a cipher."""
    cipher = get_cipher(cipher_id)
    print(f"\n--- {cipher.name.upper()} ---")
    print(f"Description: {cipher.description}\n")

    mode = input("Select Operation (1 = Encrypt, 2 = Decrypt, Q = Cancel): ").strip()
    if mode.upper() == "Q":
        return
    if mode not in ("1", "2"):
        print("Invalid choice. Returning to main menu.")
        return

    text_prompt = "Enter plaintext: " if mode == "1" else "Enter ciphertext: "
    text = input(text_prompt)

    if cipher_id == "one_time_pad" and mode == "1":
        print(f"Hint: Press Enter to automatically generate a random key via secrets.")
    key = input(f"Enter key [{default_key_hint}]: ").strip()

    try:
        t0 = time.perf_counter_ns()
        if mode == "1":
            res = cipher.encrypt(text, key)
            op = "Encryption"
        else:
            res = cipher.decrypt(text, key)
            op = "Decryption"
        t1 = time.perf_counter_ns()
        duration_us = (t1 - t0) / 1000.0

        print(f"\n{op} Successful!")
        print(f"Result: {res.text}")
        print(f"Key: {res.key_display}")
        print(f"Execution Time: {duration_us:.2f} µs ({duration_us / 1000.0:.4f} ms)")
        if res.notes:
            print(f"\nNotes & Details:\n{res.notes}")
    except Exception as exc:
        print(f"\n[ERROR] Operation failed: {exc}")


def handle_monoalphabetic() -> None:
    """Special handler for Monoalphabetic Cipher with random key generator."""
    cipher = get_cipher("monoalphabetic")
    print("\n--- MONOALPHABETIC SUBSTITUTION CIPHER ---")
    print("1. Encrypt with custom or generated key")
    print("2. Decrypt with key")
    print("3. Generate a random 26-letter substitution key")
    choice = input("Enter choice (1-3): ").strip()

    if choice == "3":
        key = MonoalphabeticCipher.generate_key()
        print(f"\nGenerated Random Key:\n{key}")
        print("\nMapping Table:")
        print(MonoalphabeticCipher.format_mapping_table(key))
        return

    prompt_cipher("monoalphabetic", "26-letter alphabet, e.g. QWERTYUIOPASDFGHJKLZXCVBNM")


def handle_comparison() -> None:
    """Run benchmark comparison in CLI."""
    print("\n--- ALGORITHM COMPARISON & BENCHMARK ---")
    msg = input("Enter sample message to compare across ciphers [Default: 'NETWORK SECURITY']: ").strip()
    if not msg:
        msg = "NETWORK SECURITY"

    print("\nRunning benchmarks with time.perf_counter_ns()...\n")
    rows = ComparisonService.run_comparison(msg)

    header = f"{'Algorithm':<28} | {'Category':<14} | {'Enc (µs)':<9} | {'Dec (µs)':<9} | {'Roundtrip'}"
    print(header)
    print("-" * len(header))
    for r in rows:
        rt = "PASS" if r.round_trip_success else "FAIL/NORM"
        print(f"{r.cipher_name:<28} | {r.category:<14} | {r.enc_time_us:<9.2f} | {r.dec_time_us:<9.2f} | {rt}")

    print("\nLimitations & Observations:")
    for r in rows:
        print(f"• {r.cipher_name}: {r.limitations}")


def handle_file_encrypt() -> None:
    """File encryption workflow."""
    print("\n--- FILE ENCRYPTION ---")
    in_path = input("Enter input text file path: ").strip()
    if not in_path:
        print("Path cannot be empty.")
        return
    out_path = input("Enter destination output file path: ").strip()
    if not out_path:
        print("Destination path cannot be empty.")
        return

    print("Select Cipher:")
    ciphers = list(CIPHER_REGISTRY.keys())
    for i, cid in enumerate(ciphers, 1):
        print(f"  {i}. {get_cipher(cid).name}")
    c_idx = input("Choose cipher number (1-8): ").strip()
    try:
        cid = ciphers[int(c_idx) - 1]
    except (ValueError, IndexError):
        print("Invalid cipher selection.")
        return

    key = input("Enter key: ").strip()
    try:
        res = FileService.encrypt_file(in_path, out_path, cid, key, overwrite=True)
        print(f"\n[SUCCESS] {res.message}")
        print(f"Output saved to: {res.output_path}")
        print(f"Original size: {res.input_size_bytes} bytes -> Output size: {res.output_size_bytes} bytes")
        print(f"Execution time: {res.execution_time_ms:.3f} ms")
    except Exception as exc:
        print(f"\n[ERROR] File encryption failed: {exc}")


def handle_file_decrypt() -> None:
    """File decryption workflow."""
    print("\n--- FILE DECRYPTION ---")
    in_path = input("Enter encrypted envelope file path: ").strip()
    if not in_path:
        print("Path cannot be empty.")
        return
    out_path = input("Enter destination plaintext file path: ").strip()
    if not out_path:
        print("Destination path cannot be empty.")
        return

    key = input("Enter secret key: ").strip()
    try:
        res = FileService.decrypt_file(in_path, out_path, key, overwrite=True)
        print(f"\n[SUCCESS] {res.message}")
        print(f"Decrypted text saved to: {res.output_path}")
        print(f"Execution time: {res.execution_time_ms:.3f} ms")
    except Exception as exc:
        print(f"\n[ERROR] File decryption failed: {exc}")


def handle_help() -> None:
    """Display Help documentation."""
    print("""
======================================================================
                     HELP & DOCUMENTATION OVERVIEW
======================================================================
1. Classical Ciphers operate on characters rather than modern binary bit blocks.
   - Substitution Ciphers replace characters or digraphs with alternatives.
   - Transposition Ciphers reorder or permute the positions of characters.

2. Ciphers and Required Key Formats:
   - Caesar: Integer shift 0-25 (e.g. 5).
   - Monoalphabetic: 26 unique letters (e.g. QWERTYUIOPASDFGHJKLZXCVBNM).
   - Playfair: Keyword (e.g. MONARCHY), 5x5 grid combining I/J.
   - Hill: 4 integers (e.g. 3 3 2 5) with determinant coprime to 26.
   - Vigenère: Repeating keyword (e.g. SECRET).
   - One-Time Pad: Random alphabetic key of equal or greater length.
   - Rail Fence: Integer number of rails >= 1 (e.g. 3).
   - Columnar: Keyword or permutation order (e.g. ZEBRA).

3. Important Security Warning:
   Classical ciphers are strictly for academic demonstration and historical
   study. They are completely insecure against modern cryptanalysis (frequency
   analysis, Kasiski test, known plaintext, brute force). Never protect real-world
   confidential data with classical ciphers.
======================================================================
""")


def run_cli() -> None:
    """Main CLI event loop."""
    print(BANNER)
    while True:
        print(MENU_TEXT)
        choice = input("Enter selection (1-13): ").strip()
        if choice == "1":
            prompt_cipher("caesar", "integer 0–25, e.g. 5")
        elif choice == "2":
            handle_monoalphabetic()
        elif choice == "3":
            prompt_cipher("playfair", "keyword, e.g. MONARCHY")
        elif choice == "4":
            prompt_cipher("hill", "4 numbers '3 3 2 5' or 4-letter word 'DDCF'")
        elif choice == "5":
            prompt_cipher("vigenere", "keyword, e.g. SECRET")
        elif choice == "6":
            prompt_cipher("one_time_pad", "alphabetic key matching text length")
        elif choice == "7":
            prompt_cipher("rail_fence", "positive integer rails, e.g. 3")
        elif choice == "8":
            prompt_cipher("columnar_transposition", "keyword e.g. ZEBRA or permutation 3 1 4 2")
        elif choice == "9":
            handle_comparison()
        elif choice == "10":
            handle_file_encrypt()
        elif choice == "11":
            handle_file_decrypt()
        elif choice == "12":
            handle_help()
        elif choice == "13":
            print("\nExiting Classical Cryptography Toolkit. Goodbye!\n")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 13.")


if __name__ == "__main__":
    run_cli()
