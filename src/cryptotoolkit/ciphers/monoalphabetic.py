"""Monoalphabetic Substitution Cipher implementation."""

import secrets
import string
from typing import Any, Dict
from .base import BaseCipher, CipherResult
from ..utils.validation import validate_monoalphabetic_key, validate_not_empty

ALPHABET = string.ascii_uppercase


class MonoalphabeticCipher(BaseCipher):
    name = "Monoalphabetic Substitution Cipher"
    category = "Substitution"
    description = "Each letter of the plaintext alphabet is mapped to a distinct substitute letter defined by a 26-letter permutation key."

    @staticmethod
    def generate_key() -> str:
        """Generate a cryptographically randomized 26-letter substitution alphabet."""
        shuffled = list(ALPHABET)
        # Fisher-Yates shuffle using secrets.randbelow
        for i in range(len(shuffled) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        return "".join(shuffled)

    @staticmethod
    def format_mapping_table(key: str) -> str:
        """Format an educational mapping table for the substitution key."""
        plain_row = "Plain:  " + " ".join(ALPHABET)
        cipher_row = "Cipher: " + " ".join(key)
        return f"{plain_row}\n{cipher_row}"

    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        valid_key = validate_monoalphabetic_key(key)

        # Build translation map
        upper_map = {ALPHABET[i]: valid_key[i] for i in range(26)}
        lower_map = {ALPHABET[i].lower(): valid_key[i].lower() for i in range(26)}

        result_chars = []
        for ch in plaintext:
            if ch in upper_map:
                result_chars.append(upper_map[ch])
            elif ch in lower_map:
                result_chars.append(lower_map[ch])
            else:
                result_chars.append(ch)

        ciphertext = "".join(result_chars)
        return CipherResult(
            text=ciphertext,
            key_display=valid_key,
            metadata={"key": valid_key, "mapping_table": self.format_mapping_table(valid_key)},
            notes=(
                f"Each English letter is replaced using the 26-letter key.\n"
                f"Letter case, digits, spaces, and punctuation are preserved unchanged."
            )
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        valid_key = validate_monoalphabetic_key(key)

        # Inverse translation map
        inv_upper_map = {valid_key[i]: ALPHABET[i] for i in range(26)}
        inv_lower_map = {valid_key[i].lower(): ALPHABET[i].lower() for i in range(26)}

        result_chars = []
        for ch in ciphertext:
            if ch in inv_upper_map:
                result_chars.append(inv_upper_map[ch])
            elif ch in inv_lower_map:
                result_chars.append(inv_lower_map[ch])
            else:
                result_chars.append(ch)

        plaintext = "".join(result_chars)
        return CipherResult(
            text=plaintext,
            key_display=valid_key,
            metadata={"key": valid_key, "mapping_table": self.format_mapping_table(valid_key)},
            notes="Decrypted by inverting the substitution alphabet mapping."
        )
