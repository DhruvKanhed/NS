"""Hill Cipher (2×2 Matrix) implementation."""

import re
from typing import Any, List, Tuple
from .base import BaseCipher, CipherResult
from ..utils.validation import parse_hill_2x2_matrix, validate_not_empty
from ..utils.text_utils import format_grid


class HillCipher(BaseCipher):
    name = "Hill Cipher (2×2)"
    category = "Substitution"
    description = "Polygraphic substitution cipher based on linear algebra and modular matrix arithmetic modulo 26."

    @staticmethod
    def get_inverse_matrix(matrix: List[List[int]], det_inv: int) -> List[List[int]]:
        """Calculate inverse 2x2 matrix modulo 26."""
        a, b = matrix[0][0], matrix[0][1]
        c, d = matrix[1][0], matrix[1][1]

        # Adjugate of [[a, b], [c, d]] is [[d, -b], [-c, a]]
        adj = [
            [(d % 26), ((-b % 26) + 26) % 26],
            [((-c % 26) + 26) % 26, (a % 26)]
        ]

        inv = [
            [(det_inv * adj[0][0]) % 26, (det_inv * adj[0][1]) % 26],
            [(det_inv * adj[1][0]) % 26, (det_inv * adj[1][1]) % 26]
        ]
        return inv

    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        matrix, det, det_inv = parse_hill_2x2_matrix(key)
        inv_matrix = self.get_inverse_matrix(matrix, det_inv)

        letters = [ch.upper() for ch in plaintext if ch.isalpha()]
        if not letters:
            raise ValueError("Hill cipher encryption requires at least one alphabetic letter.")

        padded = False
        if len(letters) % 2 != 0:
            letters.append("X")
            padded = True

        cipher_letters = []
        for i in range(0, len(letters), 2):
            v0 = ord(letters[i]) - 65
            v1 = ord(letters[i + 1]) - 65

            c0 = (matrix[0][0] * v0 + matrix[0][1] * v1) % 26
            c1 = (matrix[1][0] * v0 + matrix[1][1] * v1) % 26

            cipher_letters.append(chr(c0 + 65))
            cipher_letters.append(chr(c1 + 65))

        ciphertext = "".join(cipher_letters)
        matrix_str = format_grid(matrix)
        inv_str = format_grid(inv_matrix)

        notes = [
            f"Key Matrix K mod 26:\n{matrix_str}",
            f"Determinant det(K) = {det} (gcd({det}, 26) = 1, det⁻¹ = {det_inv})",
            f"Inverse Key Matrix K⁻¹ mod 26:\n{inv_str}",
        ]
        if padded:
            notes.append("Padded odd-length input with trailing 'X'.")

        return CipherResult(
            text=ciphertext,
            key_display=f"[[{matrix[0][0]}, {matrix[0][1]}], [{matrix[1][0]}, {matrix[1][1]}]]",
            metadata={
                "matrix": matrix,
                "inverse_matrix": inv_matrix,
                "det": det,
                "det_inv": det_inv,
                "padded": padded,
            },
            notes="\n\n".join(notes)
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        matrix, det, det_inv = parse_hill_2x2_matrix(key)
        inv_matrix = self.get_inverse_matrix(matrix, det_inv)

        letters = [ch.upper() for ch in ciphertext if ch.isalpha()]
        if len(letters) % 2 != 0:
            raise ValueError(
                f"Ciphertext length must be an even number of letters for 2×2 Hill cipher (got {len(letters)})."
            )

        plain_letters = []
        for i in range(0, len(letters), 2):
            v0 = ord(letters[i]) - 65
            v1 = ord(letters[i + 1]) - 65

            p0 = (inv_matrix[0][0] * v0 + inv_matrix[0][1] * v1) % 26
            p1 = (inv_matrix[1][0] * v0 + inv_matrix[1][1] * v1) % 26

            plain_letters.append(chr(p0 + 65))
            plain_letters.append(chr(p1 + 65))

        plaintext = "".join(plain_letters)
        inv_str = format_grid(inv_matrix)

        return CipherResult(
            text=plaintext,
            key_display=f"[[{matrix[0][0]}, {matrix[0][1]}], [{matrix[1][0]}, {matrix[1][1]}]]",
            metadata={
                "matrix": matrix,
                "inverse_matrix": inv_matrix,
                "det": det,
                "det_inv": det_inv,
            },
            notes=(
                f"Decrypted using Modular Inverse Matrix K⁻¹ mod 26:\n{inv_str}\n"
                f"Note: Any trailing 'X' padding applied during encryption is preserved."
            )
        )
