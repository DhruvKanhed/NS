"""Integration tests for all cipher modules and comparison service."""

import unittest
from cryptotoolkit.ciphers import get_all_ciphers, CIPHER_REGISTRY
from cryptotoolkit.services.comparison_service import ComparisonService
from cryptotoolkit.utils.text_utils import egcd, mod_inverse


class TestIntegration(unittest.TestCase):
    def test_all_eight_ciphers_registered(self):
        ciphers = get_all_ciphers()
        self.assertEqual(len(ciphers), 8)
        self.assertEqual(len(CIPHER_REGISTRY), 8)

    def test_extended_gcd_and_modular_inverse(self):
        # gcd(9, 26) = 1, mod inverse = 3
        gcd, x, y = egcd(9, 26)
        self.assertEqual(gcd, 1)
        inv = mod_inverse(9, 26)
        self.assertEqual((9 * inv) % 26, 1)

        # No inverse for even number modulo 26
        with self.assertRaises(ValueError):
            mod_inverse(4, 26)

    def test_comparison_service_all_ciphers(self):
        message = "NETWORK SECURITY 2026"
        rows = ComparisonService.run_comparison(message)
        self.assertEqual(len(rows), 8)
        for r in rows:
            self.assertGreater(r.enc_time_us, 0.0)
            self.assertGreater(r.dec_time_us, 0.0)
            self.assertNotEqual(r.ciphertext, "")
            self.assertIn(r.category, ("Substitution", "Transposition"))


if __name__ == "__main__":
    unittest.main()
