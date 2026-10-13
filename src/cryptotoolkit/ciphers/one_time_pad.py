"""One-Time Pad (Vernam Cipher) implementation."""

import secrets
import string
from typing import Any, Tuple
from .base import BaseCipher, CipherResult
from ..utils.validation import validate_otp_key, validate_not_empty

ALPHABET = string.ascii_uppercase


class OneTimePadCipher(BaseCipher):
    name = "One-Time Pad"
    category = "Substitution"
    description = "Theoretically unbreakable cipher (Vernam) providing perfect secrecy when used with a truly random, single-use key of equal or greater length."

    @staticmethod
    def generate_random_key(length: int) -> str:
        """Generate a cryptographically secure random alphabetic key using Python's secrets module."""
        if length <= 0:
            length = 16
        return "".join(secrets.choice(ALPHABET) for _ in range(length))

    @staticmethod
    def count_alphabetic_characters(text: str) -> int:
        """Count alphabetic characters requiring key characters."""
        return sum(1 for ch in text if ch.isalpha())

    def encrypt(self, plaintext: str, key: Any = None, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        alpha_count = self.count_alphabetic_characters(plaintext)
        if alpha_count == 0:
            raise ValueError("Plaintext must contain at least one alphabetic character.")

        key_str = str(key).strip() if key is not None else ""
        if not key_str:
            # Generate new random key if user explicitly did not supply one for encryption
            key_str = self.generate_random_key(alpha_count)

        valid_key = validate_otp_key(key_str, required_min_length=alpha_count)

        result_chars = []
        k_idx = 0
        for ch in plaintext:
            if "A" <= ch <= "Z":
                shift = ord(valid_key[k_idx]) - 65
                result_chars.append(chr((ord(ch) - 65 + shift) % 26 + 65))
                k_idx += 1
            elif "a" <= ch <= "z":
                shift = ord(valid_key[k_idx]) - 65
                result_chars.append(chr((ord(ch) - 97 + shift) % 26 + 97))
                k_idx += 1
            else:
                result_chars.append(ch)

        ciphertext = "".join(result_chars)
        used_key = valid_key[:alpha_count]

        warning_note = (
            "SECURITY REQUIREMENTS FOR PERFECT SECRECY (Shannon's Theorem):\n"
            "1. Truly Random: Key generated using cryptographically secure PRNG (Python secrets).\n"
            "2. Key Length >= Message: Exactly one key character per alphabetic character.\n"
            "3. Single Use Only: NEVER reuse this key! Reusing a one-time pad key allows depth-reading attacks.\n"
            "4. Absolute Secrecy: Secure key exchange is required before communication."
        )

        return CipherResult(
            text=ciphertext,
            key_display=valid_key,
            metadata={
                "key": valid_key,
                "used_key": used_key,
                "alpha_count": alpha_count,
            },
            notes=warning_note
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        key_str = str(key).strip() if key is not None else ""
        if not key_str:
            raise ValueError(
                "Decryption requires the exact original One-Time Pad key. "
                "A key is NEVER automatically generated during decryption."
            )

        alpha_count = self.count_alphabetic_characters(ciphertext)
        if alpha_count == 0:
            raise ValueError("Ciphertext must contain at least one alphabetic character.")

        valid_key = validate_otp_key(key_str, required_min_length=alpha_count)

        result_chars = []
        k_idx = 0
        for ch in ciphertext:
            if "A" <= ch <= "Z":
                shift = ord(valid_key[k_idx]) - 65
                result_chars.append(chr((ord(ch) - 65 - shift + 26) % 26 + 65))
                k_idx += 1
            elif "a" <= ch <= "z":
                shift = ord(valid_key[k_idx]) - 65
                result_chars.append(chr((ord(ch) - 97 - shift + 26) % 26 + 97))
                k_idx += 1
            else:
                result_chars.append(ch)

        plaintext = "".join(result_chars)
        return CipherResult(
            text=plaintext,
            key_display=valid_key,
            metadata={"key": valid_key, "alpha_count": alpha_count},
            notes="Decrypted using the verified original One-Time Pad key."
        )
