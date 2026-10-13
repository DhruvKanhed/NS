"""Text utilities and mathematical helper functions for classical ciphers."""

from typing import Tuple


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a: int, m: int = 26) -> int:
    """Compute modular multiplicative inverse of a modulo m.
    Raises ValueError if gcd(a, m) != 1.
    """
    a = a % m
    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        raise ValueError(f"No modular inverse exists for {a} modulo {m} (gcd is {gcd}).")
    return (x % m + m) % m


def clean_alpha_only(text: str, keep_case: bool = False) -> str:
    """Extract only alphabetic characters."""
    filtered = "".join(ch for ch in text if ch.isalpha())
    return filtered if keep_case else filtered.upper()


def format_grid(grid: list, cell_width: int = 3) -> str:
    """Format a 2D list into a neat string representation."""
    lines = []
    for row in grid:
        lines.append(" ".join(f"{str(cell):>{cell_width}}" for cell in row))
    return "\n".join(lines)
