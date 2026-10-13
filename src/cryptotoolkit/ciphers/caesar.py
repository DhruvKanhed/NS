"""Caesar Cipher implementation."""

from typing import Any
from .base import BaseCipher, CipherResult
from ..utils.validation import validate_caesar_key, validate_not_empty


class CaesarCipher(BaseCipher):
    name = "Caesar Cipher"
    category = "Substitution"
    description = "Monoalphabetic shift cipher where each letter is replaced by a letter a fixed number of positions down the alphabet."

    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        shift = validate_caesar_key(key)

        result_chars = []
        for ch in plaintext:
            if "A" <= ch <= "Z":
                result_chars.append(chr((ord(ch) - 65 + shift) % 26 + 65))
            elif "a" <= ch <= "z":
                result_chars.append(chr((ord(ch) - 97 + shift) % 26 + 97))
            else:
                result_chars.append(ch)

        ciphertext = "".join(result_chars)
        return CipherResult(
            text=ciphertext,
            key_display=f"Shift: {shift} (normalized mod 26)",
            metadata={"shift": shift},
            notes=f"Shift {shift}: C = (P + {shift}) mod 26. Spaces, numbers, and punctuation are preserved unchanged."
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        shift = validate_caesar_key(key)

        result_chars = []
        for ch in ciphertext:
            if "A" <= ch <= "Z":
                result_chars.append(chr((ord(ch) - 65 - shift + 26) % 26 + 65))
            elif "a" <= ch <= "z":
                result_chars.append(chr((ord(ch) - 97 - shift + 26) % 26 + 97))
            else:
                result_chars.append(ch)

        plaintext = "".join(result_chars)
        return CipherResult(
            text=plaintext,
            key_display=f"Shift: {shift} (normalized mod 26)",
            metadata={"shift": shift},
            notes=f"Inverse Shift {shift}: P = (C - {shift}) mod 26."
        )
