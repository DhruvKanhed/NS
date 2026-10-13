"""Input and key validation routines for classical ciphers."""

import math
import re
from typing import List, Tuple
from .text_utils import egcd


class ValidationError(ValueError):
    """Raised when cipher input or key validation fails."""
    pass


def validate_not_empty(text: str, field_name: str = "Input text") -> str:
    """Ensure text is not empty or whitespace only."""
    if not text or not text.strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return text


def validate_caesar_key(key_input: str) -> int:
    """Validate and normalize Caesar shift key."""
    if isinstance(key_input, int):
        return key_input % 26
    if not str(key_input).strip():
        raise ValidationError("Caesar key cannot be empty. Please enter an integer shift (0–25).")
    try:
        val = int(str(key_input).strip())
        return val % 26
    except ValueError:
        raise ValidationError(f"Invalid Caesar shift key '{key_input}'. Must be an integer.")


def validate_monoalphabetic_key(key_input: str) -> str:
    """Validate 26-letter substitution alphabet key."""
    cleaned = re.sub(r"[^A-Za-z]", "", str(key_input)).upper()
    if len(cleaned) != 26:
        raise ValidationError(
            f"Monoalphabetic key must contain exactly 26 letters (got {len(cleaned)}). "
            f"Current: '{key_input}'"
        )
    unique = set(cleaned)
    if len(unique) != 26:
        missing = sorted(list(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") - unique))
        duplicates = [ch for ch in unique if cleaned.count(ch) > 1]
        raise ValidationError(
            f"Monoalphabetic key must contain every English letter exactly once.\n"
            f"Duplicate letters: {', '.join(duplicates)}\n"
            f"Missing letters: {', '.join(missing)}"
        )
    return cleaned


def validate_playfair_key(key_input: str) -> str:
    """Validate Playfair cipher keyword."""
    cleaned = re.sub(r"[^A-Za-z]", "", str(key_input)).upper()
    if not cleaned:
        raise ValidationError("Playfair keyword must contain at least one alphabetic letter.")
    return cleaned


def parse_hill_2x2_matrix(key_input: str) -> Tuple[List[List[int]], int, int]:
    """Parse and validate 2x2 Hill cipher key matrix.
    Accepts formats:
    - '3, 3, 2, 5' or '3 3 2 5'
    - '[[3, 3], [2, 5]]'
    - 4-letter alphabetic keyword e.g. 'DDCF' (maps A=0..Z=25)
    Returns ((matrix_2x2), determinant_mod_26, modular_inverse_det).
    """
    cleaned = str(key_input).strip()
    if not cleaned:
        raise ValidationError("Hill key cannot be empty. Enter 4 numbers (e.g., '3 3 2 5') or a 4-letter keyword.")

    numbers: List[int] = []

    # Check if 4 alphabetic letters
    letters_only = re.sub(r"[^A-Za-z]", "", cleaned)
    if len(letters_only) == 4 and not re.search(r"\d", cleaned):
        numbers = [ord(c.upper()) - 65 for c in letters_only]
    else:
        # Extract all integer tokens
        tokens = re.findall(r"-?\d+", cleaned)
        if len(tokens) == 4:
            numbers = [int(t) for t in tokens]
        else:
            raise ValidationError(
                f"Hill 2x2 matrix requires exactly 4 numbers or a 4-letter word. "
                f"Found {len(tokens)} numbers in: '{cleaned}'"
            )

    a, b = numbers[0] % 26, numbers[1] % 26
    c, d = numbers[2] % 26, numbers[3] % 26
    matrix = [[a, b], [c, d]]

    det = (a * d - b * c) % 26
    det = (det + 26) % 26

    gcd, x, _ = egcd(det, 26)
    if gcd != 1:
        raise ValidationError(
            f"Invalid Hill matrix: Determinant is {det}, which is not coprime to 26 (gcd={gcd}). "
            f"The matrix is non-invertible modulo 26 and cannot decrypt messages.\n"
            f"Tip: Determinant must be odd and not a multiple of 13."
        )

    det_inv = (x % 26 + 26) % 26
    return matrix, det, det_inv


def validate_vigenere_key(key_input: str) -> str:
    """Validate Vigenere keyword."""
    cleaned = re.sub(r"[^A-Za-z]", "", str(key_input)).upper()
    if not cleaned:
        raise ValidationError("Vigenère keyword must contain at least one alphabetic letter.")
    return cleaned


def validate_otp_key(key_input: str, required_min_length: int = 1) -> str:
    """Validate One-Time Pad key."""
    cleaned = re.sub(r"[^A-Za-z]", "", str(key_input)).upper()
    if not cleaned:
        raise ValidationError("One-Time Pad key must be alphabetic and non-empty.")
    if len(cleaned) < required_min_length:
        raise ValidationError(
            f"One-Time Pad key is too short. Message has {required_min_length} alphabetic characters, "
            f"but key only has {len(cleaned)} letters. OTP requires key length >= message length."
        )
    return cleaned


def validate_rail_fence_rails(key_input: str) -> int:
    """Validate Rail Fence cipher rails count."""
    if isinstance(key_input, int):
        rails = key_input
    else:
        cleaned = str(key_input).strip()
        if not cleaned:
            raise ValidationError("Rail Fence rails count cannot be empty. Please enter an integer >= 1.")
        try:
            rails = int(cleaned)
        except ValueError:
            raise ValidationError(f"Invalid rails count '{key_input}'. Must be an integer >= 1.")
    if rails < 1:
        raise ValidationError(f"Rails count must be >= 1 (got {rails}).")
    return rails


def validate_columnar_key(key_input: str) -> Tuple[str, List[int]]:
    """Validate Columnar Transposition keyword or numeric order.
    Returns (normalized_key_string, column_order_0_indexed).
    """
    raw = str(key_input).strip()
    if not raw:
        raise ValidationError("Columnar key cannot be empty. Enter a keyword (e.g. 'ZEBRA') or permutation.")

    # Check if comma/space-separated digits (e.g. "3 1 4 2")
    digit_tokens = re.findall(r"\d+", raw)
    if digit_tokens and len("".join(digit_tokens)) == len(re.sub(r"[\s,]", "", raw)):
        nums = [int(t) for t in digit_tokens]
        # Check if 1-indexed or 0-indexed permutation
        k = len(nums)
        if sorted(nums) == list(range(1, k + 1)):
            order = [n - 1 for n in nums]
            return f"Order({' '.join(str(n) for n in nums)})", order
        elif sorted(nums) == list(range(k)):
            return f"Order({' '.join(str(n) for n in nums)})", nums
        else:
            raise ValidationError(
                f"Numeric columnar key must be a valid permutation of 1..{k} or 0..{k-1}."
            )

    # Otherwise alphabetic keyword
    cleaned = re.sub(r"[^A-Za-z0-9]", "", raw).upper()
    if not cleaned:
        raise ValidationError("Columnar keyword must contain letters or digits.")

    # Stable alphabetical sort to obtain column order
    # For repeated letters, order preserves original left-to-right occurrence
    indexed_chars = [(char, idx) for idx, char in enumerate(cleaned)]
    sorted_chars = sorted(indexed_chars, key=lambda item: item[0])
    order = [item[1] for item in sorted_chars]

    return cleaned, order
