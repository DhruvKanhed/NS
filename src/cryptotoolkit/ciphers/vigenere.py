"""Vigenère Cipher (Polyalphabetic Substitution) implementation."""

from typing import Any
from .base import BaseCipher, CipherResult
from ..utils.validation import validate_vigenere_key, validate_not_empty


class VigenereCipher(BaseCipher):
    name = "Vigenère Cipher"
    category = "Substitution"
    description = "Polyalphabetic substitution cipher that encrypts letters using a repeating keyword, switching Caesar shifts per character."

    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        valid_key = validate_vigenere_key(key)

        result_chars = []
        key_idx = 0
        key_len = len(valid_key)

        for ch in plaintext:
            if "A" <= ch <= "Z":
                shift = ord(valid_key[key_idx % key_len]) - 65
                result_chars.append(chr((ord(ch) - 65 + shift) % 26 + 65))
                key_idx += 1
            elif "a" <= ch <= "z":
                shift = ord(valid_key[key_idx % key_len]) - 65
                result_chars.append(chr((ord(ch) - 97 + shift) % 26 + 97))
                key_idx += 1
            else:
                # Non-alphabetic character preserved without advancing keyword pointer
                result_chars.append(ch)

        ciphertext = "".join(result_chars)
        return CipherResult(
            text=ciphertext,
            key_display=f"Keyword: {valid_key}",
            metadata={"key": valid_key, "keystream_length": key_idx},
            notes=(
                f"Encrypted using polyalphabetic keyword '{valid_key}'.\n"
                f"Spaces, digits, and punctuation are preserved without advancing the key position."
            )
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        valid_key = validate_vigenere_key(key)

        result_chars = []
        key_idx = 0
        key_len = len(valid_key)

        for ch in ciphertext:
            if "A" <= ch <= "Z":
                shift = ord(valid_key[key_idx % key_len]) - 65
                result_chars.append(chr((ord(ch) - 65 - shift + 26) % 26 + 65))
                key_idx += 1
            elif "a" <= ch <= "z":
                shift = ord(valid_key[key_idx % key_len]) - 65
                result_chars.append(chr((ord(ch) - 97 - shift + 26) % 26 + 97))
                key_idx += 1
            else:
                result_chars.append(ch)

        plaintext = "".join(result_chars)
        return CipherResult(
            text=plaintext,
            key_display=f"Keyword: {valid_key}",
            metadata={"key": valid_key, "keystream_length": key_idx},
            notes="Decrypted by inverting each letter's keyword shift."
        )
