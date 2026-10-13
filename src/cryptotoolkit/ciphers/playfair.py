"""Playfair Cipher implementation."""

import re
from typing import Any, List, Tuple
from .base import BaseCipher, CipherResult
from ..utils.validation import validate_playfair_key, validate_not_empty
from ..utils.text_utils import format_grid


class PlayfairCipher(BaseCipher):
    name = "Playfair Cipher"
    category = "Substitution"
    description = "Digraphic substitution cipher encrypting pairs of letters (digraphs) using a 5×5 matrix constructed from a keyword, combining I and J."

    @staticmethod
    def generate_matrix(keyword: str) -> Tuple[List[List[str]], dict]:
        """Generate 5x5 Playfair matrix from keyword (I/J combined).
        Returns (matrix_5x5, position_dict: char -> (row, col)).
        """
        cleaned = re.sub(r"[^A-Za-z]", "", keyword).upper().replace("J", "I")
        seen = set()
        sequence = []
        for ch in cleaned:
            if ch not in seen and ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
                seen.add(ch)
                sequence.append(ch)

        for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            if ch not in seen:
                seen.add(ch)
                sequence.append(ch)

        matrix = [sequence[i * 5 : (i + 1) * 5] for i in range(5)]
        pos_map = {}
        for r in range(5):
            for c in range(5):
                pos_map[matrix[r][c]] = (r, c)
        return matrix, pos_map

    @staticmethod
    def prepare_plaintext(text: str) -> Tuple[List[Tuple[str, str]], List[str]]:
        """Normalize plaintext into pairs of letters with filler letters."""
        # Clean: keep only letters, uppercase, replace J with I
        letters = [ch.upper().replace("J", "I") for ch in text if ch.isalpha()]
        if not letters:
            return [], []

        digraphs: List[Tuple[str, str]] = []
        notes: List[str] = []
        i = 0
        while i < len(letters):
            first = letters[i]
            if i + 1 < len(letters):
                second = letters[i + 1]
                if first == second:
                    filler = "X" if first != "X" else "Q"
                    digraphs.append((first, filler))
                    notes.append(f"Inserted filler '{filler}' between duplicate letters '{first}{first}'.")
                    i += 1
                else:
                    digraphs.append((first, second))
                    i += 2
            else:
                # Odd length trailing letter
                pad = "X" if first != "X" else "Z"
                digraphs.append((first, pad))
                notes.append(f"Appended padding letter '{pad}' to odd-length trailing letter '{first}'.")
                i += 1

        return digraphs, notes

    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        valid_key = validate_playfair_key(key)
        matrix, pos_map = self.generate_matrix(valid_key)

        digraphs, prep_notes = self.prepare_plaintext(plaintext)
        if not digraphs:
            raise ValueError("Playfair encryption requires at least one alphabetic character.")

        cipher_pairs = []
        for a, b in digraphs:
            r1, c1 = pos_map[a]
            r2, c2 = pos_map[b]

            if r1 == r2:
                # Same row -> shift right
                ca = matrix[r1][(c1 + 1) % 5]
                cb = matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:
                # Same column -> shift down
                ca = matrix[(r1 + 1) % 5][c1]
                cb = matrix[(r2 + 1) % 5][c2]
            else:
                # Rectangle -> swap columns
                ca = matrix[r1][c2]
                cb = matrix[r2][c1]

            cipher_pairs.append(ca + cb)

        ciphertext = " ".join(cipher_pairs)
        matrix_str = format_grid(matrix)

        notes_str = "\n".join(prep_notes) if prep_notes else "Clean digraph pairing without fillers."
        return CipherResult(
            text=ciphertext,
            key_display=f"Keyword: {valid_key}",
            metadata={
                "matrix": matrix,
                "matrix_display": matrix_str,
                "digraphs": digraphs,
                "notes": prep_notes,
            },
            notes=(
                f"Playfair 5×5 Key Matrix (I/J combined):\n{matrix_str}\n\n"
                f"Digraph Preprocessing:\n{notes_str}"
            )
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        valid_key = validate_playfair_key(key)
        matrix, pos_map = self.generate_matrix(valid_key)

        # Normalize ciphertext: letters only, uppercase, J -> I
        clean_ct = [ch.upper().replace("J", "I") for ch in ciphertext if ch.isalpha()]
        if len(clean_ct) % 2 != 0:
            raise ValueError(
                f"Ciphertext has odd number of letters ({len(clean_ct)}). "
                "Valid Playfair ciphertext must consist of even-length digraph pairs."
            )

        plain_pairs = []
        for i in range(0, len(clean_ct), 2):
            a, b = clean_ct[i], clean_ct[i + 1]
            if a not in pos_map or b not in pos_map:
                continue
            r1, c1 = pos_map[a]
            r2, c2 = pos_map[b]

            if r1 == r2:
                # Same row -> shift left
                pa = matrix[r1][(c1 - 1 + 5) % 5]
                pb = matrix[r2][(c2 - 1 + 5) % 5]
            elif c1 == c2:
                # Same column -> shift up
                pa = matrix[(r1 - 1 + 5) % 5][c1]
                pb = matrix[(r2 - 1 + 5) % 5][c2]
            else:
                # Rectangle -> swap columns
                pa = matrix[r1][c2]
                pb = matrix[r2][c1]

            plain_pairs.append(pa + pb)

        recovered_text = "".join(plain_pairs)
        matrix_str = format_grid(matrix)

        return CipherResult(
            text=recovered_text,
            key_display=f"Keyword: {valid_key}",
            metadata={"matrix": matrix, "matrix_display": matrix_str},
            notes=(
                f"Decrypted digraphs combined into plaintext.\n"
                f"Note: Inserted filler letters ('X', 'Q') or trailing padding remain in decrypted text "
                f"by design, because in classical cryptography automatic removal would risk stripping valid letters "
                f"(e.g., 'FOX', 'EXTRA', 'AXIS')."
            )
        )
