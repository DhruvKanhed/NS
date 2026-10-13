"""Unit tests for Rail Fence (Zigzag) Cipher."""

import unittest
from cryptotoolkit.ciphers.rail_fence import RailFenceCipher
from cryptotoolkit.utils.validation import ValidationError


class TestRailFenceCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = RailFenceCipher()

    def test_standard_zigzag(self):
        # "WE ARE DISCOVERED FLEE AT ONCE" with 3 rails
        plain = "WE ARE DISCOVERED FLEE AT ONCE"
        enc = self.cipher.encrypt(plain, 3)
        dec = self.cipher.decrypt(enc.text, 3)
        self.assertEqual(dec.text, plain)

    def test_all_characters_preserved(self):
        plain = "Defend the east wall! 100 soldiers."
        enc = self.cipher.encrypt(plain, 4)
        dec = self.cipher.decrypt(enc.text, 4)
        self.assertEqual(dec.text, plain)

    def test_edge_case_one_rail(self):
        plain = "HELLO WORLD"
        enc = self.cipher.encrypt(plain, 1)
        self.assertEqual(enc.text, plain)
        dec = self.cipher.decrypt(enc.text, 1)
        self.assertEqual(dec.text, plain)

    def test_edge_case_rails_greater_than_length(self):
        plain = "CAT"
        enc = self.cipher.encrypt(plain, 10)
        self.assertEqual(enc.text, plain)
        dec = self.cipher.decrypt(enc.text, 10)
        self.assertEqual(dec.text, plain)

    def test_edge_case_single_character(self):
        plain = "A"
        enc = self.cipher.encrypt(plain, 3)
        self.assertEqual(enc.text, plain)
        dec = self.cipher.decrypt(enc.text, 3)
        self.assertEqual(dec.text, plain)

    def test_invalid_rails(self):
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", 0)
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", -2)
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", "abc")


if __name__ == "__main__":
    unittest.main()
