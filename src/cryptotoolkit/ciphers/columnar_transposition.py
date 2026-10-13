"""Columnar Transposition Cipher implementation (Irregular / Exact Transposition)."""

import math
from typing import Any, Dict, List, Tuple
from .base import BaseCipher, CipherResult
from ..utils.validation import validate_columnar_key, validate_not_empty
from ..utils.text_utils import format_grid


class ColumnarTranspositionCipher(BaseCipher):
    name = "Columnar Transposition Cipher"
    category = "Transposition"
    description = "Transposition cipher where message text is written in rows of fixed width and read out column-by-column in the alphabetical order of the keyword."

    @staticmethod
    def get_column_lengths(text_len: int, num_cols: int) -> List[int]:
        """Calculate the exact character count of each column for irregular grids."""
        base_len = text_len // num_cols
        rem = text_len % num_cols
        return [base_len + 1 if c < rem else base_len for c in range(num_cols)]

    @staticmethod
    def format_columnar_grid(text: str, key_str: str, col_order: List[int]) -> str:
        """Render a clear visualization of the transposition grid and reading order."""
        num_cols = len(col_order)
        num_rows = math.ceil(len(text) / num_cols)

        # Build grid
        grid = [[" " for _ in range(num_cols)] for _ in range(num_rows)]
        for idx, ch in enumerate(text):
            r = idx // num_cols
            c = idx % num_cols
            grid[r][c] = ch if ch != " " else "␣"

        # Column reading priority (1-indexed rank)
        ranks = [0] * num_cols
        for rank, col_idx in enumerate(col_order):
            ranks[col_idx] = rank + 1

        lines = []
        if len(key_str) == num_cols:
            lines.append("Key:   " + "  ".join(f"{ch:>2}" for ch in key_str))
        lines.append("Order: " + "  ".join(f"{r:>2}" for r in ranks))
        lines.append("-" * (num_cols * 4 + 7))

        for row_idx, row in enumerate(grid):
            lines.append(f"Row {row_idx + 1:<2}: " + "  ".join(f"{ch:>2}" for ch in row))

        return "\n".join(lines)

    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        key_str, col_order = validate_columnar_key(key)
        num_cols = len(col_order)
        length = len(plaintext)

        # Build columns by distributing plaintext row-wise
        columns: List[List[str]] = [[] for _ in range(num_cols)]
        for idx, ch in enumerate(plaintext):
            columns[idx % num_cols].append(ch)

        # Read out columns in the order defined by the keyword
        ciphertext_parts = []
        for col_idx in col_order:
            ciphertext_parts.append("".join(columns[col_idx]))

        ciphertext = "".join(ciphertext_parts)
        grid_viz = self.format_columnar_grid(plaintext, key_str, col_order)

        order_str = " -> ".join(f"Col {idx + 1}" for idx in col_order)
        return CipherResult(
            text=ciphertext,
            key_display=f"Key: {key_str} ({num_cols} columns)",
            metadata={
                "key_str": key_str,
                "col_order": col_order,
                "grid_viz": grid_viz,
            },
            notes=(
                f"Transposition Order: {order_str}\n\n"
                f"Grid Visualization (␣ indicates space):\n{grid_viz}\n\n"
                f"Note: Standard irregular transposition preserves all spaces and punctuation "
                f"without adding extraneous padding characters."
            )
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        key_str, col_order = validate_columnar_key(key)
        num_cols = len(col_order)
        length = len(ciphertext)

        col_lengths = self.get_column_lengths(length, num_cols)

        # Slice ciphertext into column segments based on reading order
        col_segments: Dict[int, List[str]] = {}
        ptr = 0
        for col_idx in col_order:
            segment_len = col_lengths[col_idx]
            col_segments[col_idx] = list(ciphertext[ptr : ptr + segment_len])
            ptr += segment_len

        # Reconstruct row by row
        num_rows = math.ceil(length / num_cols)
        plaintext_chars = []
        for r in range(num_rows):
            for c in range(num_cols):
                if r < len(col_segments[c]):
                    plaintext_chars.append(col_segments[c][r])

        plaintext = "".join(plaintext_chars)
        grid_viz = self.format_columnar_grid(plaintext, key_str, col_order)

        return CipherResult(
            text=plaintext,
            key_display=f"Key: {key_str} ({num_cols} columns)",
            metadata={
                "key_str": key_str,
                "col_order": col_order,
                "grid_viz": grid_viz,
            },
            notes="Reconstructed exactly from columnar slices."
        )
