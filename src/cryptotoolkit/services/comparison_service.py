"""Algorithm Comparison and Benchmarking Service."""

from dataclasses import dataclass
import time
from typing import Dict, List, Optional
from ..ciphers import get_cipher, CIPHER_REGISTRY
from ..ciphers.monoalphabetic import MonoalphabeticCipher
from ..ciphers.one_time_pad import OneTimePadCipher


@dataclass
class ComparisonRow:
    """Row representing one cipher's benchmark and evaluation result."""
    cipher_id: str
    cipher_name: str
    category: str
    key_type: str
    key_used: str
    sample_input: str
    ciphertext: str
    recovered_text: str
    round_trip_success: bool
    enc_time_us: float
    dec_time_us: float
    limitations: str
    security_verdict: str


DEFAULT_COMPARISON_KEYS = {
    "caesar": "5",
    "monoalphabetic": "QWERTYUIOPASDFGHJKLZXCVBNM",
    "playfair": "MONARCHY",
    "hill": "3 3 2 5",
    "vigenere": "CIPHER",
    "one_time_pad": "",  # Auto-generated length-matched key
    "rail_fence": "3",
    "columnar_transposition": "SECRET",
}

KEY_TYPE_DESCRIPTIONS = {
    "caesar": "Integer shift (0–25)",
    "monoalphabetic": "26-letter substitution alphabet",
    "playfair": "Alphabetic keyword (5×5 matrix, I/J combined)",
    "hill": "2×2 invertible matrix mod 26 (det coprime to 26)",
    "vigenere": "Repeating alphabetic keyword",
    "one_time_pad": "Random alphabetic string (length ≥ message)",
    "rail_fence": "Integer rail count (≥ 1)",
    "columnar_transposition": "Keyword or numeric column order",
}

LIMITATIONS_DATA = {
    "caesar": "Trivial keyspace (25 non-trivial keys). Vulnerable to brute-force and frequency analysis in seconds.",
    "monoalphabetic": "Vulnerable to single-letter frequency analysis (E, T, A, O, I, N) and digram/trigram patterns.",
    "playfair": "Digraph frequency analysis reveals key structure; does not protect against modern cryptanalysis.",
    "hill": "Vulnerable to known-plaintext attack using 2 pairs of digraphs via standard linear algebra (matrix inversion).",
    "vigenere": "Vulnerable to Kasiski examination and Friedman test (Index of Coincidence) to deduce keyword length.",
    "one_time_pad": "Theoretically unbreakable ONLY if key is truly random, never reused, kept secret, and distributed securely.",
    "rail_fence": "Does not alter letter frequencies; susceptible to anagramming and rail-count brute force.",
    "columnar_transposition": "Letter frequencies unchanged; vulnerable to multiple-anagramming and digraph frequency scoring.",
}


class ComparisonService:
    """Runs fair, high-resolution comparative benchmarks across ciphers."""

    @classmethod
    def run_comparison(
        cls,
        message: str,
        selected_cipher_ids: Optional[List[str]] = None,
        custom_keys: Optional[Dict[str, str]] = None
    ) -> List[ComparisonRow]:
        """Execute encryption and decryption on the message across selected ciphers."""
        if selected_cipher_ids is None:
            selected_cipher_ids = list(CIPHER_REGISTRY.keys())
        if custom_keys is None:
            custom_keys = {}

        results: List[ComparisonRow] = []

        for cid in selected_cipher_ids:
            cipher = get_cipher(cid)
            key = custom_keys.get(cid, DEFAULT_COMPARISON_KEYS.get(cid, ""))

            # Handle OTP dynamic key generation to match length
            if cid == "one_time_pad" and not key:
                alpha_count = sum(1 for ch in message if ch.isalpha())
                key = OneTimePadCipher.generate_random_key(max(alpha_count, 1))

            try:
                # Benchmark Encryption
                t0_enc = time.perf_counter_ns()
                enc_res = cipher.encrypt(message, key)
                t1_enc = time.perf_counter_ns()
                enc_time_us = (t1_enc - t0_enc) / 1000.0

                # Benchmark Decryption
                t0_dec = time.perf_counter_ns()
                dec_res = cipher.decrypt(enc_res.text, key)
                t1_dec = time.perf_counter_ns()
                dec_time_us = (t1_dec - t0_dec) / 1000.0

                # Verify round-trip recovery
                # Some ciphers (Playfair, Hill) normalize to uppercase letters and add filler/padding
                recovered = dec_res.text
                if cid in ("playfair", "hill"):
                    # Check if normalized letters match (accounting for padding)
                    norm_input = "".join(c.upper() for c in message if c.isalpha()).replace("J", "I" if cid == "playfair" else "")
                    norm_rec = "".join(c for c in recovered if c.isalpha())
                    # Check prefix match (allowing filler/padding differences)
                    round_trip = norm_rec.startswith(norm_input) or (norm_input in norm_rec)
                else:
                    round_trip = (recovered == message)

                verdict = (
                    "Educational Only (Insecure for modern data)"
                    if cid != "one_time_pad"
                    else "Information-Theoretic Security (Strict conditions apply)"
                )

                row = ComparisonRow(
                    cipher_id=cid,
                    cipher_name=cipher.name,
                    category=cipher.category,
                    key_type=KEY_TYPE_DESCRIPTIONS.get(cid, "Standard"),
                    key_used=str(enc_res.key_display),
                    sample_input=message,
                    ciphertext=enc_res.text,
                    recovered_text=recovered,
                    round_trip_success=round_trip,
                    enc_time_us=round(enc_time_us, 2),
                    dec_time_us=round(dec_time_us, 2),
                    limitations=LIMITATIONS_DATA.get(cid, "Classical cipher with statistical weaknesses."),
                    security_verdict=verdict,
                )
                results.append(row)

            except Exception as exc:
                # Still record the failure row
                results.append(
                    ComparisonRow(
                        cipher_id=cid,
                        cipher_name=cipher.name,
                        category=cipher.category,
                        key_type=KEY_TYPE_DESCRIPTIONS.get(cid, "Standard"),
                        key_used=str(key),
                        sample_input=message,
                        ciphertext=f"ERROR: {exc}",
                        recovered_text="N/A",
                        round_trip_success=False,
                        enc_time_us=0.0,
                        dec_time_us=0.0,
                        limitations=f"Failed with input: {exc}",
                        security_verdict="Error during execution",
                    )
                )

        return results
