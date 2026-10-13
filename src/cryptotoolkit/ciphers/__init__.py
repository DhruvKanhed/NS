"""Classical Ciphers registry and accessors."""

from typing import Dict, List, Type
from .base import BaseCipher, CipherResult
from .caesar import CaesarCipher
from .monoalphabetic import MonoalphabeticCipher
from .playfair import PlayfairCipher
from .hill import HillCipher
from .vigenere import VigenereCipher
from .one_time_pad import OneTimePadCipher
from .rail_fence import RailFenceCipher
from .columnar_transposition import ColumnarTranspositionCipher

CIPHER_REGISTRY: Dict[str, Type[BaseCipher]] = {
    "caesar": CaesarCipher,
    "monoalphabetic": MonoalphabeticCipher,
    "playfair": PlayfairCipher,
    "hill": HillCipher,
    "vigenere": VigenereCipher,
    "one_time_pad": OneTimePadCipher,
    "rail_fence": RailFenceCipher,
    "columnar_transposition": ColumnarTranspositionCipher,
}

CIPHER_DISPLAY_NAMES = [
    ("caesar", "1. Caesar Cipher (Substitution)"),
    ("monoalphabetic", "2. Monoalphabetic Substitution Cipher"),
    ("playfair", "3. Playfair Cipher (Digraph Substitution)"),
    ("hill", "4. Hill Cipher (2×2 Matrix Substitution)"),
    ("vigenere", "5. Vigenère Cipher (Polyalphabetic)"),
    ("one_time_pad", "6. One-Time Pad (Vernam Cipher)"),
    ("rail_fence", "7. Rail Fence Cipher (Transposition)"),
    ("columnar_transposition", "8. Columnar Transposition Cipher"),
]


def get_cipher(cipher_id: str) -> BaseCipher:
    """Retrieve an instantiated cipher by ID."""
    key = cipher_id.lower().replace("-", "_").replace(" ", "_")
    if key not in CIPHER_REGISTRY:
        raise KeyError(f"Cipher '{cipher_id}' not found in registry.")
    return CIPHER_REGISTRY[key]()


def get_all_ciphers() -> List[BaseCipher]:
    """Retrieve instantiated list of all 8 ciphers in canonical order."""
    return [cls() for cls in CIPHER_REGISTRY.values()]
